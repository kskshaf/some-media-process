import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import vsutil
import fvsfunc as fvf
import lvsfunc as lvf
import muvsfunc as muf
import xvs
import zvs
from ksksfunc import DBMask
import nnedi3_resample as nnrs
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=10000
#core.num_threads=16
#
def CropPart(src,src_crop,l=0,t=0,r=0,b=0):
	w=src.width
	h=src.height
	left = core.std.Crop(src,right=w-l)
	right = core.std.Crop(src,left=w-r)
	top = core.std.Crop(src,left=l,right=r,bottom=h-t)
	bottom = core.std.Crop(src,left=l,right=r,top=h-b)
	part = core.std.Crop(src_crop,left=l,right=r,top=t,bottom=b)
	top_mid_bottom = core.std.StackVertical([top,part,bottom])
	right_last = core.std.StackHorizontal([left,top_mid_bottom,right])
	return right_last
def yuv_rgb(srca,csp=vs.RGBS):
	return nnrs.nnedi3_resample(srca,mode='znedi3',csp=csp)
# down8d() was written by x_x.
def down8d(clip):
    amp1=clip.fmtc.bitdepth(bits=8,dmode=8,ampo=1.5)
    amp2=clip.fmtc.bitdepth(bits=8,dmode=8,ampo=2)
    dmask=core.std.Expr(clip.std.ShufflePlanes(0,vs.GRAY).fmtc.bitdepth(bits=8),'x 100 > 0 255 ?')
    res_d=core.std.MaskedMerge(amp1,amp2,dmask)
    return res_d
#Source
a=r'E:\A\floflo_op.mpg'
srca=core.lsmas.LWLibavSource(a)
csp=vs.YUV420P16
src=nnrs.nnedi3_resample(srca,1920,1080,nsize=3,qual=2,mode='znedi3',csp=csp)
#Pics
pica=core.imwri.Read("F:\\PNG\\flowlove\\%04d.png",0)
picb=core.imwri.Read("F:\\PNG\\flowlove\\%04d.png",1680)
pic=core.std.AssumeFPS(pica+picb,src)
pic=nnrs.nnedi3_resample(pic,1920,1080,nsize=3,qual=2,mode='znedi3',csp=csp)
pic=src[:28]+pic+src[3332:]
black=core.std.BlankClip(srca,width=1920,height=1080,format=csp)
white=core.std.BlankClip(srca,width=1920,height=1080,color=[65535,32678,32678],format=csp)
#
out_a=core.imwri.Read(filename="E:\\A\\PNG\\a%04d.png",firstnum=28)
out_b=core.imwri.Read(filename="E:\\A\\PNG\\b%04d.png",firstnum=0)
out_c=core.imwri.Read(filename="E:\\A\\PNG\\c%04d.png",firstnum=0)
out_d=core.imwri.Read(filename="E:\\A\\PNG\\d%04d.png",firstnum=0)
out_pic=out_a+out_b+out_c+out_d
out_up=nnrs.nnedi3_resample(out_pic,1920,1080,nsize=3,qual=2,mode='znedi3',csp=csp).std.AssumeFPS(src)
out_up=black[:28]+out_up+black[3334:]
#
mask3=xvs.mwdbmask(out_up)
mask1=lvf.mask.detail_mask(out_up,brz_a=0.025,brz_b=0.045)
mask2=DBMask(out_up)
#db1
blur=haf.MinBlur(out_up,1)
db1=core.neo_f3kdb.Deband(blur,8,128,120,120,0,0,sample_mode=4)
db1=core.neo_f3kdb.Deband(db1,15,96,84,84,32,0,sample_mode=4)
db1=core.std.MergeDiff(db1,core.std.MakeDiff(out_up,blur))
db1=core.std.MaskedMerge(db1,out_up,mask1)
#db2
db2=core.neo_f3kdb.Deband(out_up,8,96,96,96,0,0,sample_mode=4)
db2=core.neo_f3kdb.Deband(db2,15,48,48,48,0,0,sample_mode=4)
db2=mvf.LimitFilter(db2,out_up,thr=0.6,thrc=0.5,elast=20)
db2=core.std.MaskedMerge(db2,out_up,mask2,first_plane=True)
#db3
db3=core.neo_f3kdb.Deband(blur,6,128,96,96,0,0,sample_mode=4)
db3=core.neo_f3kdb.Deband(db3,15,96,84,84,0,0,sample_mode=4)
db3=core.neo_f3kdb.Deband(db3,8,96,84,84,64,0,sample_mode=4)
db3=core.std.MergeDiff(db3,core.std.MakeDiff(out_up,blur))
db3=core.std.MaskedMerge(db3,out_up,mask1)
#db4
db4=core.neo_f3kdb.Deband(out_up,8,36,24,24,0,0,sample_mode=2)
db4=core.neo_f3kdb.Deband(db4,15,24,16,16,0,0,sample_mode=2)
db4=mvf.LimitFilter(db4,out_up,thr=0.6,thrc=0.5,elast=2.0)
db4=core.std.MaskedMerge(db4,out_up,mask2,first_plane=True)
#Banding#2013-2021 2034-2044 2065-2086 2185-2187 2201-2265  2270-2290 2835-2945 3276-3351
out=fvf.rfs(out_up,db1,"[2013 2021]")
out=fvf.rfs(out,db2,"[2034 2044] [2185 2187] [2270 2290] [3276 3350]")
out=fvf.rfs(out,db3,"[2065 2086]")
out=fvf.rfs(out,db4,"[2201 2265] [2835 2945]")
#for 264
out_264=down8d(out)
#
preview0=out_up
preview1=db2 #1
preview2=srca #2
preview3=out_b #3
#
Debug=4
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
	res=out_264
else:
	res=mvf.Depth(out,10)
res.set_output()