import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import ContraDering
import adptvgrnMod as adp
import vsutil as vst
import fvsfunc as fvf
import xvs
import lvsfunc as lvf
from dfttest2 import DFTTest
core=vs.core
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\LLN S2\Love.Live.Nijigasaki.School.Idol.Doukoukai.S2.Vol3.2022.COMPLETE.BLURAY-KoushinRip\BDROM\BDMV\STREAM\00010.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src32=mvf.Depth(src8,32)
#BM3DCPU
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[5,3],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,1.5],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
diff=core.std.MakeDiff(src32.fmtc.bitdepth(bits=16),bm3d)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.4,brightstr=0.4)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
#Deband for Live
db16=core.neo_f3kdb.Deband(dhaf,15,60,48,48,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
#Anime
dring=haf.FineDehalo(bm3d,brightstr=0.4,darkstr=0.4)
dring=core.std.MaskedMerge(bm3d,dring,halos)
db16_a=core.neo_f3kdb.Deband(dring,10,48,32,32,0,0,sample_mode=4)
db16_a=mvf.LimitFilter(db16_a,dring,thr=0.6,thrc=0.5,elast=2.0)
dbm_a=lvf.mask.detail_mask(dring,brz_a=0.025,brz_b=0.045)
db16_a=core.std.MaskedMerge(db16_a,dring,dbm_a)
snoise=adp.adptvgrnMod(db16_a,strength=0.90,size=1.2,sharp=120,static=False,luma_scaling=6,grain_chroma=0)
#Mix
mix16=fvf.rfs(db16,db16_a,"[8896 8978] [9088 9143] [9391 9479] [9549 9827] [9872 9930] [9970 10022] [10066 10457] [118170 130938] [219435 235408]")
mix16=fvf.rfs(mix16,snoise,"[124726 126773] [127423 130938] [219622 228445] [235158 235408]")
#
preview0=src8
preview1=snoise
preview2=src8
preview3=db16
#OKE:DEBUG
Debug=0
if Debug==1:
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	#preview2=preview2.resize.Bicubic(1280,720)
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
else:
	res=mvf.Depth(mix16,10)
res.set_output()
src8.set_output(1)