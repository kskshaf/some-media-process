import vapoursynth as vs
core = vs.core
a=r"E:\BD\[210714] ｢11という名の永遠の素数｣／22／7 [完全生産限定盤C] (flac)\SRCL-11790\BDMV\STREAM\00009.m2ts"
src8=core.lsmas.LWLibavSource(a)
src8.set_output()