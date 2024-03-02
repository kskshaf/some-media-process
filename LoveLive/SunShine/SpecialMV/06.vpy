import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
import vsTAAmbk as taa
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=9000
#OKE:INPUTFILE
a=r'E:\BD\MV\BDROM\BDMV\STREAM\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)[39178:46530]
src8=core.std.SetFieldBased(src8,0)
#
db=zvs.xdbcas(src8,mask=True,casstr=0)
#
preview0=src8
preview1=db #1
preview2=db #2
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
	res=mvf.Depth(db,10)
res.set_output()
src8.set_output(1)