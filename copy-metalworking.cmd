@echo off
copy /Y "%~dp0inner-page-3.html" "%~dp0inner-page-metalworking.html"
find /c /v "" "%~dp0inner-page-metalworking.html"