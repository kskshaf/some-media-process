import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
import vsTAAmbk as taa
import fvsfunc as fvf
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=9000
#OKE:INPUTFILE
a=r'E:\BD\MV\BDROM\BDMV\STREAM\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)[61633:69231]
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
fm=core.tivtc.TFM(src8,order=1,mode=3,cthresh=6)
deint=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=2)
src8=mvf.FilterCombed(fm,deint)
src8=core.tivtc.TDecimate(src8)
src8=core.std.SetFieldBased(src8,0)
#
out=zvs.xdbcas(src8,casstr=0,mask=True)
#
preview0=src8
preview1=out #1
preview2=out #2
preview3=src8 #3
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1868
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	#src1=mvf.ToRGB(preview0,depth=8)#[n]
	#src2=mvf.ToRGB(preview1,depth=8)#[n]
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=db
else:
	res=mvf.Depth(out,10)
res.set_output()
src8.set_output(1)