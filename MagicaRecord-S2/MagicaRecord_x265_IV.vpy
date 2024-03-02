import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import vsutil
import fvsfunc as fvf
core = vs.core
#BM3D
def BM3DCPU(clip,sigma,radius1,block_step,bm_range,ps_num,ps_range):
	src_opp = mvf.ToRGB(clip).bm3d.RGB2OPP(1)
	cpu = core.bm3dcpu.BM3Dv2(src_opp,src_opp, sigma=sigma, block_step=block_step, bm_range=bm_range, radius=radius1, ps_num=ps_num, ps_range=ps_range, chroma=True)
	bm3d = mvf.ToYUV(core.bm3d.OPP2RGB(cpu),css='22',depth=16)
	return bm3d
#OKE:MEMORY
core.max_cache_size = 8000
#OKE:INPUTFILE
a = r'F:\BDMV\Magica Record\S2 02\BDMV\STREAM\00005.m2ts'
src8 = core.lsmas.LWLibavSource(a)
src16 = mvf.Depth(src8,16)
#########################IV#########################
#Kukoc@SkyeySnow(https://skyeysnow.com/forum.php?mod=viewthread&tid=32004)
#get_y = vsutil.get_y(src16)
dftt = core.dfttest.DFTTest(src16,sigma=12,planes=[0,1,2])
dftt = haf.MinBlur(dftt,2)
mask = core.tcanny.TCanny(vsutil.get_y(dftt),t_h=1.6, t_l=1.55, op=1).std.Maximum().std.Maximum().std.Minimum().std.Inflate()
smd = haf.SMDegrain(src16,tr=2,thSAD=300,RefineMotion=True,subpixel=3,prefilter=3)
knlm = core.knlm.KNLMeansCL(src16, d=1, a=2, s=4, h=1.5)
smd_knlm = core.std.MaskedMerge(smd,knlm,mask)
bm3d = BM3DCPU(smd_knlm,[3.0,1.0],radius1=2,block_step=6,bm_range=12,ps_num=2,ps_range=5)
skb = core.std.MaskedMerge(smd_knlm,bm3d,mask)
#Dehalo
hlmask_b = haf.FineDehalo(vsutil.get_y(skb), showmask=4)
mask_outer_b = vsutil.iterate(hlmask_b,core.std.Maximum,2).std.Inflate()
mask_inner_b = vsutil.iterate(mask_outer_b,core.std.Minimum,3)
halos_b = core.std.Expr([mask_outer_b,mask_inner_b],'x y -')
dehalo_b = haf.DeHalo_alpha(skb,rx=2.0,ry=2.0,darkstr=0.6)
dehalo = core.std.MaskedMerge(skb,dehalo_b,halos_b) 
srcb = core.rgvs.Repair(dehalo,skb,23)
srcb = mvf.LimitFilter(srcb,dehalo,thr=1.2,thrc=1.0,elast=25)
db16 = core.f3kdb.Deband(srcb,10,48,32,32,0,0,output_depth=16)
db16 = core.f3kdb.Deband(db16,12,24,16,16,0,0,output_depth=16)
ivpart = mvf.LimitFilter(db16,srcb,thr=1.0,thrc=0.8,elast=3.0)
#########################Anime#########################
#BM3D
bm3d_a = BM3DCPU(src16,sigma=[1.0,0.8,0.8],radius1=1,block_step=7,bm_range=7,ps_num=2,ps_range=5)
#Deband
nr8    = mvf.Depth(bm3d_a, depth=8)
luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks,nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
blur = haf.MinBlur(bm3d_a)
db16_a = core.f3kdb.Deband(blur,8,36,32,32,0,0,output_depth=16)
db16_a = core.f3kdb.Deband(db16_a,12,18,16,16,0,0,output_depth=16)
db16_a = mvf.LimitFilter(db16_a,blur,thr=0.6,thrc=0.5,elast=2.5)
diff = core.std.MakeDiff(bm3d_a,blur)
merge = core.std.MergeDiff(db16_a,diff)
ampart = core.std.MaskedMerge(merge,bm3d_a,nrmask,first_plane=True)
#########################SP#########################
bm3d_s = BM3DCPU(src16,sigma=[1.6,1.0,1.0],radius1=1,block_step=6,bm_range=8,ps_num=2,ps_range=5)
db16_s = core.f3kdb.Deband(bm3d_s,8,18,16,16,0,0,output_depth=16)
sppart = mvf.LimitFilter(db16_s,bm3d_s,thr=1.0,thrc=0.8,elast=3.0)
#########################Final#########################
out16 = fvf.rfs(ivpart,ampart,"[687 2338] [3136 3708] [5771 6176] [7770 7965] [8782 9591] [11565 12159] [12348 12726] [18384 18700] [18808 19117] [19508 19929] [21511 21679] [21924 22143] [26063 26200] [26326 26623] [30338 32504] [33624 34069]")
out16 = fvf.rfs(out16,sppart,"[26201 26325] [26624 28952]")
#OKE:DEBUG
debug =0
if debug:
	src1 = mvf.ToRGB(src16,depth=8)
	src2 = mvf.ToRGB(out16,depth=8)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(out16,10)
res.set_output()
src8.set_output(1)