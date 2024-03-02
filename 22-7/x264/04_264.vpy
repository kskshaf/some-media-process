import vapoursynth as vs
core=vs.core
a=r"E:\BD\[210714] ｢11という名の永遠の素数｣／22／7 [完全生産限定盤C] (flac)\SRCL-11790\BDMV\STREAM\00004.m2ts"
res=core.lsmas.LWLibavSource(a)
res.set_output()