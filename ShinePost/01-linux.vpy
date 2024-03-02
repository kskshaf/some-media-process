from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import vsTAAmbk as taa
import fvsfunc as fvf
from ksksfunc import MRcoref
import xvs,zvs
core.max_cache_size=9600

a=r'/run/media/ksks/Others/ShinePost/[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]/SHINEPOST_BOX1_DISC1/BDMV/STREAM/00002.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
bm3d_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
# Dehalo & Dering
dehalo=haf.FineDehalo(bm3d_y,thlimi=80,thlima=160,brightstr=0.5,darkstr=0)
dering=haf.HQDeringmod(dehalo,mrad=1,msmooth=1,mthr=58,minp=1,sharp=1,thr=2.8,elast=2.0)
dering=haf.EdgeCleaner(dering,strength=10,rmode=20)
# AA
aa=taa.TAAmbk(dering,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stablize=2,cycle=1,thin=0,dark=0.15)
aa=core.std.ShufflePlanes([aa,bm3d],[0,1,2],vs.YUV)
# Deband & Sharpen
db1=zvs.xdbcas(aa,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0.1)
db1_y=db1.std.ShufflePlanes(0,vs.GRAY)
blur=haf.MinBlur(db1_y,1)
diff=core.std.MakeDiff(db1_y,blur)
eh=xvs.mwenhance(diff,Strength=1.4,useExpr=True)
merge=core.std.MergeDiff(blur,eh)
cln=haf.EdgeCleaner(merge,strength=16,rmode=20)
cln=haf.FineDehalo(cln,thlimi=80,thlima=160,brightstr=0.4,darkstr=0)
db1=core.std.ShufflePlanes([cln,db1],[0,1,2],vs.YUV)
###
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0.20)
db=fvf.rfs(db1,db2,"[74 142]")
#74-142 12931

preview0=src16
preview1=db
preview2=src16
preview3=db
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
