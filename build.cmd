@echo off

if not "%~1"=="" set RELEASE_TAG=%~1

cargo build --release

pause
