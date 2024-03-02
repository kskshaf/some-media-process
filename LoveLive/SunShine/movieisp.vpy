from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import MRcoref
import xvs,zvs
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=10000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 1\BDMV\STREAM\00035.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
mvd=zvs.zmdg(src8.fmtc.bitdepth(bits=16),thsad=200,truemotion=True,thscd1=250,limit=300,cs=True)
mvd=mvd.fmtc.bitdepth(bits=32)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,mvd,sigma=[2.4,1.4],block_step=6,bm_range=9,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(mvd,bm3d_b,sigma=[1.2,0.7],block_step=5,bm_range=9,radius=1,ps_num=2,ps_range=5)
#Deband
db1=zvs.xdbcas(bm3d,y=[48,36],cb=[32,24],cr=[32,24],mask=True,casstr=0)
out10=mvf.Depth(db1,10)
db2=zvs.xdbcas(src8,y=[48,36],cb=[32,24],cr=[32,24],mask=True,casstr=0)
src10=mvf.Depth(db2,10)

#out10=src10[:3120]+out10[3120:4380]+src10[4380:] #00026
#out10=src10[:3460]+out10[3460:4990]+src10[4990:] #00027
#out10=src10[:3220]+out10[3220:4590]+src10[4590:] #00028
#out10=src10[:3500]+out10[3500:4740]+src10[4740:] #00029
#out10=src10[:3300]+out10[3300:4598]+src10[4598:] #00030
#out10=src10[:2780]+out10[2780:4156]+src10[4156:] #00031
#out10=src10[:3150]+out10[3150:4190]+src10[4190:] #00032
#out10=src10[:2760]+out10[2760:4110]+src10[4110:] #00033
#out10=src10[:3250]+out10[3250:4520]+src10[4520:] #00034
#out10=src10[:2880]+out10[2880:3960]+src10[3960:] #00035

if a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00026.m2ts':
    out10=src10[:3120]+out10[3120:4380]+src10[4380:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00027.m2ts':
    out10=src10[:3460]+out10[3460:4990]+src10[4990:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00028.m2ts':
    out10=src10[:3220]+out10[3220:4590]+src10[4590:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00029.m2ts':
    out10=src10[:3500]+out10[3500:4740]+src10[4740:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00030.m2ts':
    out10=src10[:3300]+out10[3300:4598]+src10[4598:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00031.m2ts':
    out10=src10[:2780]+out10[2780:4156]+src10[4156:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00032.m2ts':
    out10=src10[:3150]+out10[3150:4190]+src10[4190:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00033.m2ts':
    out10=src10[:2760]+out10[2760:4110]+src10[4110:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00034.m2ts':
    out10=src10[:3250]+out10[3250:4520]+src10[4520:]
elif a=='F:\\BDMV\\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\\BD\\Special Disc 1\\BDMV\\STREAM\\00035.m2ts':
    out10=src10[:2880]+out10[2880:3960]+src10[3960:]
else: raise ValueError

out10.set_output()
src8.set_output(1)