import vapoursynth as vs
import mvsfunc as mvf
import fvsfunc as fvf
import xvs,zvs
import nnedi3_resample as nnrs
core = vs.core

src   = core.imwri.Read(filename="/mnt/Video/PNG/moyu2/%04d.png", firstnum=0)

read1 = core.imwri.Read(firstnum=2124,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")
read2 = core.imwri.Read(firstnum=3039,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")
read3 = core.imwri.Read(firstnum=3320,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")
read4 = core.imwri.Read(firstnum=3468,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")
read5 = core.imwri.Read(firstnum=3555,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")
read6 = core.imwri.Read(firstnum=3967,filename="/mnt/Video/PNG/moyu2/refix/%04d.png")

res = fvf.rfs(src,read1,"[2124 2173]",fd_mode=True)
res = fvf.rfs(res,read2,"[3039 3107]",fd_mode=True)
res = fvf.rfs(res,read3,"[3320 3381]",fd_mode=True)
res = fvf.rfs(res,read4,"[3468 3486]",fd_mode=True)
res = fvf.rfs(res,read5,"[3555 3583]",fd_mode=True)
res = fvf.rfs(res,read6,"[3967 4024]",fd_mode=True)

res = nnrs.nnedi3_resample(res,1920,1080,nsize=3,qual=2,mode='znedi3',csp=vs.YUV444P16)
res = zvs.xdbcas(res,y=[48,36],cb=[36,24],cr=[36,24],mask=False,casstr=0.08)
res = mvf.Depth(res, depth=10)
res.set_output()
