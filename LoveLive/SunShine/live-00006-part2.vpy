from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import muvsfunc as muf
import lvsfunc as lvf
import vsTAAmbk as taa
from dfttest2 import DFTTest
#FixBorder
def fixborder(clip):
    fbr=core.std.CropRel(clip,bottom=4)
    fbr=core.edgefixer.Continuity(fbr,top=2,left=5,right=5,radius=24)
    blur1=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur1,left=8,right=8,radius=24)
    fbr=core.std.AddBorders(fbr,bottom=4)
    fbr=core.fb.FillBorders(fbr,bottom=4,interlaced=False,mode='fillmargins')
    blur=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=4,radius=8)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=6,radius=24)
    return fbr
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00006.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
#FixBorder&Denoise
fb=fixborder(src16)
fb=haf.daa(fb)
fb32=fb.fmtc.bitdepth(bits=32)
cb=DFTTest(fb32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(fb32,cb,sigma=[3,1.6],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(fb32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#AA&Dering
aa16=taa.TAAmbk(bm3d.std.ShufflePlanes(0,vs.GRAY),aatype=-3,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=2,cycle=5)
halo_f=muf.mdering(aa16,thr=2)
dhaf=core.std.ShufflePlanes([halo_f,bm3d],[0,1,2],vs.YUV)
#Deband
db1=zvs.xdbcas(fb,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0)
db1=mvf.Depth(db1,10) #direct output.
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0)
db2=mvf.Depth(db2,10) #denoise output.
db4=zvs.xdbcas(haf.daa(bm3d),y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0)
db4=mvf.Depth(db4,10) #denoise output.
db3=zvs.xdbcas(dhaf,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0)
db3=mvf.Depth(db3,10) ###
#
out=db1[152021:152224]+db3[152224:152899]+db2[152899:153024]+db4[153024:153085]
#part2 [152021:153085]
#
out.set_output()
src8[152021:153085].set_output(1)

