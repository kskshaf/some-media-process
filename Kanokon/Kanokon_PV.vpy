import vapoursynth as vs
from vapoursynth import core
import havsfunc as haf
import mvsfunc as mvf
import nnedi3_resample as nnrs
import zvs
#OKE:MEMORY
core.max_cache_size=8000
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
#OKE:INPUTFILE
a=r'E:\DVD\KANOKON\PV.mkv'
src=core.lsmas.LWLibavSource(a,repeat=True)
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
deint=haf.QTGMC(src,Preset="Slower",TFF=True,FPSDivisor=2)
src8=core.vivtc.VDecimate(deint)
src8=core.std.SetFieldBased(src8,0)
src8=haf.daa(src8)
#Crop&Resize
src8=core.std.Crop(src8,left=4,right=4,top=2,bottom=2)
src8=core.resize.Spline64(src8,width=720,height=540,src_top=0)
b_ref=core.std.BoxBlur(src8,planes=0,hradius=1,hpasses=1,vpasses=0)
src8=core.edgefixer.Reference(src8,b_ref,left=6,right=6)
src8=core.std.Crop(src8,top=66,bottom=64)
src8=core.edgefixer.Continuity(src8,top=2,bottom=2)
#Denoise(stolen from x_x)
src16=mvf.Depth(src8,16)
smd=haf.SMDegrain(src16,3,320,RefineMotion=True,prefilter=3)
resb=zvs.bm3d(src16,smd,sigma=[2,2,2],radius2=1,vt=1,mode='cpu')
res=haf.SMDegrain(resb,3,320,RefineMotion=True,prefilter=3)
res=zvs.bm3d(smd,res,sigma=[1,1,1],radius2=1,vt=1,mode='cpu')
#EdgeClean
res=haf.FineDehalo(res,darkstr=0,brightstr=0.5)
res=haf.EdgeCleaner(res,strength=30,rmode=20)
#Deband
db=core.neo_f3kdb.Deband(res,8,36,24,24,0,0,sample_mode=4)
db=core.neo_f3kdb.Deband(db,15,24,16,16,0,0,sample_mode=4)
db=mvf.LimitFilter(db,res,thr=0.6,thrc=0.5,elast=3)
res=core.std.MaskedMerge(db,res,DBMask(res),first_plane=True)
res=nnrs.nnedi3_resample(res,1280,720,nsize=3,qual=2,mode='znedi3',csp=vs.YUV420P10)
#
res.set_output()
src8.set_output(1)
