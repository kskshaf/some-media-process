from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import vsTAAmbk as taa
import fvsfunc as fvf
from ksksfunc import MRcoref
from rekt import rekt
import xvs,zvs
#OKE:MEMORY
core.max_cache_size=10000
#OKE:INPUTFILE
a=r"/run/media/ksks/Others/ShinePost/[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]/SHINEPOST_BOX2_DISC2/BDMV/STREAM/00017.m2ts"
#a=r"/run/media/ksks/Others/BD/ShinePost/enc/12.hevc"
src8=core.lsmas.LWLibavSource(a,repeat=True)#[30691:]
#src_i=core.text.ClipInfo(src8)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Descale mask.
bm3d_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
rs_mask=MRcoref(bm3d_y,'Delanczos',h=870,mask_dif_pix=2.6,mthr=[6,5],show='mask',blur_mask=True,aa_m=False,dering=0,dehalo=0)
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

db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=False,limit=[0.6,0.4,3],casstr=0)
#[30691:]
res= mvf.Depth(db1,10)[30691:30884] +  mvf.Depth(db2,10)[30884:]
res.set_output()
src8[30691:].set_output(1)
#src_i.set_output(2)
