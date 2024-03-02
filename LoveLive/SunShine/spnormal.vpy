from vapoursynth import core
import vapoursynth as vs
import vsTAAmbk as taa
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 1\BDMV\STREAM\00036.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
#source=src8
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
#fm=core.tivtc.TFM(src8,order=1,mode=5,cthresh=2)
#deint=haf.QTGMC(src8,Preset="Slow",TFF=True,FPSDivisor=2)
#src8=mvf.FilterCombed(fm,deint)
#src8=core.std.SetFieldBased(src8,0)
#src8=taa.daa(src8,1)
#src8=haf.daa(src8)
src8=haf.QTGMC(src8,Preset="Slow",TFF=True,FPSDivisor=2)
src8=core.std.SetFieldBased(src8,0)
#
src32=core.fmtc.bitdepth(src8,bits=32)
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[6,3],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[3,1.5],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.4,brightstr=0.4)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
#
db=core.neo_f3kdb.Deband(dhaf,8,36,24,24,0,0,sample_mode=4)
db=core.neo_f3kdb.Deband(db,15,48,36,36,0,0,sample_mode=4)
#db=db[56854:56928]
#
preview0=src8
preview1=db
preview2=src8#.resize.Bicubic(960,540)
preview3=db
#OKE:DEBUG
Debug=1
if Debug==1:
	n=1372
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
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

