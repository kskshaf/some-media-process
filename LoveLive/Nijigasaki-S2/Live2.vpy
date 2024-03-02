import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import ContraDering
import vsutil as vst
import fvsfunc as fvf
import xvs
import lvsfunc as lvf
from dfttest2 import DFTTest
core=vs.core
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\LLN S2\LLNijigasakiS2Vol2\BDROM\BDMV\STREAM\00011.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src32=mvf.Depth(src8,32)
#BM3DCPU
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[5,3],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,1.5],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
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
#Mix
mix16=db16[:9527]+db16_a[9527:9713]+db16[9713:9816]+db16_a[9816:9903]+db16[9903:9954]+db16_a[9954:10109]+db16[10109:10165]+db16_a[10165:10319]+db16[10319:10377]+db16_a[10377:10524]+db16[10524:10744]+db16_a[10744:11079]+db16[11079:94070]+db16_a[94070:109975]+db16[109975:177434]+db16_a[177434:191584]+db16[191584:]
#OKE:DEBUG
debug=1
if debug:
	src1 = mvf.ToRGB(src8,depth=8)
	src2 = mvf.ToRGB(mix16,depth=8)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(mix16,10)
res.set_output()
src8.set_output(1)