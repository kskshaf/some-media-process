import vapoursynth as vs
core = vs.core
import xvs,zvs
from zvs import nnrs
import mvsfunc as mvf
import havsfunc as haf
import muvsfunc as muf
from functools import partial
import vsTAAmbk as taa
#core.num_threads=16
#OKE:MEMORY
core.max_cache_size=8000
#OKE:INPUTFILE
a=r"F:\BDMV\Kanokon OVA BD\OVA かのこん ～真夏の大謝肉祭・上巻～\BDMV\STREAM\00001.m2ts"
src=core.lsmas.LWLibavSource(a)
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
fm=core.vivtc.VFM(src,order=1,mode=3,cthresh=6)
deint=haf.QTGMC(src,Preset="Slower",TFF=True,FPSDivisor=2)
src8=mvf.FilterCombed(fm,deint)
src8=core.vivtc.VDecimate(src8)
src8=core.std.SetFieldBased(src8,0)
last=src8.fmtc.bitdepth(bits=16)
#Border Fix
src_c=core.std.CropRel(last,right=4)
src_c=core.edgefixer.Continuity(src_c,top=4,right=4,bottom=4,radius=1080)
blur=core.std.BoxBlur(src_c,planes=0,hradius=1,vradius=2,vpasses=1)
src_c=core.edgefixer.Reference(src_c,blur,top=4,right=4,bottom=6)
src_c=core.std.AddBorders(src_c,right=4)
src_c=core.fb.FillBorders(src_c,right=4,mode='fillmargins')
blur=core.std.BoxBlur(src_c,planes=0,hradius=1,vradius=2,vpasses=1)
src_c=core.edgefixer.Reference(src_c,blur,right=4)
last=core.edgefixer.Reference(src_c,blur,right=6)
#(written by x_x)
luma=xvs.getY(last)
luma_de=core.std.SeparateFields(luma,True).fmtc.bitdepth(bits=32)
luma_de=core.descale.Debilinear(luma_de,1280,360)
luma_up=core.std.DoubleWeave(luma_de,True)[::2]
luma_up=core.resize.Bilinear(luma_up,1920,1080).fmtc.bitdepth(bits=16,dmode=1)
mask=core.std.Expr([luma,luma_up],'x y - abs').std.Binarize(28*256)
mask=xvs.expand(mask,cycle=2)
mask=xvs.inpand(mask,cycle=2)
mask=mask.std.Median()
mask=xvs.expand(mask,cycle=7).std.Inflate().std.BoxBlur()
luma_de=core.std.DoubleWeave(luma_de,True)[::2].std.SetFieldBased(0)
luma_rs=nnrs.nnedi3_resample(luma_de,1920,1080).fmtc.bitdepth(bits=16)
luma_rs=core.std.MaskedMerge(luma_rs,luma,mask)
last=core.std.ShufflePlanes([luma_rs,last],[0,1,2],vs.YUV)
last=zvs.zmde(last,thsad=200,truemotion=True,thscd1=250,limit=350,cs=True)
last=xvs.bm3d(last,sigma=[3,2,2],sigma2=[2,1,1],radius=1,preset='lc',mode='cpu',v2=True)#
last=haf.HQDeringmod(last,mthr=60,thr=2,darkthr=1,elast=20,mrad=3,msmooth=5,show=False)
aa=taa.daa(last,opencl=True)
aam=zvs.wtfmask(last,nnrs=0,sigma=1,t_l=36,t_h=42)
aa=core.std.MaskedMerge(last,aa,aam)
last=mvf.LimitFilter(aa,last,thr=1,elast=20,planes=[0])
last=zvs.xdbcas(last,casstr=0,mask=False)
last=last.fmtc.bitdepth(bits=10,dmode=8,patsize=64)
#last=zvs.n3pv(tmp,last,mode='znedi3',scale=1)
last.set_output()
last.set_output(1)