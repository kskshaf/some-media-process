@ECHO OFF & CD/D "%~dp0"
 
::usage: double click bat to start encoding

set eac3to="C:\Tools\eac3to.exe"

:start
IF "%~1"=="" GOTO :END 

%eac3to% "%~n1.m2ts" "%~n1.flac"

:ɨβ
SHIFT /1
GOTO :start

:End
echo ���������
echo 
pause
