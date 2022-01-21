@ ECHO OFF
SET ansi.SELF=%~nx0
SET ansi.EXTENSIONS=
CALL :Extensions
IF NOT "%ansi.EXTENSIONS%"=="ON" SETLOCAL EnableExtensions & CALL :Help OFF && ENDLOCAL & ECHO OFF & @ GOTO :EOF
    SET ansi.ARGS=%*
    IF     "%~1"=="%1"         ( SET ansi.MODE=%~1)&( CALL :Arguments %ansi.ARGS:~2%)
    IF NOT "%~1"=="%1"         ( SET ansi.MODE=)
    IF "%ansi.MODE%"==""       CALL :Help
    IF "%ansi.MODE%"=="-h"     CALL :Help
    IF "%ansi.MODE%"=="-H"     START /D "%~dp0" CALL "%~nx0" -h
    IF "%ansi.MODE%"=="-c"     CALL :Current
    IF "%ansi.MODE%"=="-C"     START /D "%~dp0" CALL "%~nx0" -c
    IF "%ansi.MODE%"=="-t"     CALL :Text %ansi.ARGS%
    IF "%ansi.MODE%"=="-T"     START /D "%~dp0" CALL "%~nx0" -t %ansi.ARGS%
    IF "%ansi.MODE%"=="-m"     CALL :MarkUp %ansi.ARGS%
    IF "%ansi.MODE%"=="-M"     START /D "%~dp0" CALL "%~nx0" -t %ansi.ARGS%
    IF "%ansi.MODE%"=="-p"     CALL :Product %ansi.MARKUP%
    IF "%ansi.MODE%"=="-P"     START /D "%~dp0" CALL "%~nx0" -p %ansi.ARGS%
    IF "%ansi.MODE%"=="-d"     CALL :Default %ansi.ARGS%
    IF "%ansi.MODE%"=="-D"     START /D "%~dp0" CALL "%~nx0" -d %ansi.ARGS%
    IF "%ansi.MODE%"=="-i"     CALL :Import %ansi.ARGS%
    IF "%ansi.MODE%"=="-I"     START /D "%~dp0" CALL "%~nx0" -i %ansi.ARGS%
    IF "%ansi.MODE%"=="-e"     CALL :Export %ansi.ARGS%
::ECHO ON
@ GOTO :EOF




:: Verify current state of cmd /E:ON,OFF switch 
:Extensions
    ( SET ansi.EXTENSIONS=ON)
GOTO :EOF




:: Trim leading and ending space from argument string
:Arguments
    SET ansi.ARGS=%*
GOTO :EOF



