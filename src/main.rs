#![windows_subsystem = "windows"]

// SPDX-License-Identifier: MIT
// Copyright (c) 2026 powerbq

use std::fmt;
use std::fs;
use std::fs::File;
use std::io;
use std::io::Cursor;
use std::io::Read;
use std::path::Path;
use std::path::PathBuf;
use std::process::Command;
use std::thread;
use std::time::Duration;

use fltk::app;
use fltk::frame::Frame;
use fltk::misc::Progress;
use fltk::prelude::*;
use fltk::window::Window;
use sha2::Digest;
use sha2::Sha256;

const RELEASE_TAG: &str = match option_env!("RELEASE_TAG") {
    Some(tag) => tag,
    None => "current",
};

const UPDATER_REPO: &str = "https://github.com/powerbq/eso-addons-updater/releases/download";
const MANAGER_RELEASES: &str = "https://github.com/powerbq/eso-addons-manager/releases";
const MANAGER_API: &str = "https://api.github.com/repos/powerbq/eso-addons-manager/releases";

// The baked channel decides which manager the updater fetches: `testing` → the newest pre-release (via
// the API), anything else → the stable `latest` release (via the redirect).
const CHANNEL_TESTING: &str = "testing";

#[cfg(windows)]
const UPDATER_ASSET: &str = "app.exe";
#[cfg(windows)]
const MANAGER_EXE: &str = "app.exe";
#[cfg(windows)]
const MANAGER_ASSET: &str = "eso-addons-manager-windows-amd64.zip";

#[cfg(target_os = "linux")]
const UPDATER_ASSET: &str = "app";
#[cfg(target_os = "linux")]
const MANAGER_EXE: &str = "app";
#[cfg(target_os = "linux")]
const MANAGER_ASSET: &str = "eso-addons-manager-linux-amd64.zip";

#[cfg(target_os = "macos")]
const UPDATER_ASSET: &str = "app-macos";
#[cfg(target_os = "macos")]
const MANAGER_EXE: &str = "app.app/Contents/MacOS/app";
#[cfg(target_os = "macos")]
const MANAGER_ASSET: &str = "eso-addons-manager-macos-arm64.zip";

const VERSION_FILE: &str = "version.txt";
const SUMS_FILE: &str = "SHA256SUMS";
const UPDATER_VERSION: &str = env!("CARGO_PKG_VERSION");
const USER_AGENT: &str = concat!("eso-addons-updater/", env!("CARGO_PKG_VERSION"));

const CONNECT_TIMEOUT: Duration = Duration::from_secs(10);
const READ_TIMEOUT: Duration = Duration::from_secs(60);

type Sha256Digest = [u8; 32];

#[derive(Debug)]
enum Error {
    Io(io::Error),
    Http(Box<ureq::Error>),
    Zip(zip::result::ZipError),
    Json(serde_json::Error),
    Msg(&'static str),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Io(e) => write!(f, "{e}"),
            Error::Http(e) => write!(f, "{e}"),
            Error::Zip(e) => write!(f, "{e}"),
            Error::Json(e) => write!(f, "{e}"),
            Error::Msg(m) => write!(f, "{m}"),
        }
    }
}

impl std::error::Error for Error {}

impl From<io::Error> for Error {
    fn from(e: io::Error) -> Self {
        Error::Io(e)
    }
}

impl From<ureq::Error> for Error {
    fn from(e: ureq::Error) -> Self {
        Error::Http(Box::new(e))
    }
}

impl From<zip::result::ZipError> for Error {
    fn from(e: zip::result::ZipError) -> Self {
        Error::Zip(e)
    }
}

impl From<serde_json::Error> for Error {
    fn from(e: serde_json::Error) -> Self {
        Error::Json(e)
    }
}

#[derive(serde::Deserialize)]
struct Release {
    tag_name: String,
    #[serde(default)]
    draft: bool,
}

// The newest release tag by SemVer among non-drafts (pre-releases included), so the testing channel is
// never empty: with no pre-release it resolves to the stable latest. Tags keep their leading `v`.
fn newest(releases: &[Release]) -> Option<&str> {
    releases
        .iter()
        .filter(|release| !release.draft)
        .filter_map(|release| {
            let version = semver::Version::parse(release.tag_name.strip_prefix('v')?).ok()?;
            Some((version, release.tag_name.as_str()))
        })
        .max_by(|a, b| a.0.cmp(&b.0))
        .map(|(_, tag)| tag)
}

