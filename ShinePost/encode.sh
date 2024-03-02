#!/usr/bin/bash
# thanks for xyx98's help!
export SYS_PATH=$PATH
export PATH=$HOME/myenc/bin
export LD_LIBRARY_PATH=$HOME/myenc/lib
export PREFIX=/home/ksks/myenc
export prefix=/home/ksks/myenc
export bin=/home/ksks/myenc/bin

export enc_p="--y4m -D 10 --preset slower --ctu 32 --crf 14.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.76 --rd 5 --psy-rd 2.0 --psy-rdoq 1.0 --vbv-maxrate 42000 --vbv-bufsize 48000 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

export enc_p_live="--y4m -D 10 --preset slower --ctu 32 --crf 18.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -3 --crqpoffs -3 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.80 --rd 5 --psy-rd 2.0 --psy-rdoq 1.0 --vbv-maxrate 42000 --vbv-bufsize 48000 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

export enc_mv="--y4m -D 10 --preset slower --ctu 32 --crf 14.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -3 --crqpoffs -3 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 3 --aq-strength 0.80 --rd 5 --psy-rd 2.0 --psy-rdoq 1.2 --vbv-maxrate 42000 --vbv-bufsize 48000 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

export enc_menu="--y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.80 --rd 5 --psy-rd 2.0 --psy-rdoq 1.0 --vbv-maxrate 25000 --vbv-bufsize 30000 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

# Menu
#$bin/vspipe -c y4m "menu_01.py" - | $bin/x265 --input - $enc_menu --output "menu_01.hevc"
#PATH=$SYS_PATH mkvmerge --output "menu_01.mkv" "menu_01.hevc"

$bin/vspipe -c y4m "pv.py" - | $bin/x265 --input - $enc_menu --output "pv.hevc"
PATH=$SYS_PATH mkvmerge --output "pv.mkv" --language 0:und "pv.hevc" --language 0:ja "pv.flac" --track-order 0:0,1:0

# 10
#$bin/vspipe -c y4m "10.vpy" - | $bin/x265 --input - $enc_p --output "10.hevc"
#PATH=$SYS_PATH mkvmerge --output "10.mkv" --language 0:und "10.hevc" --language 0:ja "10.flac" --chapter-language en --chapters "10.txt" --track-order 0:0,1:0
#$bin/vspipe -p rpc_10.vpy . | $bin/python3.11 qc2.py > rpc_10.txt
#mv 10.vpy 10.flac 10.hevc 10.txt rpc_10.vpy rpc_10.txt used
# 11
#$bin/vspipe -c y4m "11.vpy" - | $bin/x265 --input - $enc_p --output "11.hevc"
#PATH=$SYS_PATH mkvmerge --output "11.mkv" --language 0:und "11.hevc" --language 0:ja "11.flac" --chapter-language en --chapters "11.txt" --track-order 0:0,1:0
#$bin/vspipe -p rpc_11.vpy . | $bin/python3.11 qc2.py > rpc_11.txt
#mv 11.vpy 11.flac 11.hevc 11.txt rpc_11.vpy rpc_11.txt used
# 12
#$bin/vspipe -c y4m "12.vpy" - | $bin/x265 --input - $enc_p --output "12.hevc"
#PATH=$SYS_PATH mkvmerge --output "12.mkv" --default-track "0:1" --language 0:und "12.hevc" --default-track "0:1" --language 0:ja "12.flac" --default-track "0:0" --language 0:ja "12_2.aac" --chapter-language en --chapters "12.txt" --track-order 0:0,1:0,2:0
#$bin/vspipe -p rpc_12.vpy . | $bin/python3.11 qc2.py > rpc_12.txt
#mv 12.vpy 12.flac 12.hevc 12.txt rpc_12.vpy rpc_12.txt used
# 12_ed
#$bin/vspipe -c y4m "12_ed.vpy" - | $bin/x265 --input - $enc_p --output "12_ed.hevc"
#$bin/vspipe -p rpc_12ed.vpy . | $bin/python3.11 qc2.py

# op

#$bin/vspipe -c y4m "op.vpy" - | $bin/x265 --input - $enc_p --output "op.hevc"
#$bin/vspipe -p rpc_op.vpy . | $bin/python3.11 qc2.py > rpc_op.txt

#$bin/vspipe -c y4m "ed.vpy" - | $bin/x265 --input - $enc_p --output "ed.hevc"
#$bin/vspipe -p rpc_ed.vpy . | $bin/python3.11 qc2.py > rpc_ed.txt

#$bin/vspipe -c y4m "live_op.vpy" - | $bin/x265 --input - $enc_p_live --output "live_op.hevc"
#$bin/vspipe -p rpc_liveop.vpy . | $bin/python3.11 qc2.py > rpc_liveop.txt

#PATH=$SYS_PATH mkvmerge --output "op.mkv" --language 0:und "op.hevc" --language 0:ja "op_2.flac" --track-order 0:0,1:0
#PATH=$SYS_PATH mkvmerge --output "ed.mkv" --language 0:und "ed.hevc" --language 0:ja "ed.flac" --track-order 0:0,1:0
#PATH=$SYS_PATH mkvmerge --output "live_op.mkv" --language 0:und "live_op.hevc" --language 0:ja "live_op.flac" --track-order 0:0,1:0

# mv
#$bin/vspipe -c y4m "mv2.vpy" - | $bin/x265 --input - $enc_mv --output "mv2.hevc"
#$bin/vspipe -p rpc_mv2.vpy . | $bin/python3.11 qc2.py > rpc_mv2.txt

#$bin/vspipe -c y4m "mv1.vpy" - | $bin/x265 --input - $enc_mv --output "mv1.hevc"
#$bin/vspipe -p rpc_mv1.vpy . | $bin/python3.11 qc2.py > rpc_mv1.txt

echo enc end
