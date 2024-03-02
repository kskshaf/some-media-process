@ECHO OFF & CD/D "%~dp0"
::pause
pause
::Encode
"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\ShinePost\sp\Untitled.vpy" - | "E:\BD\ShinePost\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 18.0 --qg-size 32 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.80 --rd 5 --psy-rd 1.5 --psy-rdoq 0.7 --vbv-maxrate 32000 --vbv-bufsize 38000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\ShinePost\sp\sp-video.hevc"
::pause
pause