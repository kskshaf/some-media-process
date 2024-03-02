import vapoursynth as vs
from vsmlrt import DPIR, DPIRModel, Backend
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import vsutil
import nnedi3_resample as nnrs
import fvsfunc as fvf
import kagefunc as kgf
import xvs
core = vs.core

core.max_cache_size = 6000

a = r'D:\Game\ISLAND\ISLAND_OP.mpg'
src8 = core.lsmas.LWLibavSource(a)
src16 = mvf.ToYUV(src8,depth=16,css="420")

up16 = nnrs.nnedi3_resample(src16,target_width=1920,target_height=1080)
up32 = mvf.ToRGB(up16,depth=32)
flt32 = DPIR(up32,strength=45, model=DPIRModel.drunet_deblocking_color, tiles=2, backend=Backend.OV_CPU())
flt16 = mvf.ToYUV(flt32,depth=16,css="420")
nr16 = flt16
#mask = core.tcanny.TCanny(vsutil.get_y(haf.MinBlur(up16)), sigma=1.0, t_h=8.0, t_l=1.0, mode=1, op=1)
#mask = core.std.Expr(mask,["x 25000 > 65535 0 ?"])
#mask = mask.std.Maximum().std.Minimum().std.Maximum().std.Inflate().std.Inflate()
#nr16 = core.std.MaskedMerge(flt16,up16,mask)
nr8    = mvf.Depth(nr16,depth=8)
luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
nrmasks = core.tcanny.TCanny(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
nrmaskb = core.tcanny.TCanny(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
nrmaskg = core.tcanny.TCanny(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks, nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
debd  = core.f3kdb.Deband(nr16,12,36,24,24,0,0,output_depth=16)
debd  = core.f3kdb.Deband(debd,20,64,48,48,0,0,output_depth=16)
debd  = mvf.LimitFilter(debd,nr16,thr=0.6,thrc=0.5,elast=3.0)
out16  = core.std.MaskedMerge(debd,nr16,nrmask,first_plane=True)
res = mvf.Depth(out16,10)

res.set_output()