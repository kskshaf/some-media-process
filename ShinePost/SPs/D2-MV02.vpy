from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import zvs
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC2\BDMV\STREAM\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
res=mvf.Depth(src8,10)

res.set_output()
src8.set_output(1)

