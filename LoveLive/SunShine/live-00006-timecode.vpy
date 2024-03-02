from vapoursynth import core
import vapoursynth as vs
import pathlib
import vsTAAmbk as taa
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import muvsfunc as muf
from dfttest2 import DFTTest
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00006.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
tdec_24p=core.tivtc.TDecimate(src8).std.SetFieldBased(0)
src8=core.std.SetFieldBased(src8,0)
#
st1=153302 #24p
st2=162794 #30p
st3=162952 #24p
st4=163764 #30p
#
def nto24p(number):
    return int(number*4/5)
#
def nto60p(number):
    return int(number*2)
#
p0=src8[:st1]
p1=tdec_24p[nto24p(st1):nto24p(st2)]
p2=src8[st2:st3]
p3=tdec_24p[nto24p(st3):nto24p(st4)]
p4=src8[st4:]
#
out=muf.VFRSplice([p0,p1,p2,p3,p4], tcfile="E:\\BD\\LoveLiveSunshine\\live\\00006.txt")
out=core.std.AssumeFPS(out,fpsnum=114514,fpsden=1000)
#
preview0=src8
preview1=src8
preview2=src8#.resize.Bicubic(1280,720)#(1600,900)
preview3=src8
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	#src1=mvf.ToRGB(preview0,depth=8)#[n]
	#src2=mvf.ToRGB(preview1,depth=8)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=src8
else:
	res=out
res.set_output()
src8.set_output(1)

