@ECHO OFF & CD/D "%~dp0"
 
::usage: double click bat to start encoding

set vspipe="E:\OKEGui\tools\vapoursynth\VSPipe.exe"

:start
IF "%~1"=="" GOTO :END 

:video
%vspipe% --y4m "%~n1.vpy" - | x264 --demuxer y4m --level 4.2 --preset veryslow --profile high --crf 16.0 --deblock -1:-1 --keyint 480 --min-keyint 1 --ref 9 --vbv-bufsize 35000 --vbv-maxrate 30000 --chroma-qp-offset 0 --no-mbtree --qcomp 0.65 --rc-lookahead 80 --aq-mode 3 --aq-strength 0.8 --merange 32 --psy-rd 0.60:0.00 --no-fast-pskip --colorprim bt709 --transfer bt709 --colormatrix bt709 --log-file "%~n1.log" --output "%~n1.264" -

:扫尾
SHIFT /1
GOTO :start

:End
echo 任务已完成
echo 
pause
