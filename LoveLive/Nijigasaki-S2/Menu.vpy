import vapoursynth as vs
import mvsfunc as mvf
core = vs.core
#OKE:MEMORY
core.max_cache_size=8000
#OKE:INPUTFILE
a=r'F:\BDMV\LL Nijigasaki S2D1\BDROM\BDMV\STREAM\00011.m2ts'
src8=core.lsmas.LWLibavSource(a)
res=mvf.Depth(src8,10)

res.set_output()
src8.set_output(1)