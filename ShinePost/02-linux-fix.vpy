from vapoursynth import core
import vapoursynth as vs
import mvsfunc as mvf
import zvs
core.max_cache_size=9600

a=r"/run/media/ksks/Others/ShinePost/[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]/SHINEPOST_BOX1_DISC1/BDMV/STREAM/00016.m2ts"
src8=core.lsmas.LWLibavSource(a,repeat=True)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0.20)
res=mvf.Depth(db2,10)
res[20589:20649].set_output()
