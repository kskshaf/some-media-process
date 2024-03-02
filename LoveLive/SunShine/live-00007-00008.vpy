from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import lvsfunc as lvf
from dfttest2 import DFTTest
#MEMORY
core.max_cache_size=11000
#INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00007.m2ts'
b=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00008.m2ts'
#Source A
srca=core.lsmas.LWLibavSource(a,repeat=True)
#[119230:119730] #fucking mistakes.
srca_d=core.std.SeparateFields(srca,True)
srca_d=core.std.DoubleWeave(srca_d,True)[1::2]
#Source B
srcb=core.lsmas.LWLibavSource(b,repeat=True)
src8=srca[:119230]+srca_d[119230:119730]+srca[119730:]+srcb
#
source=src8.std.SetFieldBased(0)
src8=core.edgefixer.Continuity(src8,top=2,left=2,right=2,radius=24)
blur=core.std.BoxBlur(src8,planes=0,hradius=1,vradius=2,vpasses=1)
src8=core.edgefixer.Reference(src8,blur,top=2,left=4,right=4,radius=24)
src8=haf.daa(src8)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
src32=src8.fmtc.bitdepth(bits=32)
#Denoise
mvd=zvs.zmdg(src16,tr=2,thsad=210,truemotion=False,thscd1=280,limit=300,cs=True)
cb=DFTTest(mvd,sigma=5,tbsize=5)
cb32=cb.fmtc.bitdepth(bits=32)
mvd=mvd.fmtc.bitdepth(bits=32)
bm3d_b=core.bm3dcpu.BM3Dv2(mvd,cb32,sigma=[4,2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(mvd,bm3d_b,sigma=[2,1],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.4,brightstr=0.1)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
dhaf=haf.EdgeCleaner(dhaf,strength=20,rmode=20)
#Deband for Live
db16=core.neo_f3kdb.Deband(dhaf,15,60,48,48,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
#
preview0=src8
preview1=db16
preview2=source
preview3=bm3d
#OKE:DEBUG
Debug=0
if Debug==1:
	n=145224
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	#src1=mvf.ToRGB(preview0,depth=8)#[n]
	#src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=db16
else:
	res=mvf.Depth(db16,10)
res.set_output()
source.set_output(1)

