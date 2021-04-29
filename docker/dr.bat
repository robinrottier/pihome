@echo off
setlocal
set options=--rm --name pihome -p 7080:80 -p 7081:3306
set image=pihome

set detached=-d
if "%1" == "-d"   shift&set detached=-d
if "%1" == "-nd"  shift&set detached=

if "%1" == "-i"  shift&set options=%options% -it
if "%1" == "-it" shift&set options=%options% -it

rem kill previosu run?
docker kill pihome >nul 2>&1

@echo on
docker run %detached% %options% %image% %1 %2 %3 %4
@echo off
echo.
echo Try browse to http://localhost:7080 for website
echo OR execute "docker exec -it pihome ash" to run terminal shell
echo.
