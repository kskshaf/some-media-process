@ECHO OFF & CD/D "%~dp0"

:start
IF "%~1"=="" GOTO :END

avs2pipemod64 -wav "%~n1.avs" > "%~n1.wav"

flac -8 -o "%~n1.flac" "%~n1.wav"

del "%~n1.wav"

:ɨβ
SHIFT /1
GOTO :start

:End
echo ���������
echo 
pause