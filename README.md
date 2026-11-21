# ESO Addons Updater

> **Legacy.** The main project is now
> [ESO Addons Manager](https://github.com/powerbq/eso-addons-manager), which you can
> download and install directly (installers and standalone builds, with a built-in
> update check). This updater remains only for people who already use it: it still
> works and keeps launching and updating the manager. New users do not need it —
> see the manager's repository for the user documentation.

## What it is

A small launcher that downloads the ESO Addons Manager, keeps it up to date and runs
it. On launch it reads the manager's release `version.txt`, and if it differs from
the installed version it downloads the new binary, verifies it against `SHA256SUMS`,
swaps it in and launches it. It updates itself the same way.

## For existing users

Latest release: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

| System | File |
|--------|------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> Intel architecture on macOS is not supported.

Place the file in its own folder and run it (on Linux, grant execute permission
first). It updates itself and the manager on launch.

On Windows the program is unsigned, so SmartScreen will most likely warn about an
unknown publisher — click **"More info"** → **"Run anyway"**.

To stop using the updater, install the manager directly instead (see its
repository) — the two share the same per-user data, so your settings and add-ons
carry over.

## Build

The updater is written in Rust. The manager's codebase and the runtime assets the
updater downloads live in
[powerbq/eso-addons-manager](https://github.com/powerbq/eso-addons-manager).

```bash
./build.sh   # Linux / macOS
build.cmd    # Windows
```

This runs `cargo build --release`; the binary is written to `target/release/`.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 powerbq.
