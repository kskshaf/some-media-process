import vapoursynth as vs
import mvsfunc as mvf
import fvsfunc as fvf
import xvs,zvs
import nnedi3_resample as nnrs
core = vs.core

src = core.imwri.Read(filename="E:\\Video\\PNG\\moyu1\\%04d.png", firstnum=0)

read1 = core.imwri.Read(firstnum=169,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read2 = core.imwri.Read(firstnum=360,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read3 = core.imwri.Read(firstnum=521,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read4 = core.imwri.Read(firstnum=630,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read5 = core.imwri.Read(firstnum=1093,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read6 = core.imwri.Read(firstnum=1177,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read7 = core.imwri.Read(firstnum=1251,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read8 = core.imwri.Read(firstnum=2955,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")
read9 = core.imwri.Read(firstnum=3270,filename="E:\\Video\\PNG\\moyu1\\refix\\%04d.png")

res = fvf.rfs(src,read1,"[169 298]",fd_mode=True)
res = fvf.rfs(res,read2,"[360 377]",fd_mode=True)
res = fvf.rfs(res,read3,"521",fd_mode=True)
res = fvf.rfs(res,read4,"[630 674]",fd_mode=True)
res = fvf.rfs(res,read5,"[1093 1111]",fd_mode=True)
res = fvf.rfs(res,read6,"[1177 1205]",fd_mode=True)
res = fvf.rfs(res,read7,"[1251 1455]",fd_mode=True)
res = fvf.rfs(res,read8,"[2955 3085]",fd_mode=True)
res = fvf.rfs(res,read9,"[3270 3309]",fd_mode=True)

res = nnrs.nnedi3_resample(res,1920,1080,nsize=3,qual=2,mode='znedi3',csp=vs.YUV444P16)
res = zvs.xdbcas(res,y=[48,36],cb=[36,24],cr=[36,24],mask=False,casstr=0.08)
res = mvf.Depth(res, depth=10)
res.set_output()