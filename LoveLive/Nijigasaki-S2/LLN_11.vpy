import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
#import vsutil
#import nazobase as nazo
from ksksfunc import CropPart, DBMask, Deband, rescalef_aa, Sharp
import fvsfunc as fvf
import xvs
import zvs
core = vs.core
#OKE:MEMORY
core.max_cache_size=8000
#core.num_threads=16
#OKE:INPUTFILE
a=r'F:\BDMV\LLN S2\Love.Live.Nijigasaki.Gakuen.School.Idol.Doukoukai.S2.Vol6.2022.COMPLETE.BLURAY-KoushinRip\BDROM\BDMV\STREAM\00003.m2ts'
src8=core.lsmas.LWLibavSource(a)
src16=mvf.Depth(src8,16)
src32=mvf.Depth(src8,32)
#
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[4,4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2,2],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
diff=core.std.MakeDiff(src16,bm3d)
#
rs16=rescalef_aa(bm3d,'Debicubic',h=800,b=1/3,c=1/3,mask_dif_pix=2.5,rsmode="znedi3",dering=True,mrad=1.2,mthr=115,csrange=1.2,not_aa=False,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,aacycle=2,dark=0.15,aamask=0)
rs16=haf.FineDehalo(rs16,brightstr=0.8,darkstr=0.4)
rs16=core.std.ShufflePlanes([rs16,bm3d],[0,1,2],vs.YUV)
#last=zvs.xdbcas(rs16,casstr=0.5,sm=4)
rs16=Sharp(rs16,sigma=1,t_h=12,t_l=2.5,mode=1,op=2,br=1,rmode=0,thr=0.6,thrc=0.5,elast=10,showmask=0)
#
txt_mask=xvs.rescalef(bm3d,'Debicubic',h=800,b=1/3,c=1/3,show="mask",mask_dif_pix=2.65)
staff=core.std.MaskedMerge(rs16,bm3d,txt_mask)
staff=haf.EdgeCleaner(staff,strength=20,rmode=18)
#Denoise&Deband
#anmask=nazo.nmask.nazolmask(haf.MinBlur(bm3d),l1=110,h1=120,h2=180,l2=200)
#anmask=haf.MinBlur(anmask).rgvs.RemoveGrain(20)
#aa_mg=core.std.MergeDiff(aa16,diff,0)
#aa16=core.std.MaskedMerge(aa_mg,aa16,anmask)
dbmask=DBMask(rs16)
aa16=Deband(rs16,dbmask,range1=8,range2=15,y1=16,c1=16,r1=16,y2=20,c2=20,r2=20,thr=0.6,thrc=0.5,elast=2.0,first_plane=True)
staff=Deband(staff,dbmask,range1=8,range2=15,y1=16,c1=16,r1=16,y2=20,c2=20,r2=20,thr=0.6,thrc=0.5,elast=2.0,first_plane=True)
snoise=core.std.MergeDiff(aa16,diff,0)
#st_mg=core.std.MergeDiff(staff,diff,0)
#staff=core.std.MaskedMerge(st_mg,staff,anmask)
#ed16=ADN(src16,sigma=[1.5,1.2],radius1=0,block_step=7,bm_range=8,ps_num=2,ps_range=5,x1=58982,y2=48000)
#############STAFF CROP#############
###OP###
op_start = 3693
op_length = 2157 #Remember to change the end frame of the RFS.
op16 = aa16[op_start:op_start+op_length]
staff_t = staff[op_start:op_start+op_length]
snoise_t = snoise[op_start:op_start+op_length]
#op16 = src16[op_start:op_start+op_length]
#staff_t = core.std.BlankClip(op16)
#rs16_tt = staff_t
op_out16=fvf.rfs(op16,CropPart(op16,staff_t,20,60,1300,650),"[373 485]")#373 485
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,50,680,1270,20),"[527 609]")#527 609
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,50,30,850,600),"[646 733]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,1220,360,90,360),"[773 853]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,60,780,1020,2),"[866 979]")
op_out16=fvf.rfs(op_out16,CropPart(op_out16,staff_t,820,2,20,700),"[866 979]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,1150,460,60,2),"[1003 1117]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,20,720,1120,2),"[1133 1215]")
op_out16=fvf.rfs(op_out16,snoise_t,"[1255 1293]")#Strong Noise
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,2,260,450,2),"[1322 1409]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,60,700,1100,40),"[1488 1575]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,60,700,1050,40),"[1597 1683]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,640,630,680,90),"[1724 1835]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,1000,660,40,80),"[1882 1975]")
op_out16=fvf.rfs(op_out16,CropPart(op16,staff_t,120,490,120,490),"[2037 2156]")
#TITLE&ED
out16=fvf.rfs(aa16,CropPart(aa16,staff,1156,940,122,60),"[5863 5993]")#TITLE1
out16=fvf.rfs(out16,bm3d,"[30954 33110]")#ED
out16=fvf.rfs(out16,CropPart(aa16,staff,1402,60,112,944),"[33928 34046]")#TITLE2
#MIX OUTPUT
out16 = out16[:op_start]+op_out16+out16[op_start+op_length:]
#
preview0=src8
preview1=out16
preview2=src8
preview3=out16
#OKE:DEBUG
Debug=1
if Debug==1:
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
else:
	res=mvf.Depth(out16,10)
res.set_output()
src8.set_output(1)