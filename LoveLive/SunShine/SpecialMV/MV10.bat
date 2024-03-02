C:\Windows\system32\cmd.exe /c "start "foo" /b /wait /affinity 0xFFFFFFFFFFFFFFFF /node 0 "E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\MV\BDROM\BDMV\STREAM\10.vpy" - | "E:\BD\LoveLiveSunshine\x265.exe" --y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 32 --tu-inter-depth 4 --tu-intra-depth 4 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -3 --crqpoffs -3 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --rect --amp --ref 5 --limit-refs 0 --weightb --keyint 240 --min-keyint 23 --bframes 10 --aq-mode 1 --aq-strength 0.90 --rd 5 --psy-rd 1.8 --psy-rdoq 1.5 --vbv-maxrate 41200 --vbv-bufsize 51200 --rdoq-level 2 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --rc-grain --pools + -o "E:\BD\MV\BDROM\BDMV\STREAM\10-2.hevc" -"

:End
echo WORKSFINISHED
echo 
pause