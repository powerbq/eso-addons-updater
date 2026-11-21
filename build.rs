#[cfg(windows)]
fn main() {
    let icon = "icons/eso-addons-updater.ico";
    println!("cargo::rerun-if-changed={icon}");
    assert!(
        std::path::Path::new(icon).exists(),
        "{icon} not found — run ./icons.sh and commit icons/"
    );
    winresource::WindowsResource::new()
        .set_icon(icon)
        .compile()
        .expect("the Windows icon resource can be compiled");
}

#[cfg(not(windows))]
fn main() {}
