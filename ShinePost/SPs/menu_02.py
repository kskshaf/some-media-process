import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
core = vs.core

a=r'/run/media/ksks/Others/ShinePost/[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]/SHINEPOST_BOX1_DISC2/BDMV/STREAM/00007.m2ts'
src16=core.lsmas.LWLibavSource(a).fmtc.bitdepth(bits=16)
out=zvs.xdbcas(src16,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0)
out=mvf.Depth(out,10)

out.set_output()
src16.set_output(1)
mvf.ToRGB(src16,depth=8).set_output(2)
