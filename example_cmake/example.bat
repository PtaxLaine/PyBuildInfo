@echo off
setlocal

IF NOT exist build (
	mkdir build
	IF NOT %errorlevel%==0 (exit /B -1)
)

cd build
IF NOT %errorlevel%==0 (exit /B -1)

cmake ..
IF NOT %errorlevel%==0 (
	IF %errorlevel%==9009 (
		echo please append path to cmake.exe in PATH env
	)
	exit /B -1
)

cmake --build . --target buildInfoExample_RUN
IF NOT %errorlevel%==0 (exit /B -1)

endlocal
