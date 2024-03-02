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
core.max_cache_size=10500
#ksf.ADN(input,sigma,radius1,block_step,bm_range,ps_num,ps_range,x1=52428,y1=65535,x2=32678,y2=1200)
#NormalDeband
def Deband(denoised,nrmask,range1=6,y1=48,c1=36,r1=36,y2=36,c2=24,r2=24,range2=10,thr=0.6,thrc=0.5,elast=2.5,first_plane=True):
    deband=core.f3kdb.Deband(denoised,range1,y1,c1,r1,0,0)
    deband=core.f3kdb.Deband(deband,range2,y2,c2,r2,0,0)
    deband=mvf.LimitFilter(deband,denoised,thr=thr,thrc=thrc,elast=elast)
    deband=core.std.MaskedMerge(deband,denoised,nrmask,first_plane)
    return deband
#DebandMask(LoliHouse)
def DBMask(clip):
    nr8=mvf.Depth(clip,8)
    luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
    nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
    nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
    nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
    nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks,nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
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
#INPUT
a=r"E:\BD\[210714] ｢11という名の永遠の素数｣／22／7 [完全生産限定盤C] (flac)\SRCL-11790\BDMV\STREAM\00001.m2ts"
src8=core.lsmas.LWLibavSource(a)#[4964:5217]
src16=mvf.Depth(src8,16)
#Denoise
bm3d=ksf.BM3DCPU(src16,[3,3],radius1=2,block_step=7,bm_range=12,ps_num=2,ps_range=5)
nrmask=DBMask(bm3d)#DebandMask
normal=Deband(bm3d,nrmask,range1=10,range2=12,y1=36,c1=24,r1=24,y2=18,c2=16,r2=16,thr=0.6,thrc=0.5,elast=2.0)
normal=adp.adptvgrnMod(Sharp(normal,1),strength=0.6,size=1.5,sharp=30,static=False,luma_scaling=4,grain_chroma=False)
db1=Deband(bm3d,nrmask,range1=6,range2=9,thr=1.2,thrc=1.0,elast=4)
db1=adp.adptvgrnMod(Sharp(db1,1),strength=0.6,size=1.5,sharp=30,static=False,luma_scaling=4,grain_chroma=False)
db2=Deband(bm3d,nrmask,range1=6,range2=8,thr=1.2,thrc=1.0,elast=2.2)
db2=adp.adptvgrnMod(Sharp(db2,1),strength=0.6,size=1.5,sharp=30,static=False,luma_scaling=4,grain_chroma=False)
db3=Deband(bm3d,nrmask,range1=8,range2=10,thr=0.8,thrc=0.7,elast=1.95)
db3=adp.adptvgrnMod(Sharp(db3,1),strength=0.6,size=1.5,sharp=30,static=False,luma_scaling=4,grain_chroma=False)
#1530-1553#1575-1832#1920-2184#2590-2619#3417-3564##3673-3909#3910-3951#4304-4365#4444-4539#4751-4964#5217-6800
#Deband Storng
##Part Shit
dbs=core.f3kdb.Deband(bm3d,10,48,36,36,0,0)
dbs=core.f3kdb.Deband(dbs,15,64,48,48,0,0)
dbs=core.f3kdb.Deband(dbs,6,96,72,72,0,0)
#deband=mvf.LimitFilter(dbs,denoised,thr=1.8,thrc=1.5,elast=50)
dbs=core.std.MaskedMerge(dbs,bm3d,nrmask,first_plane=True)
shit=adp.adptvgrnMod(Sharp(dbs,1),strength=0.70,size=1.5,sharp=30,static=False,luma_scaling=1.0,grain_chroma=False)
#Output
out16=fvf.rfs(normal,shit,"[1530 1553] [5217 6800]")
out16=fvf.rfs(out16,db1,"[1575 1832] [2590 2619] [4751 4964]")
out16=fvf.rfs(out16,db2,"[1920 2184] [4304 4750]")
out16=fvf.rfs(out16,db3,"[3673 3951]")
#OKE:DEBUG
debug =0
if debug:
	src1 = mvf.ToRGB(src16,depth=8)
	src2 = mvf.ToRGB(out16,depth=8)
	src3 = mvf.ToRGB(src16,depth=8)
	#compare = core.butteraugli.butteraugli(src1, src2)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(out16,10)
res.set_output()
src8.set_output(1)