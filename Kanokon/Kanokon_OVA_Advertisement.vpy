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
a=r"F:\BDMV\Kanokon OVA BD\OVA かのこん ～真夏の大謝肉祭・上巻～\BDMV\STREAM\00008.m2ts"
src=core.lsmas.LWLibavSource(a).fmtc.bitdepth(bits=16)
#Deint
deint=haf.QTGMC(src,Preset="Slower",TFF=True,FPSDivisor=1)
deint=core.std.SetFieldBased(deint,0)
#Border Fix
src_c=core.std.CropRel(deint,right=4)
src_c=core.edgefixer.Continuity(src_c,top=4,right=4,bottom=4,radius=1080)
blur=core.std.BoxBlur(src_c,planes=0,hradius=1,vradius=2,vpasses=1)
src_c=core.edgefixer.Reference(src_c,blur,top=4,right=4,bottom=6)
src_c=core.std.AddBorders(src_c,right=4)
src_c=core.fb.FillBorders(src_c,right=4,mode='fillmargins')
blur=core.std.BoxBlur(src_c,planes=0,hradius=1,vradius=2,vpasses=1)
src_c=core.edgefixer.Reference(src_c,blur,right=4)
last=core.edgefixer.Reference(src_c,blur,right=6)
last=taa.daa(last)
#(by x_x)
last=zvs.zmde(last,thsad=200,truemotion=True,thscd1=250,limit=350,cs=True)
last=xvs.bm3d(last,sigma=[3,2,2],sigma2=[2,1,1],radius=1,preset='lc',mode='cpu',v2=True)#
last=haf.HQDeringmod(last,mthr=60,thr=2,darkthr=1,elast=20,mrad=3,msmooth=5,show=False)
last=zvs.xdbcas(last,casstr=0,mask=False)
last=last.fmtc.bitdepth(bits=10,dmode=8,patsize=64)
#last=zvs.n3pv(deint,last,mode='znedi3',scale=1)
last.set_output()
last.set_output(1)