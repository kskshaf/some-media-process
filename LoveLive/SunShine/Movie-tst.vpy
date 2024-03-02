from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import MRcoref
import xvs,zvs
from dfttest2 import DFTTest
import nnedi3_resample as nnrs
#
def crossfademod(clipa,clipb,start,end):
    import kagefunc as kgf
    fd=kgf.crossfade(clipa[start:end+3],clipb[start:end+3],end-start+2)
    fade=clipa[:start]+fd[:-3]+clipb[end+1:]
    return fade
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'E:\BD\LoveLiveSunshine\F_\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\Disc 7\00004.m2ts.hevc'
#a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 7\BDMV\STREAM\00004.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src8=core.text.ClipInfo(src8)

preview0=src8 #[384:601]
preview1=src8 #[:217]
preview2=src8
preview3=src8
#OKE:DEBUG
Debug=2
if Debug==1:
	n=1372
	#src1=zvs.n3pv(preview0,scale=1)#[n]
	#src2=zvs.n3pv(preview1,scale=1)#[n]
	src1=mvf.ToRGB(preview0,depth=8)#[n]
	src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	#src8=src8[1456]+src8[2656]+src8[3564]+src8[6666]
	res=nnrs.nnedi3_resample(src8,mode='znedi3',csp=vs.RGB24)
	#res=core.imwri.Write(res,imgformat="PNG",filename="E:\\A\\apours%04d.png",firstnum=0,quality=0,overwrite=True)
else:
	res=out10
res.set_output()
src8.set_output(1)