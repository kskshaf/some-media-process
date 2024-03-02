from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import zvs
import vsutil as vst
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC2\BDMV\STREAM\00012.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=haf.daa(src8)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
cb=DFTTest(src32,sigma=18,tbsize=3)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[6,3],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(cb,bm3d_b,sigma=[3,1.5],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.4,brightstr=0.1)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
dhaf=haf.EdgeCleaner(dhaf,strength=20,rmode=20)
db=zvs.xdbcas(dhaf,y=[36,24],cb=[24,16],cr=[24,16],mask=False,casstr=0,limit=[0.8,0.5,3])


preview0=src16
preview1=db
preview2=src8
preview3=src8
#OKE:DEBUG
Debug=1
if Debug==1:
	#n=1372
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
src16.set_output(1)

