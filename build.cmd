@echo off

cd build

pyinstaller --clean ..\app.spec

pause
