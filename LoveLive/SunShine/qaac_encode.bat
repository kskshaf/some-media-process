@ECHO OFF & CD/D "%~dp0"

:start
IF "%~1"=="" GOTO :END

:encode
"E:\OKEGui850\tools\qaac\qaac64.exe" -v 320 -q 2 --no-delay -o "%~n1.aac" "%~n1.flac"

:扫尾
SHIFT /1
GOTO :start

:End
echo 任务已完成
echo 
pause