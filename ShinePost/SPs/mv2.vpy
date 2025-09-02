import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import vsTAAmbk as taa
import xvs,zvs
import fvsfunc as fvf
import nnedi3_resample as nnrs
from ksksfunc import MRcoref
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=8600
a=r'/run/media/ksks/Others/ShinePost/[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]/SHINEPOST_BOX1_DISC2/BDMV/STREAM/00014.m2ts'
src8=core.lsmas.LWLibavSource(a)
src16=core.fmtc.bitdepth(src8,bits=16)
src_o=src16
# cut down the fucking border
src_c=core.std.CropRel(src16,2,2,2,2)
src_c_y=core.std.ShufflePlanes(src_c,0,vs.GRAY)
src_f_y=core.edgefixer.Continuity(src_c_y, 2,2,2,2)
blk_m=core.std.BlankClip(src_c_y).std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535)
src_f_y=core.std.MaskedMerge(src_c_y, src_f_y, blk_m)
src_c=core.std.ShufflePlanes([src_f_y, src_c],[0,1,2],vs.YUV)
#
src32=core.fmtc.bitdepth(src_c,bits=32)
#Denoise
tms=DFTTest(src32,sigma=8,tbsize=3)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[4,2.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,1.1],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
# Dehalo & Dering
bm3d_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
dehalo=haf.FineDehalo(bm3d_y,thlimi=80,thlima=160,brightstr=0.8,darkstr=0)
dr_diff=core.std.MakeDiff(bm3d_y, dehalo)
dering=haf.HQDeringmod(dehalo,mrad=1,msmooth=1,mthr=58,minp=1,sharp=1,thr=2.0,elast=1.8)
dering=haf.EdgeCleaner(dering,strength=8,rmode=20)
# AA
aa=taa.TAAmbk(dering,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,cycle=1,thin=0,dark=0.15)
aa_md=core.std.MergeDiff(aa, dr_diff)
#aa=core.std.ShufflePlanes([aa,bm3d],[0,1,2],vs.YUV)
aa_md=core.std.ShufflePlanes([aa_md,bm3d],[0,1,2],vs.YUV)
# Deband
db1=zvs.xdbcas(aa_md,y=[48,36],cb=[36,32],cr=[36,32],mask=True,limit=[0.8,0.5,2.88],casstr=0.1)
db1=nnrs.nnedi3_resample(db1,1920,1080,nsize=3,qual=2,mode='znedi3',csp=vs.YUV420P10)

db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,limit=[0.8,0.5,2.88],casstr=0.1)
db2=nnrs.nnedi3_resample(db2,1920,1080,nsize=3,qual=2,mode='znedi3',csp=vs.YUV420P10)

staff=mvf.Depth(src8,10)

out=fvf.rfs(db1,db2,"[0 95] [1116 1122] [1230 1235] [1341 1348] [1482 1495] [1638 1655] [3220 3335]")
out=out[:3336]+staff[3336:]

out.set_output()
src_c.resize.Spline16(1920,1080).set_output(1)
src_o.set_output(2)
