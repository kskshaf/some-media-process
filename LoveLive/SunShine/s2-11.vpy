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
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 6\BDMV\STREAM\00005.m2ts'
b=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 6\BDMV\STREAM\00006.m2ts'
srca=core.lsmas.LWLibavSource(a,repeat=True)
srcb=core.lsmas.LWLibavSource(b,repeat=True)
src8=core.std.SetFieldBased(srca+srcb,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1,0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Rescale&FixBoeder
rs_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
rs_f=core.edgefixer.Continuity(rs_y,left=1,top=1,right=1,bottom=1)
rs_m=core.std.BlankClip(rs_y).std.CropRel(1,1,1,1).std.AddBorders(1,1,1,1,65535)
rs_y=core.std.MaskedMerge(rs_y,rs_f,rs_m)
rs_y=MRcoref(rs_y,'Debilinear',h=720,mask_dif_pix=3.6,mthr=[6,5],show='result',blur_mask=True,ds_aa=True,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,aacycle=0,dark=0,dehalo=True,dering=True,thlimi=80,thlima=160,brightstr=1.0,drthr=5)
rs=core.std.ShufflePlanes([rs_y,bm3d],[0,1,2],vs.YUV)
#Deband&MergeNoise
db1=zvs.xdbcas(rs,mask=True,casstr=0.16)
gn=core.std.MergeFullDiff(db1,core.std.MakeFullDiff(bm3d,src16))
gn=core.std.Merge(db1,gn,0.90)
gnmk=core.adg.Mask(db1.std.PlaneStats(),16)
db1=core.std.MaskedMerge(db1,gn,gnmk)
db1=mvf.Depth(db1,10)
#
db2=zvs.xdbcas(bm3d,mask=True,casstr=0)
db2=mvf.Depth(db2,10)
out10=db1[:34047]+db2[34047:]
#
preview0=src8
preview1=db1
preview2=src8
preview3=out10
#OKE:DEBUG
Debug=0
if Debug==1:
	n=20600
	#src1=zvs.n3pv(preview0,scale=1)#[n]
	#src2=zvs.n3pv(preview1,scale=1)#[n]
	src1=mvf.ToRGB(preview0,depth=8)[n]
	src2=mvf.ToRGB(preview1,depth=8)[n]
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