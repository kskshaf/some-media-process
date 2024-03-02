@ECHO OFF & CD/D "%~dp0"

:start
IF "%~1"=="" GOTO :END

:mux
"E:\OKEGui\tools\mkvtoolnix\mkvmerge.exe" --output "%~1.mkv" --language 0:und "%~1.hevc" --language 0:jpn "%~1.flac" --track-order 0:0,1:0

:É¨Î²
SHIFT /1
GOTO :start

:End
echo ·â×°Íê³É£¡£¡£¡
echo 
pause