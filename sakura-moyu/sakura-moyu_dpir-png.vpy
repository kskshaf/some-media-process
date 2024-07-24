import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import nnedi3_resample as nnrs
from vsmlrt import DPIR, DPIRModel, Backend
core = vs.core

a=r'E:\Gal\sakura-moyu\movie\01.wmv' # 02.wmv
src8=core.ffms2.Source(a)

rgb  = nnrs.nnedi3_resample(src8, nsize=3, qual=2, mode='znedi3', csp=vs.RGBS)
dpir = DPIR(rgb, strength=86, model=DPIRModel.drunet_deblocking_color, tiles=1, backend=Backend.TRT(fp16=True, device_id=0, num_streams=1))
dpir = mvf.ToRGB(dpir, depth=16)
res = core.imwri.Write(dpir,imgformat='PNG',firstnum=0,filename="E:\\Video\\PNG\\moyu1\\%04d.png",quality=0)
res.set_output()