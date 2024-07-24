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

src   = core.imwri.Read(filename="E:\\Video\\PNG\\moyu1\\%04d.png", firstnum=0)
src_fyuv_16 =  mvf.ToYUV(src, css='444', depth=16)

small = DFTTest(src_fyuv_16 ,sigma=5,tbsize=1)

rgb   = nnrs.nnedi3_resample(src, nsize=3, qual=2, mode='znedi3', csp=vs.RGBS)
dpir  = DPIR(rgb, strength=8.88, model=DPIRModel.drunet_color, tiles=1, backend=Backend.TRT(fp16=True, device_id=0, num_streams=1))
dpir_fyuv_16 =  mvf.ToYUV(dpir, css='444', depth=16)

adb   = fvf.AutoDeblock(dpir_fyuv_16, db2=16, db3=42)

#f1 = crossfademod(dpir_fyuv_16, src_fyuv_16, 1177, 1205)
#f2 = crossfademod(dpir_fyuv_16, small, 1284, 1338)

dpir = mvf.ToRGB(dpir, depth=16)
adb  = mvf.ToRGB(adb, depth=16)
small= mvf.ToRGB(small, depth=16)

f1 = crossfademod(dpir, src, 1177, 1205)
f2 = crossfademod(dpir, small, 1284, 1338)



dpir_a = core.imwri.Write(dpir[169:250],imgformat='PNG',firstnum=169,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

adb_a  = dpir_a + core.imwri.Write(adb[250:265],imgformat='PNG',firstnum=250,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

dpir_a = adb_a  + core.imwri.Write(dpir[265:299],imgformat='PNG',firstnum=265,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

small_a = dpir_a + core.imwri.Write(small[360:366],imgformat='PNG',firstnum=360,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

dpir_a = small_a + core.imwri.Write(dpir[366:378],imgformat='PNG',firstnum=366,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)
dpir_a = dpir_a +  core.imwri.Write(dpir[521],imgformat='PNG',firstnum=521,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

adb_a  = dpir_a + core.imwri.Write(adb[630:675],imgformat='PNG',firstnum=630,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

dpir_a = adb_a  + core.imwri.Write(dpir[1093:1112],imgformat='PNG',firstnum=1093,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

fade_a = dpir_a + core.imwri.Write(f1[1177:1206],imgformat='PNG',firstnum=1177,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

small_a = fade_a +  core.imwri.Write(small[1251:1284],imgformat='PNG',firstnum=1251,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

fade_a = small_a + core.imwri.Write(f2[1284:1339],imgformat='PNG',firstnum=1284,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

small_a = fade_a + core.imwri.Write(small[1336:1456],imgformat='PNG',firstnum=1336,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)

dpir_a = small_a + core.imwri.Write(dpir[2955:3086],imgformat='PNG',firstnum=2955,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)
dpir_a = dpir_a + core.imwri.Write(dpir[3270:3310],imgformat='PNG',firstnum=3270,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png",quality=0)
dpir_a.set_output()


# DPIR
# [169 249] [265 298] [366 377] 521 [1093 1111] [2955 3085] [3270 3309]
# with crossfademod() [1177 1205] [1284 1335]
#

# ADB
# [250 264] [630 674]
#

# Small
# [360 365] [1251 1283] [1336 1455]


#res1=zvs.n3pv(src,scale=1)
#res1.set_output()

#res2=zvs.n3pv(dpir,scale=1)
#res2.set_output(1)

#res3=zvs.n3pv(adb,scale=1)
#res3.set_output(2)

#res4=zvs.n3pv(small,scale=1)
#res4.set_output(3)

#res5=res1[:1177]+res2[1177:1197]+res1[1197:]
#f2.set_output(4)
