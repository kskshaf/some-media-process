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
mvd=zvs.zmdg(src16,thsad=120,truemotion=True,thscd1=200,limit=350)
cb=DFTTest(mvd,sigma=1.6,tbsize=5)
cb32=cb.fmtc.bitdepth(bits=32)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb32,sigma=[3,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.2,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
tpbd=bm3d
egmk=zvs.wtfmask(bm3d,nnrs=True,t_l=16,t_h=26,range='limited',op=[1],optc=2,bin=True,bthr=1)
bm3d=core.std.MaskedMerge(bm3d,cb,egmk)
diff=core.std.MakeFullDiff(bm3d,src16)
#Rescale&FixBoeder
rs_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
bm3d_y=rs_y
rs_f=core.edgefixer.Continuity(rs_y,left=2,top=2,right=2,bottom=2)
rs_m=core.std.BlankClip(rs_y).std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535)
rs_y=core.std.MaskedMerge(rs_y,rs_f,rs_m)
rs_y=MRcoref(rs_y,'Debilinear',h=720,mask_dif_pix=3.6,mthr=[6,5],show='result',blur_mask=True,ds_aa=True,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stablize=2,aacycle=0,dark=0,dehalo=True,dering=True,thlimi=80,thlima=160,brightstr=1.0,drthr=5)
rs=core.std.ShufflePlanes([rs_y,bm3d],[0,1,2],vs.YUV)
#Deband&MergeNoise
db1=zvs.xdbcas(rs,y=[48,36],cb=[32,24],cr=[32,24],mask=True,casstr=0.16)
db1=adp.adptvgrnMod(db1,strength=0.40,size=1.0,sharp=50,static=False,luma_scaling=18,grain_chroma=False)
db1=mvf.Depth(db1,10)
#Oths
db2=zvs.xdbcas(tpbd,y=[48,36],cb=[32,24],cr=[32,24],mask=False,casstr=0)
db2=mvf.Depth(db2,10)
#Extract 0-215 ; 384-600
srcb=core.lsmas.LWLibavSource(r"E:\BD\[BDMV][2015.10.07] ラブライブ！サンシャイン!! Aqours - 君のこころは輝いてるかい？\BDMV\STREAM\00000.m2ts",repeat=True).fmtc.bitdepth(bits=16)
srcb=srcb[0]+srcb
srcb=core.std.CropRel(srcb,left=24,right=24,top=14,bottom=14)
srcb=nnrs.nnedi3_resample(srcb,1920,1080,mode='znedi3')
srcb=crossfademod(srcb[:217],rs[384:601],150,213)
db3=zvs.xdbcas(srcb,y=[48,36],cb=[32,24],cr=[32,24],mask=False,casstr=0)
db3=mvf.Depth(db3,10)
#ED
ed_f=core.edgefixer.Continuity(tpbd,left=2,top=2,right=2,bottom=2)
ed_m=core.std.BlankClip(bm3d_y).std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535)
ed_o=core.std.MaskedMerge(tpbd,ed_f,ed_m)
ed_o=zvs.xdbcas(ed_o,mask=True,casstr=0.1)
ed_nm=core.std.MergeFullDiff(ed_o,diff)
ed=core.std.Merge(ed_o,ed_nm,0.86)
edgm=core.adg.Mask(ed_o.std.PlaneStats(),16)
ed=core.std.MaskedMerge(ed,ed_nm,edgm)
ed=mvf.Depth(ed,10)
ed=crossfademod(db1,ed,138561,138679)
#
out10=db2[:384]+db3+db1[601:138561]+ed[138561:143505]+db1[143505:144192]+db2[144192:]
#
preview0=src8 #[384:601]
preview1=db1 #[:217]
preview2=src8
preview3=tpbd
#OKE:DEBUG
Debug=1
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