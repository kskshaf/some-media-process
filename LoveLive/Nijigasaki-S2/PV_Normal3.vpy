import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
from ksksfunc import CropPart, DBMask, Deband, rescalef_aa, Sharp
import fvsfunc as fvf
import xvs
import zvs
core = vs.core
#OKE:MEMORY
core.max_cache_size=8000
#OKE:INPUTFILE
a=r'F:\BDMV\LL Nijigasaki S2D1\BDROM\BDMV\STREAM\00018.m2ts'
src8=core.lsmas.LWLibavSource(a)
src16=mvf.Depth(src8,16)
src32=mvf.Depth(src8,32)
#
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[4,4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,2],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
diff=core.std.MakeDiff(src16,bm3d)
#
rs16=rescalef_aa(bm3d,'Debicubic',h=800,b=1/3,c=1/3,mask_dif_pix=2.5,rsmode="znedi3",dering=True,mrad=1.2,mthr=115,csrange=1.2,not_aa=False,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,aacycle=2,dark=0.15,aamask=0)
rs16=haf.FineDehalo(rs16,brightstr=0.8,darkstr=0.4)
aa16=core.std.ShufflePlanes([rs16,bm3d],[0,1,2],vs.YUV)
#
aa16=fvf.rfs(aa16,bm3d,"[0 23] [352 407]")
#
preview0=src8
preview1=aa16
preview2=src8
preview3=aa16
#OKE:DEBUG
Debug=0
if Debug==1:
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	#preview2=preview2.resize.Bicubic(1280,720)
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
else:
	res=mvf.Depth(aa16,10)
res.set_output()
src8.set_output(1)