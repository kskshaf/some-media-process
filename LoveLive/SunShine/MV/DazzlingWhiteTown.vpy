from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
from ksksfunc import MRcoref
import xvs,zvs
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\CD\[EAC][200819][SINGLE][Saint Snow][Dazzling White Town][LACM-14934][WAV+CUE+LOG+PNG+BDMV]\BDMV\STREAM\00001.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1,0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Rescale&FixBoeder
rs_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
rs_f=core.edgefixer.Continuity(rs_y,left=2,top=2,right=2,bottom=2)
rs_m=core.std.BlankClip(rs_y).std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535)
rs_y=core.std.MaskedMerge(rs_y,rs_f,rs_m)
rs_y=MRcoref(rs_y,'Debilinear',h=720,mask_dif_pix=3.6,mthr=[6,5],show='result',blur_mask=True,ds_aa=True,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=2,aacycle=0,dark=0,dehalo=True,dering=True,thlimi=80,thlima=160,brightstr=1.0,drthr=5)
rs=core.std.ShufflePlanes([rs_y,bm3d],[0,1,2],vs.YUV)
#Deband
db1=zvs.xdbcas(rs,mask=True,casstr=0.16)
out10=mvf.Depth(db1,10)[470:]
#
preview0=src8
preview1=db1
preview2=src8
preview3=out10
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
	res=core.text.ClipInfo(res)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	src8=src8[1456]+src8[2656]+src8[3564]+src8[6666]
else:
	res=out10
res.set_output()
src8[470:].set_output(1)