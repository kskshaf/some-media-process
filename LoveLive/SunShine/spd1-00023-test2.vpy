from vapoursynth import core
import vapoursynth as vs
import pathlib
import vsTAAmbk as taa
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import muvsfunc as muf
from dfttest2 import DFTTest
#
def wtf(clip):
    src32=core.fmtc.bitdepth(clip,bits=32)
    cb=DFTTest(src32,sigma=3,tbsize=3)
    bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
    bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,1.2],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
    halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
    mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
    mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
    halos=core.std.Expr([mask_outer,mask_inner],'x y -')
    dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.8,brightstr=0.0)
    dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
    db1=core.neo_f3kdb.Deband(dhaf,8,36,24,24,0,0,sample_mode=4)
    db1=core.neo_f3kdb.Deband(db1,15,48,36,36,0,0,sample_mode=4)
    return db1
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 1\BDMV\STREAM\00023.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
source=src8
ca=wtf(src8)
cb=mvf.Depth(src8,16)
res=ca[:100]+cb[100:]

res.set_output()
src8.set_output(1)

