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
#OKE:INPUTFILE
a=r"E:\BD\[210714] ｢11という名の永遠の素数｣／22／7 [完全生産限定盤C] (flac)\SRCL-11790\BDMV\STREAM\00003.m2ts"
src8=core.lsmas.LWLibavSource(a)
src16=mvf.Depth(src8,16)
aa16=taa.TAAmbk(src16,aatype=3,aarepair=-20,mtype=2,sharp=-0.5,postaa=True,stablize=2)
nrmask=DBMask(src16)
nrmask=ksf.Y(nrmask)#DebandMask
db1=Deband(aa16,nrmask,range1=8,range2=12,y1=48,c1=36,r1=36,y2=36,c2=24,r2=24,thr=0.6,thrc=0.5,elast=2.0,first_plane=False)
db1=adp.adptvgrnMod(db1,strength=0.25,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
db2=Deband(aa16,nrmask,range1=6,range2=8,y1=64,c1=48,r1=48,y2=48,c2=32,r2=32,thr=1.2,thrc=1.0,elast=5,first_plane=False)
db2=adp.adptvgrnMod(db2,strength=0.25,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
db3=Deband(aa16,nrmask,range1=6,range2=12,y1=48,c1=36,r1=36,y2=36,c2=36,r2=36,thr=0.8,thrc=0.7,elast=3.0,first_plane=False)
db3=adp.adptvgrnMod(db3,strength=0.25,size=1.5,sharp=30,static=False,luma_scaling=12,grain_chroma=False)
out8=fvf.rfs(db1,db2,"[627 717]")
out8=fvf.rfs(out8,db3,"[1808 1822] [5114 5126]")
out8=fvf.rfs(out8,src16,"[6711 6800]")
#OKE:DEBUG
debug =0
if debug:
	src1 = mvf.ToRGB(src8,depth=8)
	src2 = mvf.ToRGB(out8,depth=8)
	src3 = mvf.ToRGB(src16,depth=8)
	#compare = core.butteraugli.butteraugli(src1,src2)
	res = core.std.Interleave([src1,src2])
else: res = mvf.Depth(out8,8)
res.set_output()
src16.set_output(1)