type Result<T> = std::result::Result<T, Error>;

#[derive(Clone)]
enum Msg {
    Status(String),
    Progress(f64),
    Restart(String),
    Quit,
    Fatal(String),
}

fn http_agent() -> ureq::Agent {
    ureq::AgentBuilder::new()
        .timeout_connect(CONNECT_TIMEOUT)
        .timeout_read(READ_TIMEOUT)
        .user_agent(USER_AGENT) // GitHub's API 403s without a User-Agent; harmless on asset downloads
        .build()
}

fn updater_url() -> String {
    format!("{UPDATER_REPO}/{RELEASE_TAG}/{UPDATER_ASSET}")
}

fn updater_version_url() -> String {
    format!("{UPDATER_REPO}/{RELEASE_TAG}/{VERSION_FILE}")
}

fn updater_sums_url() -> String {
    format!("{UPDATER_REPO}/{RELEASE_TAG}/{SUMS_FILE}")
}

// The manager release this updater's baked channel should install: the asset-download base plus the
// version. `testing` takes the newest by SemVer (pre-releases included) from the releases API; any
// other channel takes the stable `latest` (the newest non-pre-release). Both resolve a concrete tag
// and download that tag's assets — no `version.txt` asset is read; the version comes from the tag.
struct ManagerRelease {
    base: String,
    version: String,
}

fn manager_release(agent: &ureq::Agent) -> Result<ManagerRelease> {
    let tag = if RELEASE_TAG == CHANNEL_TESTING {
        let body = remote_text(agent, MANAGER_API)?;
        let releases: Vec<Release> = serde_json::from_str(&body)?;
        newest(&releases)
            .ok_or(Error::Msg("no manager release found"))?
            .to_owned()
    } else {
        let body = remote_text(agent, &format!("{MANAGER_API}/latest"))?;
        let release: Release = serde_json::from_str(&body)?;
        release.tag_name
    };
    let version = tag.strip_prefix('v').unwrap_or(&tag).to_owned();
    Ok(ManagerRelease {
        base: format!("{MANAGER_RELEASES}/download/{tag}"),
        version,
    })
}

fn manager_asset_url(base: &str) -> String {
    format!("{base}/{MANAGER_ASSET}")
}

fn manager_sums_url(base: &str) -> String {
    format!("{base}/{SUMS_FILE}")
}

fn parse_sha256(text: &str) -> Option<Sha256Digest> {
    let token = text.split_whitespace().next()?;
    if token.len() != 64 {
        return None;
    }
    let mut digest = [0u8; 32];
    let (pairs, _) = token.as_bytes().as_chunks::<2>();
    for (byte, pair) in digest.iter_mut().zip(pairs) {
        let pair = std::str::from_utf8(pair).ok()?;
        *byte = u8::from_str_radix(pair, 16).ok()?;
    }
    Some(digest)
}

fn sha256(data: &[u8]) -> Sha256Digest {
    Sha256::digest(data).into()
}

fn remote_text(agent: &ureq::Agent, url: &str) -> Result<String> {
    Ok(agent.get(url).call()?.into_string()?)
}

fn sha_from_sums(sums: &str, asset: &str) -> Option<Sha256Digest> {
    sums.lines().find_map(|line| {
        let mut parts = line.split_whitespace();
        let hex = parts.next()?;
        let name = parts.next()?;
        let name = name.strip_prefix('*').unwrap_or(name);
        (name == asset).then(|| parse_sha256(hex)).flatten()
    })
}

fn download(agent: &ureq::Agent, url: &str, s: &app::Sender<Msg>) -> Result<Vec<u8>> {
    let resp = agent.get(url).call()?;
    let total: u64 = resp
        .header("Content-Length")
        .and_then(|v| v.parse().ok())
        .unwrap_or(0);
    let mut reader = resp.into_reader();
    let mut body = if total > 0 {
        Vec::with_capacity(total as usize)
    } else {
        Vec::new()
    };
    let mut chunk = [0u8; 64 * 1024];
    let mut done: u64 = 0;
    loop {
        let n = reader.read(&mut chunk)?;
        if n == 0 {
            break;
        }
        body.extend_from_slice(&chunk[..n]);
        done += n as u64;
        if total > 0 {
            s.send(Msg::Progress(done as f64 / total as f64));
        }
    }
    Ok(body)
}

