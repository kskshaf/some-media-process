@echo off
"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\s2-in12.vpy" - | "E:\BD\LoveLiveSunshine\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 1.00 --rd 5 --psy-rd 2.0 --psy-rdoq 1.6 --vbv-maxrate 40000 --vbv-bufsize 50000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.70 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\s2-in12.hevc"
timeout 5
"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\s2-in13-ncop.vpy" - | "E:\BD\LoveLiveSunshine\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 1.00 --rd 5 --psy-rd 2.0 --psy-rdoq 1.6 --vbv-maxrate 40000 --vbv-bufsize 50000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.70 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\s2-in13-ncop.hevc"
timeout 5
echo 请RPC后再确认封装
pause
echo 确认封装？？？
pause

"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\s2-in09.mkv" --language 0:und "E:\BD\LoveLiveSunshine\s2-in09.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\s2-in09.flac" --track-order 0:0,1:0
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\s2-in11.mkv" --language 0:und "E:\BD\LoveLiveSunshine\s2-in11.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\s2-in11.flac" --track-order 0:0,1:0
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\s2-in12.mkv" --language 0:und "E:\BD\LoveLiveSunshine\s2-in12.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\s2-in12.flac" --track-order 0:0,1:0
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\s2-in13-ncop.mkv" --language 0:und "E:\BD\LoveLiveSunshine\s2-in13-ncop.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\s2-in13-ncop.flac" --track-order 0:0,1:0
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\s2-in13-nced.mkv" --language 0:und "E:\BD\LoveLiveSunshine\s2-in13-nced.hevc" --language 0:jpn "E:\BD\LoveLiveSunshine\s2-in13-nced.flac" --track-order 0:0,1:0

echo 封装完成！！！
echo 
pause