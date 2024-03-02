import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import vsutil
#from ksksfunc import CropPart
import fvsfunc as fvf
import xvs
import zvs
import nnedi3_resample as nnrs
from vsmlrt import DPIR, DPIRModel, Backend
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=10000
core.num_threads=16
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
#flta=DPIR(src,strength=90,model=DPIRModel.drunet_deblocking_color,tiles=1,backend=Backend.OV_CPU())
#fltb=DPIR(src,strength=90,model=DPIRModel.drunet_deblocking_color,tiles=1,backend=Backend.OV_CPU())
#flt=dft
#flt=fvf.rfs(flta,fltb,"[457 510] [534 549]")
#flt=fvf.rfs(flt,src,"[526 528]")

#pa=r'E:\A\floral flowlove.vpy - 1867.png'
#pica=core.imwri.Read(pa)

#flt_pa=core.imwri.Write(flta[28:1680],imgformat='PNG',firstnum=0,filename="F:\\PNG\\flowlove\\%04d.png",quality=0)
#flt_pb=core.imwri.Write(fltb[1680:3332],imgformat='PNG',firstnum=1680,filename="F:\\PNG\\flowlove\\%04d.png",quality=0)
#flt_p=core.std.StackHorizontal([flt_pa,flt_pb])

#Source
a=r'E:\A\floflo_op.mpg'
srca=core.lsmas.LWLibavSource(a)
src=nnrs.nnedi3_resample(srca,nsize=3,qual=2,mode='znedi3',csp=vs.RGB48)
#Pics
pica=core.imwri.Read("F:\\PNG\\flowlove\\%04d.png",0)
picb=core.imwri.Read("F:\\PNG\\flowlove\\%04d.png",1680)
pic=core.std.AssumeFPS(pica+picb,src)
pic=nnrs.nnedi3_resample(pic,csp=vs.RGB48)
pic=src[:28]+pic+src[3332:]
#546-549 551 654 1076-1083 1281-1282 1284-1286 2370-2371 2382-2383 2393-2398 2534
#Banding#2013-2021 2034-2044 2065-2086 2185-2187 2201-2265  2270-2290 2835-2945 3276-3351
#black=core.std.BlankClip(src)
#white=core.std.BlankClip(src,color=[65535,32678,32678])
#DFT
dft=DFTTest(src,sigma=15,tbsize=1)
yuv=yuv_rgb(src,vs.YUV444P16)
dfts1=DFTTest(yuv,sigma=50,tbsize=1)
dfts2=DFTTest(yuv,sigma=80,tbsize=1)
dfts3=DFTTest(yuv,sigma=30,tbsize=1)
#
lmask=zvs.wtfmask(dfts1,nnrs=True,t_l=16,t_h=26,range='limited',op=[1],optc=1,bin=True,bthr=1,sigma=1)
lines=core.std.MaskedMerge(pic,dft,lmask)
#
dfts1=haf.EdgeCleaner(dfts1,rmode=18,strength=20)
dfts1=yuv_rgb(dfts1,vs.RGB48)
dfts2=haf.EdgeCleaner(dfts2,rmode=18,strength=20)
dfts2=yuv_rgb(dfts2,vs.RGB48)
dfts3=haf.EdgeCleaner(dfts3,rmode=18,strength=20)
dfts3=yuv_rgb(dfts2,vs.RGB48)
#
out=fvf.rfs(lines,dfts2,"[546 549] [1076 1079] 2382 2394")
out=fvf.rfs(out,dfts1,"652 2393")
out=fvf.rfs(out,CropPart(dfts3,lines,632,1,1,1),"[1080 1083]")
out=fvf.rfs(out,CropPart(dfts1,lines,632,1,1,1),"1080")
out=fvf.rfs(out,CropPart(lines,dfts1,126,6,1048,606),"551")
out=fvf.rfs(out,CropPart(lines,dfts1,462,136,164,82),"654")
#
out=fvf.rfs(out,CropPart(dfts1,lines,936,238,282,420),"1281 1282")
out=fvf.rfs(out,CropPart(out,lines,1026,306,178,364),"1281 1282")
out=fvf.rfs(out,CropPart(out,lines,996,272,266,424),"1281 1282")
out=fvf.rfs(out,CropPart(out,lines,968,306,270,370),"1281 1282")
out=fvf.rfs(out,CropPart(out,lines,374,1,400,1),"1281 1282")
out=fvf.rfs(out,CropPart(out,lines,816,290,244,298),"1281 1282")
#
out=fvf.rfs(out,CropPart(lines,dfts1,888,188,330,474),"1284 1285")
out=fvf.rfs(out,CropPart(out,dfts1,1016,348,134,290),"[1284 1286]")
#
out=fvf.rfs(out,CropPart(out,dfts2,988,388,12,168),"2371")
out=fvf.rfs(out,CropPart(out,dfts1,191,444,864,1),"2371")
out=fvf.rfs(out,CropPart(out,dfts1,938,196,226,358),"2371")
out=fvf.rfs(out,CropPart(out,dfts1,604,1,488,514),"2371")
#
out=fvf.rfs(out,CropPart(out,dfts1,518,474,724,180),"2383")
#
out=fvf.rfs(out,CropPart(out,dfts2,1,1,926,1),"2396")
out=fvf.rfs(out,CropPart(out,lines,308,176,926,388),"2396")
out=fvf.rfs(out,CropPart(out,dfts2,340,402,816,1),"2396")
out=fvf.rfs(out,CropPart(out,dfts3,614,246,448,378),"2396")
out=fvf.rfs(out,CropPart(out,dfts2,772,100,476,604),"2396")
out=fvf.rfs(out,CropPart(out,dfts2,904,228,318,398),"2396")
out=fvf.rfs(out,CropPart(out,dfts1,1012,86,188,556),"2396")
#
out=fvf.rfs(out,CropPart(out,dfts1,1,190,964,32),"2397")
out=fvf.rfs(out,CropPart(out,lines,100,498,964,32),"2397")
out=fvf.rfs(out,CropPart(out,dfts1,184,106,992,569),"2397")
out=fvf.rfs(out,CropPart(out,dfts1,550,236,444,350),"2397")
out=fvf.rfs(out,CropPart(out,dfts1,272,142,952,490),"2397")
out=fvf.rfs(out,CropPart(out,dfts1,856,148,312,400),"2397")
#
out=fvf.rfs(out,CropPart(out,dfts1,1,90,1224,76),"[2398 2404]")
out=fvf.rfs(out,CropPart(out,dfts1,74,460,1158,88),"2398")
out=fvf.rfs(out,CropPart(out,dfts1,114,584,1088,70),"2398")
out=fvf.rfs(out,CropPart(out,dfts1,68,266,1076,280),"2398")
out=fvf.rfs(out,CropPart(out,dfts1,180,376,1038,252),"2398")
out=fvf.rfs(out,CropPart(out,dfts1,554,170,198,344),"2398")
out=fvf.rfs(out,CropPart(out,dfts1,958,122,236,546),"2398")
out=fvf.rfs(out,CropPart(out,lines,20,516,1194,86),"2398")
#
out=fvf.rfs(out,CropPart(out,dfts1,578,226,312,374),"2399")
#
out=fvf.rfs(out,CropPart(out,dfts1,564,128,312,342),"[2400 2430]")
out=fvf.rfs(out,CropPart(out,dfts1,48,210,1182,360),"2404")
#
out=fvf.rfs(out,CropPart(out,dfts1,702,40,378,438),"2543")
#
out_a=core.imwri.Write(out[:837],imgformat="PNG",filename="E:\\A\\PNG\\a%04d.png",firstnum=0,quality=0)
out_b=core.imwri.Write(out[837:1674],imgformat="PNG",filename="E:\\A\\PNG\\b%04d.png",firstnum=0,quality=0)
out_c=core.imwri.Write(out[1674:2511],imgformat="PNG",filename="E:\\A\\PNG\\c%04d.png",firstnum=0,quality=0)
out_d=core.imwri.Write(out[2511:3348],imgformat="PNG",filename="E:\\A\\PNG\\d%04d.png",firstnum=0,quality=0)
out_pic=core.std.StackHorizontal([out_a,out_b,out_c,out_d])
#out_up=nnrs.nnedi3_resample(out,1920,1080,nsize=3,qual=2,mode='znedi3',csp=vs.RGB48)


preview0=lines
preview1=dft #1
preview2=srca #2
preview3=out #3

Debug=4
if Debug==1:
	n=1372
	src1=mvf.ToRGB(preview0,depth=8)[n]
	src2=mvf.ToRGB(preview1,depth=8)[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=out_pic
else:
	res=mvf.Depth(mix16,10)
res.set_output()