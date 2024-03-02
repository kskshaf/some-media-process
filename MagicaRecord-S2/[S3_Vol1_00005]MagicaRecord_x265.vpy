import vapoursynth as vs
import havsfunc as haf
import fvsfunc as fvf
import mvsfunc as mvf
import vsTAAmbk as taa
import vsutil
core = vs.core
#OKE:MEMORY
core.max_cache_size = 8000
#Deband_Loli
def Deband(de_src1,src2):
    nr8    = mvf.Depth(de_src1, depth=8)
    luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
    nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
    nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
    nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
    nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks,nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
    nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
    nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
    blur = haf.MinBlur(de_src1)
    db16 = core.f3kdb.Deband(blur,8,36,32,32,0,0,output_depth=16)
    db16 = core.f3kdb.Deband(db16,12,18,16,16,0,0,output_depth=16)
    db16 = mvf.LimitFilter(db16,blur,thr=0.6,thrc=0.5,elast=2.0)
    diff = core.std.MakeDiff(de_src1,blur)
    merge = core.std.MergeDiff(db16,diff)
    db16 = core.std.MaskedMerge(merge,src2,nrmask,first_plane=True)
    return db16
#OKE:INPUTFILE
a = r'F:\BDMV\Magica Record\S3 01\BDMV\STREAM\00005.m2ts'
src8 = core.lsmas.LWLibavSource(a)
src16 = mvf.Depth(src8,16)
#BM3D
get_y = vsutil.get_y(src16)
src_opp = mvf.ToRGB(src16).bm3d.RGB2OPP(1)
sigma = [1.0,0.8,0.8]
radius1 = 1
cpu = core.bm3dcpu.BM3D(src_opp, sigma=sigma, block_step=7, bm_range=7, radius=radius1, ps_num=2, ps_range=5, chroma=True).bm3d.VAggregate(radius1)
bm3d = mvf.ToYUV(core.bm3d.OPP2RGB(cpu),css='22',depth=16)
mask_w = core.std.Expr(haf.MinBlur(get_y).rgvs.RemoveGrain(20),["x 52428 > 65535 x 32768 < 0 x 2 pow 32768 2 pow - 65535 * 52428 2 pow 32768 2 pow - / ? ?"]).std.Maximum().std.Minimum()
bm3d = core.std.MaskedMerge(src16,bm3d,mask_w)
#AA
mask_e = core.tcanny.TCanny(get_y, sigma=1.3, mode=1, op=0)
mask_m = haf.MinBlur(mask_e).rgvs.RemoveGrain(20)
mask_k = core.std.Expr([mask_e,mask_m],["x y - abs"]).std.Binarize(6000).std.Maximum().std.Minimum()
aa16 = taa.TAAmbk(src16,aatype=1,mtype=2,postaa=True,aarepair=-20,cycle=1,stablize=2)
aa16 = core.std.MaskedMerge(bm3d, aa16, mask_k)
aa16 = Deband(bm3d,aa16)
#D_AA
dd16 = Deband(bm3d,bm3d)
####
out16 = fvf.rfs(aa16,dd16,"[35731 35995]")
#OKE:DEBUG
debug =1
if debug:
	src1 = mvf.ToRGB(src16,depth=8)
	src2 = mvf.ToRGB(out16,depth=8)
	compare = core.butteraugli.butteraugli(src1, src2)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(out16,10)
res.set_output()
src8.set_output(1)