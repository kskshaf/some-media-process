import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import adptvgrnMod as adp
import fvsfunc as fvf
from vsutil import get_y
core = vs.core
#OKE:MEMORY
core.max_cache_size = 9000
#MinBlur_Sharpen
def Sharp(src_nos,r=1,sigma=1,t_h=12,t_l=2.5,mode=1,op=1,mask=None):
    edge=core.tcanny.TCanny(get_y(src_nos),sigma=sigma,t_h=t_h,t_l=t_l,mode=mode,op=op).std.Maximum().std.Minimum().std.Maximum()
    edge=haf.MinBlur(edge,1)
    mmd_s=core.std.MergeDiff(src_nos,core.std.MakeDiff(src_nos,haf.MinBlur(src_nos,r)))
    sharp=core.std.MaskedMerge(mmd_s,src_nos,edge)
    if mask is None:
        out=sharp
    else:
        out=edge

    return out
##DB
def DB(clipa,clipb,nrmask):
    db16=core.f3kdb.Deband(clipa,8,48,36,36,0,0)
    db16=core.f3kdb.Deband(db16,12,36,24,24,0,0)
    db16=mvf.LimitFilter(db16,clipa,thr=0.6,thrc=0.5,elast=2.5)
    db16=core.std.MaskedMerge(clipa,clipb,nrmask,first_plane=True)
    sp16=Sharp(db16,sigma=1.2,op=2)
    out16=mvf.LimitFilter(sp16,db16,thr=0.8,thrc=0.7,elast=4.5)
    return out16
#OKE:INPUTFILE
a = r'F:\BDMV\Magica Record\S2 02\BDMV\STREAM\00004.m2ts'
ass = ''.join([a[0:-4],'sc.ass'])
src8=core.lsmas.LWLibavSource(a)
src16=mvf.Depth(src8,16)
ssub=src16.xyvsf.TextSub(ass)
knlm=core.knlm.KNLMeansCL(src16,d=1,a=4,s=4,h=0.9,device_type="GPU")
#AA
mask_e=core.tcanny.TCanny(get_y(src16),sigma=1.3,mode=1,op=0)
mask_m=haf.MinBlur(mask_e).rgvs.RemoveGrain(20)
mask_k=core.std.Expr([mask_e,mask_m],["x y - abs"]).std.Binarize(6000).std.Maximum().std.Minimum()
aa16=taa.TAAmbk(knlm,aatype=3,mtype=2,postaa=True,aarepair=-20,stablize=2)
aa16=core.std.MaskedMerge(knlm,aa16,mask_k)
aa16=haf.EdgeCleaner(aa16,rmode=18)
#DebandMask(LoliHouse)
nr8    = mvf.Depth(knlm,depth=8)
luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks,nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
#DB
outa=DB(knlm,knlm,nrmask)
outb=DB(knlm,aa16,nrmask)
out16=fvf.rfs(outb,outa,"[24664 25107] [25204 25389] [25612 25707] [25876 25965]")
#Dither
bright = mvf.Depth(out16,8,dither=0,ampo=1.0)
dark = mvf.Depth(out16,8,dither=0,ampo=2.0)
bin = core.std.Binarize(bright,128,planes=0).std.Inflate().std.Inflate().std.Maximum().std.Maximum().rgvs.RemoveGrain(20)
dt8 = core.std.MaskedMerge(dark,bright,bin,first_plane=True)
#OKE:DEBUG
debug =0
if debug:
	src1 = mvf.ToRGB(src8,depth=8)
	src2 = mvf.ToRGB(bin,depth=8)
	cp = core.butteraugli.butteraugli(src1,src2)
	res = core.std.Interleave([src1,src2])
else: 
	res=core.xyvsf.TextSub(mvf.Depth(dt8,16),ass)
	res=mvf.Depth(res,8)
res.set_output()
ssub.set_output(1)