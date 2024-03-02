from vapoursynth import core
from ksksfunc import MRcoref, Sharp
from dfttest2 import DFTTest
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import xvs,zvs
import nnedi3_resample as nnrs
import adptvgrnMod as adp
#
def crossfademod(clipa,clipb,start,end):
    import kagefunc as kgf
    fd=kgf.crossfade(clipa[start:end+3],clipb[start:end+3],end-start+2)
    fade=clipa[:start]+fd[:-3]+clipb[end+1:]
    return fade
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 7\BDMV\STREAM\00004.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
mvd=zvs.zmdg(src16,thsad=200,truemotion=True,thscd1=250,limit=350,cs=True)
mvd=mvd.fmtc.bitdepth(bits=32)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,mvd,sigma=[3,2.0],block_step=6,bm_range=9,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(mvd,bm3d_b,sigma=[1.5,1.0],block_step=5,bm_range=9,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Rescale&FixBoeder
rs_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
bm3d_y=rs_y
rs_f=core.edgefixer.Continuity(rs_y,left=2,top=2,right=2,bottom=2)
rs_m=core.std.BlankClip(rs_y).std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535)
rs_y=core.std.MaskedMerge(rs_y,rs_f,rs_m)
rs_y=MRcoref(rs_y,'Debilinear',h=720,mask_dif_pix=3.6,mthr=[6,5],show='result',blur_mask=True,ds_aa=True,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stablize=2,aacycle=0,dark=0,dehalo=True,dering=True,thlimi=80,thlima=160,brightstr=1.0,drthr=5)
rs=core.std.ShufflePlanes([rs_y,bm3d],[0,1,2],vs.YUV)
#Deband&MergeNoise
db1=zvs.xdbcas(rs,y=[48,36],cb=[32,24],cr=[32,24],mask=True,casstr=0)
#db1=adp.adptvgrnMod(db1,strength=0.40,size=1.0,sharp=50,static=False,luma_scaling=18,grain_chroma=False)
#start=30203;end=35165
out10=mvf.Depth(db1,10)[2391:138470]#[start:end+1]
#
preview0=src8#[start:end+1]
preview1=rs#[start:end+1]
preview2=src8 #[start:end+1]
preview3=bm3d #[start:end+1]
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	#src1=zvs.n3pv(preview0,scale=1)#[n]
	#src2=zvs.n3pv(preview1,scale=1)#[n]
	src1=mvf.ToRGB(preview0,depth=8)#[n]
	src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	#src8=src8[1456]+src8[2656]+src8[3564]+src8[6666]
	res=nnrs.nnedi3_resample(src8,mode='znedi3',csp=vs.RGB24)
	#res=core.imwri.Write(res,imgformat="PNG",filename="E:\\A\\apours%04d.png",firstnum=0,quality=0,overwrite=True)
else:
	res=out10
res.set_output()
src8.set_output(1)