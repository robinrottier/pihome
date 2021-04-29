@echo off
setlocal
set image=pihome

if exist Dockerfile        set f=Dockerfile&set c=..
if exist docker\Dockerfile set f=docker\Dockerfile&set c=.

@echo on
docker build -t %image% -f %f% %c%
