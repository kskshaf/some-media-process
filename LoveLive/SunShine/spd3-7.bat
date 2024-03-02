@echo off
echo 请确认该任务是否已完成！
pause
echo 请再次确认该任务是否已完成！！！
pause
echo 请确认是否开始该新任务？
pause
"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\spcut.vpy" - | "E:\BD\LoveLiveSunshine\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 19.0 --qg-size 32 --tu-inter-depth 2 --tu-intra-depth 2 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.5 --vbv-maxrate 35000 --vbv-bufsize 45000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\spd3-7.hevc"
timeout 2

"E:\OKEGui\tools\mkvtoolnix\mkvmerge.exe" -o spd3-7.mkv spd3-7.hevc
echo NO ERROR?
pause

move "E:\BD\LoveLiveSunshine\spd3-7.mkv" "E:\BD\LoveLiveSunshine\output\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\Special Disc 3\spd3-7.mkv"
echo NO ERROR??
pause

cd "E:\BD\LoveLiveSunshine\output\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\Special Disc 3\"
echo NO ERROR???
pause

"E:\OKEGui\tools\mkvtoolnix\mkvmerge.exe" -o 00007-2.mkv --language 0:und "[" "spd3-7.mkv" "cut-partb.mkv" "]" --language 0:jpn "00007_2.aac" --chapters "00007.txt" --track-order 0:0,1:0

:End
echo 
pause