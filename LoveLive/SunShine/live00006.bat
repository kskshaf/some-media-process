@echo off
::Part1 30p
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part1.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 18.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.5 --vbv-maxrate 40000 --vbv-bufsize 50000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part1.hevc"
::timeout 2
::Part2 30p anime
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part2.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 17.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.90 --rd 5 --psy-rd 1.8 --psy-rdoq 1.0 --vbv-maxrate 25000 --vbv-bufsize 35000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part2.hevc"
::timeout 2
::Part3 30p digest
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part3.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 19.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.0 --vbv-maxrate 30000 --vbv-bufsize 40000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part3.hevc"
::timeout 2
::Part4 24p digest
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part4.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 19.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.0 --vbv-maxrate 30000 --vbv-bufsize 40000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part4.hevc"
::timeout 2
::Part5 30p digest
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part5.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 19.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.0 --vbv-maxrate 30000 --vbv-bufsize 40000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part5.hevc"
::timeout 2
::Part6 24p digest
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part6.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 19.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.0 --vbv-maxrate 30000 --vbv-bufsize 40000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part6.hevc"
::timeout 2
::Part7 30p
::"E:\VapourSynthR61\VSPipe.exe" -c y4m "E:\BD\LoveLiveSunshine\live-00006-part7.vpy" - | "E:\OKEGui\tools\x26x\x265.exe" --input - --y4m -D 10 --preset slower --ctu 32 --crf 18.0 --qg-size 16 --tu-inter-depth 3 --tu-intra-depth 3 --max-tu-size 16 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 38 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.90 --rd 5 --psy-rd 1.6 --psy-rdoq 1.5 --vbv-maxrate 40000 --vbv-bufsize 50000 --rdoq-level 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709 --pools + -o "E:\BD\LoveLiveSunshine\live\live-00006-part7.hevc"
::timeout 2
::
::echo Please RPC at first, and then confirm to muxing.
::pause
::echo Are you sure to muxing£¿
::pause
echo Are you sure to muxing£¿£¿£¿
pause
::
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part1.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part1.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part2.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part2.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part3.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part3.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part4.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part4.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part5.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part5.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part6.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part6.hevc" --track-order 0:0
timeout 1
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006-part7.mkv" --language 0:und "E:\BD\LoveLiveSunshine\live\live-00006-part7.hevc" --track-order 0:0
timeout 2
"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --output "E:\BD\LoveLiveSunshine\live\live-00006.mkv" --timestamps "0:E:\BD\LoveLiveSunshine\live\00006.txt" --language 0:und "[" "E:\BD\LoveLiveSunshine\live\live-00006-part1.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part2.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part3.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part4.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part5.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part6.mkv" "E:\BD\LoveLiveSunshine\live\live-00006-part7.mkv" "]" --language 0:jpn "E:\BD\LoveLiveSunshine\live\00006.flac" --chapter-language jpn --chapters "E:\BD\LoveLiveSunshine\live\00006-cha.txt" --track-order 0:0,1:0
::Example
::"E:\OKEGui850\tools\mkvtoolnix\mkvmerge.exe" --chapter-language --output "movie.mkv" --language 0:und "[" "cut-001.hevc" "movierework.mkv" "cut-002.hevc" "]" --language 0:jpn "00004_3.flac" --language 0:eng "00004_4.sup" --chapters "E:\BD\LoveLiveSunshine\live\00006-cha.txt" --track-order 0:0,1:0,2:0
echo Jobs completed!
echo 
pause