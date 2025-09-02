from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import vsTAAmbk as taa
import fvsfunc as fvf
from ksksfunc import MRcoref
from rekt import rekt
import xvs,zvs
#OKE:MEMORY
core.max_cache_size=9600
#OKE:INPUTFILE
a=r"/run/media/ksks/Others/ShinePost/[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]/SHINEPOST_BOX2_DISC1/BDMV/STREAM/00004.m2ts"
src8=core.lsmas.LWLibavSource(a,repeat=True)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[3,1.2],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Descale mask.
bm3d_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
rs_mask=MRcoref(bm3d_y,'Delanczos',h=870,mask_dif_pix=2.6,mthr=[6,5],show='mask',blur_mask=True,aa_m=False,dering=0,dehalo=0)
# Dehalo & Dering
dehalo=haf.FineDehalo(bm3d_y,thlimi=80,thlima=160,brightstr=0.5,darkstr=0)
dering=haf.HQDeringmod(dehalo,mrad=1,msmooth=1,mthr=58,minp=1,sharp=1,thr=2.8,elast=2.0)
dering=haf.EdgeCleaner(dering,strength=10,rmode=20)
# AA
aa=taa.TAAmbk(dering,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,cycle=1,thin=0,dark=0.15)
aa=core.std.ShufflePlanes([aa,bm3d],[0,1,2],vs.YUV)
# Deband & Sharpen
db1=zvs.xdbcas(aa,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0.1)
db1_y=db1.std.ShufflePlanes(0,vs.GRAY)
blur=haf.MinBlur(db1_y,1)
diff=core.std.MakeDiff(db1_y,blur)
eh=xvs.mwenhance(diff,Strength=1.4,useExpr=True)
merge=core.std.MergeDiff(blur,eh)
cln=haf.EdgeCleaner(merge,strength=16,rmode=20)
cln=haf.FineDehalo(cln,thlimi=80,thlima=160,brightstr=0.4,darkstr=0)
db1=core.std.ShufflePlanes([cln,db1],[0,1,2],vs.YUV)
###
db2=zvs.xdbcas(bm3d,y=[48,36],cb=[36,32],cr=[36,32],mask=True,casstr=0.20)
pt_txt=core.std.MaskedMerge(db1, db2, rs_mask)

# OP
# EP | strat| length
# 02 | 1248 | 2157
# 03 | 1726 | 2159
# 04 |  0   | 2158
# 05 | 792  | 2157
# 06 | 1224 | 2157
# 07 | 2422 | 2157
# 08 | 1224 | 2157

op_start=1224
op_length=2157
src_p=db1[op_start:op_start+op_length]
up_p=pt_txt[op_start:op_start+op_length]
sp_p=db2[op_start:op_start+op_length] # UP

part_a=rekt(src_p,up_p,154,932,748,84)
part=fvf.rfs(src_p,rekt(part_a,up_p,132,880,1684,144),"[69 131]")
part_a=rekt(src_p,up_p,1222,880,320,70)
part=fvf.rfs(part,rekt(part_a,up_p,1656,880,120,70),"[190 255]")
part=fvf.rfs(part,sp_p,"[388 523]") # Special part
part_a=rekt(src_p,up_p,1566,66,252,960)
part=fvf.rfs(part,rekt(part_a,up_p,1592,116,108,316),"[525 591]")
part_a=rekt(src_p,up_p,178,72,1644,956)
part_a=rekt(part_a,up_p,120,140,1644,890)
part_a=rekt(part_a,up_p,348,136,1232,888)
part=fvf.rfs(part,rekt(part_a,up_p,348,70,1356,954),"[642 706]")
part_a=rekt(src_p,up_p,114,68,1546,960)
part=fvf.rfs(part,rekt(part_a,up_p,166,122,1532,310),"[757 821]")
part_a=rekt(src_p,up_p,134,84,1554,938)
part=fvf.rfs(part,rekt(part_a,up_p,444,86,1368,938),"[877 943]")
part_a=rekt(src_p,up_p,1586,68,114,744)
part_a=rekt(part_a,up_p,1584,816,116,70)
part_a=rekt(part_a,up_p,1216,886,376,136)
part_a=rekt(part_a,up_p,1316,816,376,208)
part_a=rekt(part_a,up_p,1358,68,370,818)
part_a=rekt(part_a,up_p,900,132,560,890)
part=fvf.rfs(part,rekt(part_a,up_p,972,70,560,954),"[958 1019]")
part_a=rekt(src_p,up_p,120,76,1646,814)
part_a=rekt(part_a,up_p,350,76,1354,814)
part_a=rekt(part_a,up_p,1360,76,406,814)
part_a=rekt(part_a,up_p,1234,142,506,884)
part=fvf.rfs(part,rekt(part_a,up_p,1584,74,118,812),"[1055 1121]")
part_a=rekt(src_p,up_p,102,264,1484,756)
part_a=rekt(part_a,up_p,274,56,1484,896)
part_a=rekt(part_a,up_p,506,54,1190,754)
part_a=rekt(part_a,up_p,728,260,968,754)
part_a=rekt(part_a,up_p,690,944,88,72)
part=fvf.rfs(part,rekt(part_a,up_p,690,944,88,72),"[1231 1289]")
part_a=rekt(src_p,up_p,726,200,864,830)
part_a=rekt(part_a,up_p,580,262,720,750)
part_a=rekt(part_a,up_p,728,354,820,670)
part_a=rekt(part_a,up_p,628,416,900,610)
part_a=rekt(part_a,up_p,772,480,890,538)
part_a=rekt(part_a,up_p,848,548,660,192)
part_a=rekt(part_a,up_p,1258,764,586,266)
part=fvf.rfs(part,rekt(part_a,up_p,1258,696,628,338),"[1394 1511]")
part_a=rekt(src_p,up_p,830,724,584,298)
part_a=rekt(part_a,up_p,1000,840,584,180)
part_a=rekt(part_a,up_p,1176,960,584,64)
part_a=rekt(part_a,up_p,1406,722,296,294)
part_a=rekt(part_a,up_p,1400,834,210,186)
part_a=rekt(part_a,up_p,1718,810,90,162)
part=fvf.rfs(part,rekt(part_a,up_p,1406,958,290,58),"[1723 1789]")
part_a=rekt(src_p,up_p,754,824,1044,202)
part=fvf.rfs(part,rekt(part_a,up_p,948,824,754,202),"[1824 1890]")
part_a=rekt(src_p,up_p,782,512,1042,504)
part=fvf.rfs(part,rekt(part_a,up_p,922,512,772,502),"[1995 2061]")
part_a=rekt(src_p,up_p,638,560,1188,454)
part=fvf.rfs(part,rekt(part_a,up_p,784,560,634,454),"[2099 2156]") # 同时改！！！！！
part=fvf.rfs(part,rekt(part,up_p,636,972,108,56),"[2111 2156]")
out=db1[:op_start]+part+db1[op_start+op_length:]

preview0=src16
preview1=db1
preview2=src16
preview3=part
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
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
	res=mvf.Depth(out,10)
res.set_output()
src8.set_output(1)