fn update_self(updater_path: &Path, agent: &ureq::Agent, s: &app::Sender<Msg>) -> Result<bool> {
    let remote_version = remote_text(agent, &updater_version_url())?;
    let remote_version = remote_version.trim();
    if remote_version.is_empty() {
        return Err(Error::Msg("empty remote updater version"));
    }
    if remote_version == UPDATER_VERSION {
        return Ok(false);
    }

    let sums = remote_text(agent, &updater_sums_url())?;
    let remote =
        sha_from_sums(&sums, UPDATER_ASSET).ok_or(Error::Msg("updater checksum not found"))?;

    s.send(Msg::Status("Updating updater...".into()));
    let body = download(agent, &updater_url(), s)?;
    if sha256(&body) != remote {
        return Err(Error::Msg("updater checksum mismatch"));
    }

    let bak = with_suffix(updater_path, ".bak");
    let _ = fs::remove_file(&bak);
    fs::rename(updater_path, &bak)?;
    fs::write(updater_path, &body)?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        fs::set_permissions(updater_path, fs::Permissions::from_mode(0o755))?;
    }
    Ok(true)
}

fn extract_zip(body: &[u8], staging: &Path) -> Result<()> {
    let mut archive = zip::ZipArchive::new(Cursor::new(body))?;
    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        let name = match file.enclosed_name() {
            Some(n) => n,
            None => continue,
        };
        let outpath = staging.join(name);
        if file.is_dir() {
            fs::create_dir_all(&outpath)?;
            continue;
        }
        if let Some(parent) = outpath.parent() {
            fs::create_dir_all(parent)?;
        }
        #[cfg(unix)]
        {
            if let Some(mode) = file.unix_mode() {
                if mode & 0o170000 == 0o120000 {
                    let mut target = String::new();
                    file.read_to_string(&mut target)?;
                    let _ = fs::remove_file(&outpath);
                    std::os::unix::fs::symlink(target, &outpath)?;
                    continue;
                }
            }
        }
        let mut out = File::create(&outpath)?;
        io::copy(&mut file, &mut out)?;
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            if let Some(mode) = file.unix_mode() {
                fs::set_permissions(&outpath, fs::Permissions::from_mode(mode))?;
            }
        }
    }

    Ok(())
}

fn update_manager(manager_dir: &Path, agent: &ureq::Agent, s: &app::Sender<Msg>) -> Result<()> {
    let release = manager_release(agent)?;
    let remote_version = release.version.as_str();
    if remote_version.is_empty() {
        return Err(Error::Msg("empty remote manager version"));
    }

    let marker = manager_dir.join(VERSION_FILE);
    let up_to_date = fs::read_to_string(&marker)
        .as_deref()
        .map(str::trim)
        .map(|local| local == remote_version)
        .unwrap_or(false);
    if up_to_date && manager_dir.join(MANAGER_EXE).is_file() {
        return Ok(());
    }

    let sums = remote_text(agent, &manager_sums_url(&release.base))?;
    let remote =
        sha_from_sums(&sums, MANAGER_ASSET).ok_or(Error::Msg("manager checksum not found"))?;

    s.send(Msg::Status("Downloading manager...".into()));
    let body = download(agent, &manager_asset_url(&release.base), s)?;
    if sha256(&body) != remote {
        return Err(Error::Msg("manager checksum mismatch"));
    }

    s.send(Msg::Status("Extracting manager...".into()));
    if manager_dir.is_dir() {
        fs::remove_dir_all(manager_dir)?;
    }
    fs::create_dir_all(manager_dir)?;
    if let Err(e) = extract_zip(&body, manager_dir) {
        let _ = fs::remove_dir_all(manager_dir);
        return Err(e);
    }
    fs::write(&marker, remote_version)?;

    s.send(Msg::Status("Manager updated.".into()));
    Ok(())
}

fn with_suffix(path: &Path, suffix: &str) -> PathBuf {
    let mut s = path.as_os_str().to_os_string();
    s.push(suffix);
    PathBuf::from(s)
}

fn launch(manager_dir: &Path, updater_dir: &Path) -> io::Result<()> {
    let exe = manager_dir.join(MANAGER_EXE);
    let mut cmd = Command::new(exe);
    cmd.current_dir(updater_dir);
    // The updater has already applied the channel's update, so the manager's own in-app check is off.
    cmd.arg("--no-update-check");
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        const DETACHED_PROCESS: u32 = 0x0000_0008;
        const CREATE_NEW_PROCESS_GROUP: u32 = 0x0000_0200;
        cmd.creation_flags(DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP);
    }
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        cmd.process_group(0);
    }
    cmd.spawn().map(|_| ())
}