:: Reset prompt and configurations to DEFAULT values
:Default
    IF         NOT "%*"==""  SET ansi.DEFAULT=%*
    IF "%ansi.DEFAULT%"=="none" ( SET ansi.DEFAULT=$E[m)
    IF "%ansi.DEFAULT%"=="$" ( SET ansi.DEFAULT=%ansi.PROMPT%)
    PROMPT %ansi.DEFAULT%
    FOR /F "delims==" %%A IN ('SET ansi.') DO ( SET %%A=)
GOTO :EOF




:: Set prompt to product of the specified configuration values
:Prompt
    IF NOT "%ansi.MARKUP%"=="" SET ansi.PROMPT=$E[38;2;%1;%2;%3m$E[48;2;%4;%5;%6m%ansi.TEXT%$E[38;2;%4;%5;%6m$E[48;2;%1;%2;%3m
    IF     "%ansi.MARKUP%"=="" SET ansi.PROMPT=%ansi.TEXT%
    PROMPT %ansi.PROMPT%
GOTO :EOF




:: Configure value of ansi prompt text
:Text
    SET ansi.TEXT=%*
    CALL :Prompt %ansi.MARKUP%
GOTO :EOF




::Configure value of ansi color markup
:MarkUp
	IF NOT "%1"=="" ( SET .R0=%1) ELSE ( SET /A .R0=255 * %RANDOM% / 32767 )
	IF NOT "%2"=="" ( SET .G0=%2) ELSE ( SET /A .G0=255 * %RANDOM% / 32767 )
	IF NOT "%3"=="" ( SET .B0=%3) ELSE ( SET /A .B0=255 * %RANDOM% / 32767 )
	IF NOT "%4"=="" ( SET .R1=%4) ELSE ( SET /A .R1=255 - %.R0% )
	IF NOT "%5"=="" ( SET .G1=%5) ELSE ( SET /A .G1=255 - %.G0% )
	IF NOT "%6"=="" ( SET .B1=%6) ELSE ( SET /A .B1=255 - %.B0% )
	SET ansi.MARKUP=%.R0%;%.G0%;%.B0%,%.R1%;%.G1%;%.B1%
	FOR /F "delims==" %%A IN ('SET .') DO ( SET %%A=)
    CALL :Prompt %ansi.MARKUP%
GOTO :EOF




:: Import prompt configuration values from the ansi.IMPORT file
:Import
    IF NOT "%~1"=="" SET ansi.IMPORT=%~1
    IF "%ansi.IMPORT%"=="" ECHO Import file name? & GOTO :EOF
    FOR /F "usebackq tokens=*" %%A IN (`type "%ansi.IMPORT%"`) DO SET %%A
    CALL :Prompt %ansi.MARKUP%
 GOTO :EOF




::Export current prompt configuration values to the ansi.EXPORT file
:Export
    IF NOT "%~1"=="" SET ansi.EXPORT=%~1
    IF "%ansi.EXPORT%"=="" ECHO Export file name? & GOTO :EOF
    ECHO ansi.MARKUP=%ansi.MARKUP%>"%ansi.EXPORT%"
    ECHO ansi.PROMPT=%ansi.PROMPT%>>"%ansi.EXPORT%"
    ECHO ansi.TEXT=%ansi.TEXT%>>"%ansi.EXPORT%"
GOTO :EOF




:: Print current ANSI prompt settings 
:Current
    ECHO.
    ECHO Current settings of ANSI prompt configurator
    ECHO --------------------------------------------
    SET ansi.
    SET PROMPT
GOTO :EOF




:: Print help with syntax and usage followed by current ANSI prompt settings
:Help
    IF "%1"=="OFF" ECHO    CURRENT COMMAND EXTENSIONS ARE DISABLED !!! & ECHO.
    ECHO.
    ECHO Argument syntax of ANSI prompt configurator:
    ECHO --------------------------------------------
    ECHO     "%ansi.SELF%"  [MODE  (ARGS)]
    ECHO.
    ECHO     [-h(,-H)]  print help with syntax and usage
    ECHO     [-c(,-C)]  print CURRENT ansi prompt settings
    ECHO     [-m(,-M)]  configure value of ansi color MARKUP 
    ECHO     [-t(,-T)]  configure value of prompt TEXT 
    ECHO     [-p(,-P)]  set prompt to PRODUCT of the specified configuration values
    ECHO     [-d(,-D)]  reset prompt and configurations to DEFAULT values
    ECHO     [-i(,-I)]  IMPORT prompt configuration values from a file
    ECHO     [-e]       EXPORT current prompt configuration values to a file
    ECHO.
    ECHO     * "%ansi.SELF%" is the current file name of the ansi prompt configurator
    ECHO     * [MODE] is a processing mode of the ansi prompt configurator
    ECHO     * (ARGS) are parameters of the MODE
    ECHO     * Color ARGS format: R0,G0,B0,R1,G1,B1
    ECHO     * R0,G0,B0 foreground color component: true color {0,...,255} or random
    ECHO     * R1,G1,B1 background color component: true color {0,...,255} or compementary
    ECHO     * Use capital letter mode to run the configurator in a separate window
    ECHO     * Subshell prompt settings do not affect the top shell prompt
    ECHO     * Clear screen (CLS) to fill current window with specified ansi color
    ECHO     * To run the "%ansi.SELF%" enable command extensions, CMD /E:ON
    ECHO.
    ECHO Usage of ANSI prompt configurator:
    ECHO ----------------------------------
    ECHO     "%ansi.SELF%" -H
    ECHO     "%ansi.SELF%" -M
    ECHO     "%ansi.SELF%" -c
    ECHO     "%ansi.SELF%" -m 255,200,0,0,55,255
    ECHO     "%ansi.SELF%" -m 255,200
    ECHO     "%ansi.SELF%" -t $+$T$S$P$G
    ECHO     "%ansi.SELF%" -P
    ECHO     "%ansi.SELF%" -D
    ECHO     "%ansi.SELF%" -d none
    ECHO     "%ansi.SELF%" -d $
    ECHO     "%ansi.SELF%" -d $E[38;2;255;200;100m$T$S$P$G
    ECHO     "%ansi.SELF%" -e config.txt
    ECHO     "%ansi.SELF%" -I config.txt
GOTO :EOF
