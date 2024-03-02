from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import zvs
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC2\BDMV\STREAM\00006.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src16=core.std.CropRel(src16,top=108,bottom=108)
src32=core.fmtc.bitdepth(src16,bits=32)
#Denoise
mvd=zvs.zmdg(src16,thsad=200,truemotion=False,thscd1=250,limit=350,cs=False)
mvd=mvd.fmtc.bitdepth(bits=32)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,mvd,sigma=[4,2],block_step=6,bm_range=9,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,1],block_step=5,bm_range=9,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
diff=core.std.MakeFullDiff(src16,bm3d)
#Rescale&FixBoeder
fb_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
fb_f=core.edgefixer.Continuity(fb_y,top=2,bottom=2)
fb_m=core.std.BlankClip(fb_y).std.CropRel(top=2,bottom=2).std.AddBorders(top=2,bottom=2,color=65535)
fb_y=core.std.MaskedMerge(fb_y,fb_f,fb_m)
fb=core.std.ShufflePlanes([fb_y,bm3d],[0,1,2],vs.YUV)
db1=zvs.xdbcas(fb,y=[72,60],cb=[72,60],cr=[72,60],gy=[15,15],gc=[0,0],mask=False,casstr=0,limit=[0.6,0.5,3])
db1=core.std.MergeFullDiff(db1,diff)

preview0=src16
preview1=db1
preview2=src16
preview3=src8
#OKE:DEBUG
Debug=1
if Debug==1:
	#n=1372
	src1=mvf.ToRGB(preview0,depth=8)#[n]
	src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=src8
else:
	res=mvf.Depth(db1,10)
res.set_output()
src16.set_output(1)

