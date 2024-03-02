import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import fvsfunc as fvf
import xvs
import lvsfunc as lvf
import vsTAAmbk as taa
#import zvs
from dfttest2 import DFTTest
core=vs.core
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\LLN S2\Love.Live.Nijigasaki.Gakuen.School.Idol.Doukoukai.S2.Vol7.2022.COMPLETE.BLURAY-KoushinRip\BDROM\BDMV\STREAM\00007.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src=haf.QTGMC(src8,TFF=True,Preset="slower",Border=True,FPSDivisor=2,ShutterBlur=2)
src=haf.FineDehalo(src,brightstr=0.8,darkstr=0.4)
src32=mvf.Depth(src,32)
#BM3DCPU
bm3d_b=core.bm3dcpu.BM3Dv2(src32,src32,sigma=[3,2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,1],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Deband
dhaf=bm3d
db16=core.neo_f3kdb.Deband(dhaf,15,48,36,36,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
#
preview0=src8
preview1=db16
preview2=src8
preview3=db16
#OKE:DEBUG
Debug=0
if Debug==1:
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
else:
	res=mvf.Depth(db16,10)
res.set_output()
src8.set_output(1)