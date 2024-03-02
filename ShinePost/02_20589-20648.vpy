from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import vsTAAmbk as taa
import fvsfunc as fvf
from ksksfunc import MRcoref
from rekt import rekt
import xvs,zvs
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\ShinePost\[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]\SHINEPOST_BOX1_DISC1\BDMV\STREAM\00016.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0)

preview0=src16#.std.ShufflePlanes(0,vs.GRAY)
preview1=db2 #rs_mask
preview2=src16
preview3=db2
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	src1=mvf.ToRGB(preview0,depth=8)#[n]
	src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=src8
else:
	res=mvf.Depth(db2,10)[20589:20649]
res.set_output()
src8[20589:20649].set_output(1)