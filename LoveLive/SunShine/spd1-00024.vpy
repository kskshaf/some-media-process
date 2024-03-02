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
#
def wtf(clip):
    src32=core.fmtc.bitdepth(clip,bits=32)
    cb=DFTTest(src32,sigma=3,tbsize=1)
    bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4.8,3.0],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
    bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2.4,1.5],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
    halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
    mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
    mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
    halos=core.std.Expr([mask_outer,mask_inner],'x y -')
    dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.8,brightstr=0.0)
    dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
    db1=core.neo_f3kdb.Deband(dhaf,8,36,24,24,0,0,sample_mode=4)
    db1=core.neo_f3kdb.Deband(db1,15,48,36,36,0,0,sample_mode=4)
    return db1
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 1\BDMV\STREAM\00024.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
source=src8
#
deint_60p=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=1)
deint_30p=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=2)
tdec_24p=core.tivtc.TDecimate(deint_30p).std.SetFieldBased(0)
#
deint_60p=wtf(deint_60p.std.SetFieldBased(0))
deint_60p=mvf.Depth(deint_60p,10)
deint_30p=wtf(deint_30p.std.SetFieldBased(0))
deint_30p=mvf.Depth(deint_30p,10)
tdec_24p=wtf(tdec_24p)
tdec_24p=mvf.Depth(tdec_24p,10)
#
#Trim
#start --- 24p
st1=338     # 60p
st2=776     # 30p
st3=3560    # 24p
st4=33986   # 30p
st5=34596   # 60p
st6=36326   # 30p
st7=36419   # 60p
st8=36424   # 30p
st9=36738   # 60p
st10=36743  # 30p
st11=36849  # 60p
st12=36854  # 30p
st13=37278  # 60p
st14=40788  # 24p
#
def nto24p(number):
    return int(number*4/5)
#
def nto60p(number):
    return int(number*2)
#
p0=tdec_24p[:nto24p(st1)]
p1=deint_60p[nto60p(st1):nto60p(st2)]
p2=deint_30p[st2:st3]
p3=tdec_24p[nto24p(st3):nto24p(st4)]
p4=deint_30p[st4:st5]
p5=deint_60p[nto60p(st5):nto60p(st6)]
p6=deint_30p[st6:st7]
p7=deint_60p[nto60p(st7):nto60p(st8)]
p8=deint_30p[st8:st9]
p9=deint_60p[nto60p(st9):nto60p(st10)]
p10=deint_30p[st10:st11]
p11=deint_60p[nto60p(st11):nto60p(st12)]
p12=deint_30p[st12:st13]
p13=deint_60p[nto60p(st13):nto60p(st14)]
p14=tdec_24p[nto24p(st14):]
#
path=pathlib.Path(a)
out=muf.VFRSplice([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14], tcfile=str(path.with_suffix('.tcfile')))
out=core.std.AssumeFPS(out,fpsnum=114514,fpsden=1000)
#
preview0=deint_30p
preview1=src8
preview2=source#.resize.Bicubic(1600,900)
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

