@echo off
::Part1 30p
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00007-00008.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 18.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.5 --vbv-maxrate 40000 --vbv-bufsize 50000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\landing-action-yeah\lay.hevc"
echo Are you sure to muxing£¿£¿£¿
pause
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\landing-action-yeah\lay.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\landing-action-yeah\lay.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\live\landing-action-yeah\lay.flac" --chapter-language jpn --chapters "E:\BD\LoveLiveSunshine\live\landing-action-yeah\lay-cha.txt" --track-order 0:0,1:0
echo ·â×°Íê³É£¡£¡£¡
echo 
pause