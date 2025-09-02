import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import xvs
from dfttest2 import DFTTest
core = vs.core
core.num_threads=16
core.max_cache_size=10000
a=r'E:\Bangumi BT\[Ioroid] Oniichan wa Oshimai! - 01 [ABEMA WEB-DL 1080p AVC AAC].mkv'
#Sharpen
def Sharp(src_nos,sigma=1,t_h=12,t_l=2.5,mode=1,op=1,br=1,rmode=0,thr=0.6,thrc=0.5,elast=10,showmask=False):
    gety=xvs.getY(src_nos)
    edge=core.tcanny.TCanny(gety,sigma=sigma,t_h=t_h,t_l=t_l,mode=mode,op=op).std.Maximum().std.Minimum().std.Maximum()
    edge=haf.MinBlur(edge,br).rgvs.RemoveGrain(rmode)
    mmd_s=core.std.MergeDiff(src_nos,core.std.MakeDiff(src_nos,haf.MinBlur(src_nos,br)))
    sharp=mvf.LimitFilter(mmd_s,src_nos,thr=thr,thrc=thrc,elast=elast)
    sharp=core.std.MaskedMerge(mmd_s,src_nos,edge)
    if showmask:
        sharp_out=edge
    else:
        sharp_out=sharp
    return sharp_out
#Deband
def Deband(denoised,nrmask,range1=6,range2=10,y1=48,c1=36,r1=36,y2=36,c2=24,r2=24,thr=0.6,thrc=0.5,elast=2.0,first_plane=True):
    deband=core.f3kdb.Deband(denoised,range1,y1,c1,r1,0,0)
    deband=core.f3kdb.Deband(deband,range2,y2,c2,r2,0,0)
    deband=mvf.LimitFilter(deband,denoised,thr=thr,thrc=thrc,elast=elast)
    deband=core.std.MaskedMerge(deband,denoised,nrmask,first_plane)
    return deband
#DebandMask(From 1st Anniversary Gift Pack of LoliHouse.)
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
#######################################
src8=core.lsmas.LWLibavSource(a)
flt=mvf.Depth(src8,32)
dft=DFTTest(flt,sigma=2,tbsize=1)
bm3d_b=core.bm3dcpu.BM3Dv2(flt,dft,sigma=[5,4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(flt,bm3d_b,sigma=[1.6,1.0],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5)
src=xvs.rescalef(bm3d,'Debicubic',h=844,b=0.33,c=0.33,mask_dif_pix=2)
src=haf.FineDehalo(src,brightstr=0.8,darkstr=0)
src=taa.TAAmbk(src,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=2)
src=Sharp(src,t_h=12,t_l=8,mode=1,op=2,elast=4.5)
src=Deband(src,DBMask(src),8,15,48,36,36,36,24,24,thr=1.0,thrc=0.8,elast=3)
src=mvf.Depth(src,10)[:25]
src.set_output()
