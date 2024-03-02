from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import muvsfunc as muf
import lvsfunc as lvf
from dfttest2 import DFTTest
#FixBorder
def fixborder(clip):
    fbr=core.std.CropRel(clip,bottom=4)
    fbr=core.edgefixer.Continuity(fbr,top=6,left=5,right=5,radius=24)
    blur1=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur1,left=8,right=8,radius=24)
    fbr=core.std.AddBorders(fbr,bottom=4)
    fbr=core.fb.FillBorders(fbr,bottom=4,interlaced=False,mode='fillmargins')
    blur=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=4,radius=8)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=6,radius=24)
    return fbr
#
def nto24p(number):
    return int(number*4/5)
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00006.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.tivtc.TDecimate(src8)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
src32=src8.fmtc.bitdepth(bits=32)
#FixBorder&Denoise&daa
fb=fixborder(src16)
fb=haf.daa(fb)
fb32=fb.fmtc.bitdepth(bits=32)
cb=DFTTest(fb32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(fb32,cb,sigma=[5,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(fb32,bm3d_b,sigma=[2.5,1.2],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.6,brightstr=0.2)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
#Deband
db16=core.neo_f3kdb.Deband(dhaf,15,60,48,48,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
out=mvf.Depth(db16,10)
out=out[nto24p(153302):nto24p(162794)]
#part4 [153302:162794] #24p
#
out.set_output()
src8[nto24p(153302):nto24p(162794)].set_output(1)

