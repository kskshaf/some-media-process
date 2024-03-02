import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
import fvsfunc as fvf
from ksksfunc import MRcoref
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=8600
a=r'/run/media/ksks/Others/ShinePost/[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]/SHINEPOST_BOX1_DISC2/BDMV/STREAM/00013.m2ts'
src8=core.lsmas.LWLibavSource(a)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=DFTTest(src32,sigma=8,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[4.5,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
# Descale & AA
bm3d_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
rs_a=MRcoref(bm3d_y,'Debicubic',b=0.50,c=0.50,h=810,mask_dif_pix=2.5,mthr=[4,3],blur_mask=True,aa_m=2,dering=1,dehalo=2,brightstr=0.65)
rs_a=core.std.ShufflePlanes([rs_a,bm3d],[0,1,2],vs.YUV)
rs_a=haf.EdgeCleaner(rs_a,strength=10,rmode=20)
# Deband
db1=zvs.xdbcas(rs_a,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0)
db1=mvf.Depth(db1,10)
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0)
db2=mvf.Depth(db2,10)
out=fvf.rfs(db1,db2,"[443 529] [779 843]")

out.set_output()
src8.set_output(1)
mvf.ToRGB(src16,depth=8).set_output(2)
