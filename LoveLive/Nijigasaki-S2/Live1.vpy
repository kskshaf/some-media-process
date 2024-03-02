import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import ContraDering
import vsutil as vst
import fvsfunc as fvf
import xvs
import lvsfunc as lvf
#import zvs
from dfttest2 import DFTTest
core=vs.core
#OKE:MEMORY
core.max_cache_size=11000
#BM3D
#OKE:INPUTFILE
a=r'F:\BDMV\LL Nijigasaki S2D1\BDROM\BDMV\STREAM\00011.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)#[210250:210351]#[109450:116650]
#src16=mvf.Depth(src8,16)
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
dring=ContraDering(bm3d,ecstrength=15,ecrmode=18,conn=[1,2,1,2,4,2,1,2,1],mrad=1.0,mthr=115,csrange=1.0,rpmode=23)
#mask_r=haf.HQDeringmod(bm3d,show=True,mrad=1.0,mthr=115)
db16_a=core.neo_f3kdb.Deband(dring,10,48,32,32,0,0,sample_mode=4)
db16_a=mvf.LimitFilter(db16_a,dring,thr=0.6,thrc=0.5,elast=2.0)
dbm_a=lvf.mask.detail_mask(dring,brz_a=0.025,brz_b=0.045)
db16_a=core.std.MaskedMerge(db16_a,dring,dbm_a)
#
mix16=db16[:9138]+db16_a[9138:9350]+db16[9350:9630]+db16_a[9630:9746]+db16[9746:9807]+db16_a[9807:9865]+db16[9865:10137]+db16_a[10137:10226]+db16[10226:90321]+db16_a[90321:109373]+db16[109373:155748]+db16_a[155748:180898]+db16[180898:]
#Mix
preview0=src8
preview1=mix16
preview2=src8
preview3=db16
#[609 1048] [1155 1269] [1323 1376] [1442 1482] [1540 1595] [1655 1806]
##[1377 1441] 
#output=mix16
#OKE:DEBUG
Debug=0
if Debug==1:
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
else:
	res=mvf.Depth(mix16,10)
res.set_output()
src8.set_output(1)