#!/usr/bin/bash
set -euo pipefail

export PATH="/home/rip/ripenv/bin:$PATH"
export PYTHONUSERBASE="/home/rip/ripenv"
export LD_LIBRARY_PATH="/home/rip/ripenv/lib:/home/rip/ripenv/lib/vapoursynth"
export bin="/home/rip/ripenv/bin"
export param_01="--y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.90 --rd 5 --psy-rd 2.0 --psy-rdoq 1.0 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

export base_path="/mnt/Disk/BD"
cd $base_path/enc

enc_start_num=2
enc_end_num=2

for ((i=$enc_start_num; i<=$enc_end_num; i++)); do
    export ENC_SP=$i
    num=$(printf "%02d" $i)

    $bin/vspipe -c y4m enc.vpy -g full
#     $bin/vspipe -c y4m enc.vpy - | $bin/x265-gcc15.1 --input - $param_01 --output "$num.hevc"
#     sleep 10
#
#     if (($i >=1 && $i <= 7)); then
#         demux_src_base="$base_path/demux/10924"
#         demux_src_num=$(expr 16 - 1 + $i)
#     elif (($i >=8 && $i <= 13)); then
#         demux_src_base="$base_path/demux/10925"
#         demux_src_num=$(expr 16 - 8 + $i)
#     fi
#
#     # MKV MUX
#     mkvmerge --output "$num.mkv" --language 0:und "$num.hevc" --language 0:ja "$demux_src_base/000$demux_src_num.flac" \
#         --language 0:zh-TW --language 1:zh-CN --language 2:ja --language 3:en --language 4:ko "$demux_src_base/sup/000$demux_src_num.mks" \
#         --chapter-language en --chapters "$demux_src_base/chapter/00005_000$demux_src_num.txt" --track-order 0:0,1:0,2:0,2:1,2:2,2:3,2:4

#     echo -e "\n\nSrc Files:"
#     ls -hls "$demux_src_base/000$demux_src_num.flac"
#     ls -hls "$demux_src_base/sup/000$demux_src_num.mks"
#     ls -hls "$demux_src_base/chapter/00005_000$demux_src_num.txt"

#     # PSNR CHECK
#     $bin/vspipe -p rpc_test.vpy . | $bin/python3.11 qc2.py > rpc_$num.txt
#
#     # Move old files
#     mv $num.hevc rpc_$num.txt used/

done

# $bin/vspipe -c y4m enc.vpy - | $bin/x265-gcc15.1 --input - $param_01 --output "$i.hevc"
# # MKV MUX
# mkvmerge --output "01-test.mkv" --language 0:und "01-test.hevc" --language 0:ja "$base_path/demux/10924/00016.flac" \
#     --language 0:zh-TW --language 1:zh-CN --language 2:ja --language 3:en --language 4:ko "$base_path/demux/10924/sup/00016.mks" \
#     --chapter-language en --chapters "$base_path/demux/10924/chapter/00005_00016.txt" --track-order 0:0,1:0,2:0,2:1,2:2,2:3,2:4
#
# # PSNR CHECK
# $bin/vspipe -p rpc_test.vpy . | $bin/python3.11 qc2.py > rpc_test.txt
