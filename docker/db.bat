@echo off
setlocal
set image=pihome

@echo on
docker build -t %image% .
