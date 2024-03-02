from vapoursynth import core
import vapoursynth as vs
import mvsfunc as mvf
import zvs
from ksksfunc import MRcoref
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 1\BDMV\STREAM\00000.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[2.0,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.0,0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Deband
db1=zvs.xdbcas(bm3d,casstr=0)
db1=mvf.Depth(db1,10)
#
preview0=src8
preview1=db1
preview2=src8
preview3=db1
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=src8
else:
	res=db1
res.set_output()
src8.set_output(1)