fn run(updater_dir: PathBuf, manager_dir: PathBuf, updater_path: PathBuf, s: app::Sender<Msg>) {
    let agent = http_agent();

    match update_self(&updater_path, &agent, &s) {
        Ok(true) => {
            s.send(Msg::Restart(
                "Updater updated. Please close and open it again to continue.".into(),
            ));
            return;
        }
        Ok(false) => {}
        Err(e) => s.send(Msg::Status(format!("Updater update skipped: {e}"))),
    }

    if let Err(e) = update_manager(&manager_dir, &agent, &s) {
        if !manager_dir.join(MANAGER_EXE).is_file() {
            s.send(Msg::Fatal(format!("Manager update failed: {e}")));
            return;
        }
        s.send(Msg::Status(format!("Manager update skipped: {e}")));
    }

    if !manager_dir.join(MANAGER_EXE).is_file() {
        s.send(Msg::Fatal(
            "Manager not found and could not be downloaded.".into(),
        ));
        return;
    }

    s.send(Msg::Status("Launching...".into()));
    match launch(&manager_dir, &updater_dir) {
        Ok(()) => s.send(Msg::Quit),
        Err(e) => s.send(Msg::Fatal(format!("Failed to launch manager: {e}"))),
    }
}

fn main() {
    let updater_path = match std::env::current_exe() {
        Ok(path) => path,
        Err(e) => {
            fltk::dialog::alert_default(&format!("Cannot resolve own path: {e}"));
            return;
        }
    };
    let updater_dir = match updater_path.parent() {
        Some(dir) => dir.to_path_buf(),
        None => {
            fltk::dialog::alert_default("Cannot resolve install directory.");
            return;
        }
    };
    let manager_dir = updater_dir.join("manager");

    let application = app::App::default().with_scheme(app::Scheme::Gtk);
    let (s, r) = app::channel::<Msg>();

    let mut window = Window::default()
        .with_size(480, 130)
        .center_screen()
        .with_label("ESO Addons Updater");
    let mut status = Frame::new(20, 25, 440, 30, "Checking for updates...");
    let mut progress = Progress::new(20, 75, 440, 24, "");
    progress.set_maximum(1.0);
    window.end();
    window.show();

    thread::spawn(move || run(updater_dir, manager_dir, updater_path, s));

    while application.wait() {
        if let Some(msg) = r.recv() {
            match msg {
                Msg::Status(text) => status.set_label(&text),
                Msg::Progress(value) => {
                    progress.set_value(value);
                    progress.set_label(&format!("{:.0}%", value * 100.0));
                }
                Msg::Restart(text) => {
                    status.set_label(&text);
                    progress.set_value(1.0);
                    progress.set_label("100%");
                }
                Msg::Fatal(text) => status.set_label(&text),
                Msg::Quit => application.quit(),
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn release(tag: &str, draft: bool) -> Release {
        Release {
            tag_name: tag.to_owned(),
            draft,
        }
    }

    #[test]
    fn newest_is_max_semver_among_non_drafts() {
        let releases = [
            release("v0.1.0-rc.2", false),
            release("v0.1.0-rc.10", false),
            release("v0.1.0", false),
            release("v9.9.9", true), // draft: ignored even though highest
        ];
        assert_eq!(newest(&releases), Some("v0.1.0"));
    }

    #[test]
    fn newest_prefers_newest_rc_when_no_final() {
        let releases = [
            release("v0.1.0-rc.1", false),
            release("v0.1.0-rc.10", false),
        ];
        assert_eq!(newest(&releases), Some("v0.1.0-rc.10"));
    }

    #[test]
    fn newest_is_none_without_valid_non_drafts() {
        assert_eq!(newest(&[]), None);
        assert_eq!(newest(&[release("nightly", false)]), None);
        assert_eq!(newest(&[release("v1.0.0", true)]), None);
    }

    #[test]
    fn release_deserialises_without_draft_field() {
        let releases: Vec<Release> =
            serde_json::from_str(r#"[{"tag_name":"v0.1.0","prerelease":false}]"#).unwrap();
        assert_eq!(releases.len(), 1);
        assert_eq!(releases[0].tag_name, "v0.1.0");
        assert!(!releases[0].draft);
    }
}
