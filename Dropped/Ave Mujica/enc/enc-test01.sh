#!/usr/bin/bash
set -euo pipefail

export PATH="/home/rip/ripenv/bin:$PATH"
export PYTHONUSERBASE="/home/rip/ripenv"
export LD_LIBRARY_PATH="/home/rip/ripenv/lib:/home/rip/ripenv/lib/vapoursynth"
export bin="/home/rip/ripenv/bin"

export param_01="--y4m -D 10 --preset slower --ctu 32 --crf 15.0 --qg-size 32 --tu-inter-depth 1 --tu-intra-depth 1 --max-tu-size 32 --deblock -1:-1 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --no-sao --me 3 --subme 5 --merange 57 --limit-tu 0 --b-intra --no-rect --no-amp --ref 5 --weightb --keyint 240 --min-keyint 1 --bframes 8 --aq-mode 1 --aq-strength 0.90 --rd 5 --psy-rd 2.0 --psy-rdoq 1.0 --rdoq-level 2 --frame-threads 1 --no-open-gop --rc-lookahead 80 --scenecut 40 --qcomp 0.65 --no-strong-intra-smoothing --colorprim bt709 --transfer bt709 --colormatrix bt709"

export base_path="/mnt/Disk/BD"
cd $base_path/enc


$bin/vspipe -c y4m 01-test.vpy - | $bin/x265-gcc15.1 --input - $param_01 --output "01-test.hevc"
# MKV MUX
mkvmerge --output "01-test.mkv" --language 0:und "01-test.hevc" --language 0:ja "$base_path/demux/10924/00016.flac" \
    --language 0:zh-TW --language 1:zh-CN --language 2:ja --language 3:en --language 4:ko "$base_path/demux/10924/sup/00016.mks" \
    --chapter-language en --chapters "$base_path/demux/10924/chapter/00005_00016.txt" --track-order 0:0,1:0,2:0,2:1,2:2,2:3,2:4

# PSNR CHECK
$bin/vspipe -p rpc_test.vpy . | $bin/python3.11 qc2.py > rpc_test.txt

