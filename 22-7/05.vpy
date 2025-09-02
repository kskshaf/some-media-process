import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import adptvgrnMod as adp
import vsTAAmbk as taa
import vsutil
import ksksfunc as ksf
import fvsfunc as fvf
import kagefunc as kgf
import xvs
core = vs.core
#OKE:MEMORY
core.max_cache_size=10500
#ksf.ADN(input,sigma,radius1,block_step,bm_range,ps_num,ps_range,x1=52428,y1=65535,x2=32678,y2=1200)
#NormalDeband
def Deband(denoised,nrmask,range1=6,range2=10,y1=48,c1=36,r1=36,y2=36,c2=24,r2=24,thr=0.6,thrc=0.5,elast=2.0,first_plane=True):
    deband=core.f3kdb.Deband(denoised,range1,y1,c1,r1,0,0)
    deband=core.f3kdb.Deband(deband,range2,y2,c2,r2,0,0)
    deband=mvf.LimitFilter(deband,denoised,thr=thr,thrc=thrc,elast=elast)
    deband=core.std.MaskedMerge(deband,denoised,nrmask,first_plane)
    return deband
#DebandMask(LoliHouse)
def DBMask(clip):
    nr8=mvf.Depth(clip,8)
    luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
    nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).akarin.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
    nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
    nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
    nrmask  = core.akarin.Expr([nrmaskg,nrmaskb,nrmasks,nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
    nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
    nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
    return nrmask
#AdaptiveSharp(TCanny&MinBlur)
def Sharp(src_nos,strength=1,sigma=1,t_h=12,t_l=2.5,mode=1,op=1):
#src_nos=deband
    edge=core.tcanny.TCanny(ksf.Y(src_nos),sigma=sigma,t_h=t_h,t_l=t_l,mode=mode,op=op).std.Maximum().std.Minimum().std.Maximum()
    edge=haf.MinBlur(edge,1)
    mmd_s=core.std.MergeDiff(src_nos,core.std.MakeDiff(src_nos,haf.MinBlur(src_nos,strength)))
    sharp=core.std.MaskedMerge(mmd_s,src_nos,edge)
    return sharp
#OKE:INPUTFILE
a=r"E:\BD\[210714] ｢11という名の永遠の素数｣／22／7 [完全生産限定盤C] (flac)\SRCL-11790\BDMV\STREAM\00005.m2ts"
src8=core.lsmas.LWLibavSource(a)
#Fix Overflow
#level_y=core.std.Levels(src8,min_in=0,max_in=255,gamma=1.0,min_out=16,max_out=235,planes=[0])
#level_uv=core.std.Levels(src8, min_in=0, max_in=255, gamma=1.0,min_out=16, max_out=240, planes=[1,2])
#level=core.std.ShufflePlanes([level_y,level_uv],[0,1,2],vs.YUV)
#src8=fvf.rfs(src8,level,"[82 708] [1089 1249] [1587 1609] [1678 1705] [1783 1815]")
src16=mvf.Depth(src8,16)
#BM3D&xvs_rescale
bm3d=ksf.BM3DCPU(src8,[1.6,1.2],radius1=1,block_step=8,bm_range=8,ps_num=2,ps_range=5)
diff=core.std.MakeDiff(src16,bm3d)
rs16=xvs.rescalef(bm3d,"Debicubic",b=0,c=1/3,h=900)
#Deband Mask
nrmask=DBMask(bm3d)
nrmask=ksf.Y(nrmask)
#RS&DB&NonAA
rsnd=Deband(rs16,nrmask,range1=8,range2=12,y1=36,c1=24,r1=24,y2=24,c2=16,r2=16,thr=0.6,thrc=0.5,elast=2.8,first_plane=False)
rsnd=core.std.MergeDiff(rsnd,diff)
rsnd=adp.adptvgrnMod(rsnd,strength=0.35,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
#AA&Deband
aa16=taa.TAAmbk(rs16,aatype=3,aarepair=-20,mtype=2,sharp=-0.5,postaa=True,stabilize=2,cycle=2)
aa16=Deband(aa16,nrmask,range1=8,range2=12,y1=36,c1=24,r1=24,y2=24,c2=16,r2=16,thr=0.6,thrc=0.5,elast=2.8,first_plane=False)
aa16=core.std.MergeDiff(aa16,diff)
aa16=adp.adptvgrnMod(aa16,strength=0.35,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
#Strong AA&Deband
aa16_s=taa.TAAmbk(rs16,aatype=-1)
aa16_s=Deband(aa16_s,nrmask,range1=8,range2=12,y1=36,c1=24,r1=24,y2=24,c2=16,r2=16,thr=0.6,thrc=0.5,elast=2.8,first_plane=False)
aa16_s=core.std.MergeDiff(aa16_s,diff)
aa16_s=adp.adptvgrnMod(aa16_s,strength=0.35,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
#RGB To Preview
##NoAA
#225-413
##S_AA
#414-475
#1454-1484
out16=fvf.rfs(aa16,rsnd,"[225 413]")##NoAA
out16=fvf.rfs(out16,aa16_s,"[414 475] [1454 1484]")##S_AA
#OKE:DEBUG
debug =0
if debug:
	src1 = mvf.ToRGB(src8,depth=8)
	src2 = mvf.ToRGB(out16,depth=8)
	src3 = mvf.ToRGB(src16,depth=8)
	#compare = core.butteraugli.butteraugli(src1,src2)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(out16,10)
res.set_output()
src8.set_output(1)