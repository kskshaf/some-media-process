import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import fvsfunc as fvf
import kagefunc as kgf
import adptvgrnMod as adp
import xvs,zvs
import nnedi3_resample as nnrs
from vsmlrt import DPIR, DPIRModel, Backend
from dfttest2 import DFTTest
core = vs.core

def crossfademod(clipa,clipb,start,end):
    fd=kgf.crossfade(clipa[start:end+3],clipb[start:end+3],end-start+2)
    fade=clipa[:start]+fd[:-3]+clipb[end+1:]
    return fade

src   = core.imwri.Read(filename="E:\\Video\\PNG\\moyu2\\%04d.png", firstnum=0)
src_fyuv_16 =  mvf.ToYUV(src, css='444', depth=16)

small = DFTTest(src_fyuv_16 ,sigma=5,tbsize=1)

rgb   = nnrs.nnedi3_resample(src, nsize=3, qual=2, mode='znedi3', csp=vs.RGBS)
dpir  = DPIR(rgb, strength=8.88, model=DPIRModel.drunet_color, tiles=1, backend=Backend.TRT(fp16=True, device_id=0, num_streams=1))
dpir_fyuv_16 =  mvf.ToYUV(dpir, css='444', depth=16)

adb   = fvf.AutoDeblock(dpir_fyuv_16, db2=16, db3=42)

dpir = mvf.ToRGB(dpir, depth=16)
adb  = mvf.ToRGB(adb, depth=16)
small= mvf.ToRGB(small, depth=16)

f1 = crossfademod(src, dpir, 3320, 3340)
f2 = crossfademod(dpir, src, 3480, 3486)
f3 = crossfademod(src, dpir, 3967, 3977)


small_a = core.imwri.Write(small[2124:2174],imgformat='PNG',firstnum=2124,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

dpir_a = small_a + core.imwri.Write(dpir[3039:3064],imgformat='PNG',firstnum=3039,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

adb_a = dpir_a + core.imwri.Write(adb[3064:3095],imgformat='PNG',firstnum=3064,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

dpir_a = adb_a + core.imwri.Write(dpir[3095:3108],imgformat='PNG',firstnum=3095,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

fade_a = dpir_a + core.imwri.Write(f1[3320:3382],imgformat='PNG',firstnum=3320,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

dpir_a = fade_a + core.imwri.Write(dpir[3468:3480],imgformat='PNG',firstnum=3468,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

fade_a = dpir_a + core.imwri.Write(f2[3480:3487],imgformat='PNG',firstnum=3480,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

dpir_a = fade_a + core.imwri.Write(dpir[3555:3584],imgformat='PNG',firstnum=3555,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)

fade_a = dpir_a + core.imwri.Write(f3[3967:4025],imgformat='PNG',firstnum=3967,filename="E:\\Video\\PNG\\moyu2\\refix\\%04d.png",quality=0)
fade_a.set_output()

# DPIR
# [3039 3063] [3095 3107] [3468 3479] [3555 3583]
# with crossfademod() f1[3320 3381] f2[3480 3486] f3[3967 4024]
#

# ADB
# [3064 3094]
#

# Small
# [2124 2173]


#res1=zvs.n3pv(src,scale=1)
#res1.set_output()

#res2=zvs.n3pv(dpir,scale=1)
#res2.set_output(1)

#res3=zvs.n3pv(adb,scale=1)
#res3.set_output(2)

#res4=zvs.n3pv(small,scale=1)
#res4.set_output(3)

#res5=zvs.n3pv(f2,scale=1)
#res5.set_output(4)
