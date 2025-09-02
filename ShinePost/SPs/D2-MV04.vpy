from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import zvs
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC2\BDMV\STREAM\00011.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
dhl=haf.EdgeCleaner(src16,strength=2,rmode=20)
aa=taa.TAAmbk(dhl,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,cycle=0)
aa=zvs.xdbcas(aa,mask=True,casstr=0)

preview0=src16
preview1=aa
preview2=src8
preview3=src8
#OKE:DEBUG
Debug=1
if Debug==1:
	#n=1372
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
	res=mvf.Depth(aa,10)
res.set_output()
src16.set_output(1)

