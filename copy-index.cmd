@echo off
copy /Y "%~dp0inner-page-1.html" "%~dp0index.html"
find /c /v "" "%~dp0inner-page-1.html"
find /c /v "" "%~dp0index.html"