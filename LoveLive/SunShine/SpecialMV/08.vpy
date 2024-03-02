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
src8=core.lsmas.LWLibavSource(a,repeat=True)[55120:61571]
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
fm=core.tivtc.TFM(src8,order=1,mode=3,cthresh=6)
deint=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=2)
src8=mvf.FilterCombed(fm,deint)
src8=core.tivtc.TDecimate(src8)
src8=core.std.SetFieldBased(src8,0)
#
src32=core.fmtc.bitdepth(src8,bits=32)
dft=DFTTest(src32,sigma=2,tbsize=3)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,dft,sigma=[3,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.4,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5)
db=zvs.xdbcas(bm3d,y=[36,24],cb=[24,16],cr=[24,16],mask=True,casstr=0)
db=haf.EdgeCleaner(db,strength=20,rmode=20)
#part2
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b2=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.8],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d2=core.bm3dcpu.BM3Dv2(src32,bm3d_b2,sigma=[1.0,0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5)
db2=zvs.xdbcas(bm3d2,mask=True,casstr=0.3)
out=db[:5051]+db2[5051:]
#
preview0=src8
preview1=out #1
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
	res=mvf.Depth(out,10)
res.set_output()
src8.set_output(1)