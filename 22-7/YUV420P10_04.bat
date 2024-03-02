@ECHO OFF & CD/D "%~dp0"
 
::usage: double click bat to start encoding

set vspipe="E:\OKEGui\tools\vapoursynth\VSPipe.exe"

:start
IF "%~1"=="" GOTO :END 

:video
%vspipe% --y4m "%~n1.vpy" - | x265 --y4m -D 10 --preset slower --ctu 32 --crf 14.0 --high-tier --level-idc 4.1 --qg-size 8 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --vbv-maxrate 30000 --vbv-bufsize 36000 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.85 --rd 5 --psy-rd 2.0 --psy-rdoq 2.5 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --colorprim bt709 --transfer bt709 --colormatrix bt709 --no-strong-intra-smoothing --log-file "%~n1.log" --output "%~n1.hevc" -

:扫尾
SHIFT /1
GOTO :start

:End
echo 任务已完成
echo 
pause
