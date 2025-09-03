@ECHO OFF & CD /D "%~dp0"
 
::usage: double click bat to start encoding

set eac3to="D:\OKEGui850\tools\eac3to\eac3to-wrapper.exe"
::mkdir eac3to_log

:start
if "%~n1"=="" GOTO End
%eac3to% "%~n1.m2ts" "%~n1.wav"
move "%~n1 - Log.txt" eac3to_log
timeout 1
shift
GOTO start

:End
echo end
pause
