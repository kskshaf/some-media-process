import vapoursynth as vs
core = vs.core
import xvs,zvs
from zvs import nnrs
import mvsfunc as mvf
import havsfunc as haf
import muvsfunc as muf
from functools import partial
import vsTAAmbk as taa
core.max_cache_size=8000
a=r"F:\BDMV\Kanokon OVA BD\OVA かのこん ～真夏の大謝肉祭・上巻～\BDMV\STREAM\00001.m2ts"
src=core.lsmas.LWLibavSource(a,repeat=True)#.fmtc.bitdepth(bits=16)
#src=core.text.FrameNum(src)
#(stolen from https://vcb-s.nmm-hd.org)
fm=core.vivtc.VFM(src,order=1,mode=5,cthresh=6)#.text.FrameNum(4)
deint=haf.QTGMC(src,Preset="Slower",TFF=True,FPSDivisor=2)#.text.Text("QTGMC_A",4)
src8=mvf.FilterCombed(fm,deint)
src8=core.vivtc.VDecimate(src8)
src8=core.std.SetFieldBased(src8,0)[:100]

#
last=xvs.ivtc_t(src,order=1,mode=5,pp=lambda x:haf.QTGMC(x,FPSDivisor=2)).std.SetFieldBased(0)[0:100]
#frame: 42-45,64-67,100-101,112-113,
last=zvs.n3pv(src8,last,mode='znedi3',scale=1)
last.set_output()