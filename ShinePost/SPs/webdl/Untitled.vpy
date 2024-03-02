from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import xvs,zvs
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'D:\Download\videoplayback.webm'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src8=src8[12572:72855]+src8[192548:478432]
src16=core.fmtc.bitdepth(src8,bits=16)
#
src16=haf.daa(src16)
src32=core.fmtc.bitdepth(src16,bits=32)
dft=DFTTest(src32,sigma=2.0,tbsize=3)
dhl=haf.FineDehalo(dft,brightstr=0.4,darkstr=0.0)
db=zvs.xdbcas(dhl,y=[48,36],cb=[36,24],cr=[36,24],mask=False,casstr=0.2)
## 199019-207130  242531-255950 # ? T=80?20?
#Trim(12572,72854)+Trim(192548,478431)
preview0=src8
preview1=db
preview2=src8.resize.Bicubic(1600,900)
preview3=src16
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
	res=mvf.Depth(db,10)
res.set_output()
src8.set_output(1)

