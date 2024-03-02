C:\Windows\system32\cmd.exe /c "start "foo" /b /wait /affinity 0xFFFFFFFFFFFFFFFF /node 0 "E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\MovieRework.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 1.00 --rd 5 --psy-rd 2.0 --psy-rdoq 1.6 --vbv-maxrate 46000 --vbv-bufsize 56000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.70 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\movierework.hevc" -"

:End
echo WORKSFINISHED
echo 
pause