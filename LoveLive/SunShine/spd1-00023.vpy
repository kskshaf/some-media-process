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
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 1\BDMV\STREAM\00023.m2ts'
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
st1=279 # 24p
st2=727 # 30p
st3=833 # 24p
st4=987 # 60p
sta_4=1053 # 24p
st5=1170 # 30p
st6=1996 # 24p
st7=3432 # 30p
st8=3764 # 24p
st9=4448 # 30p
st10=6069 # 24p
st11=6164 # 30p
st12=6490 # 24p
st13=6684 # 30p
st14=6725 # 24p
st15=6996 # 30p
st16=7056 # 24p
st17=7253 # 30p
st18=7430 # 24p
st19=7515 # 30p
st20=14719 # 24p
st21=14875 # 30p
st22=14892 # 24p
st23=17527 # 30p
st24=17605 # 24p
st25=20313 # 30p
st26=24074 # 60p
st27=24210 # 24p
sta_27=24329 # 60p
st28=24343 # 24p
st29=26826 # 60p
st30=27876 # 24p
st31=30321 # 30p
st32=30385 # 60p
st33=30395 # 24p
st34=31345 # 30p
st35=39182 # 24p
st36=42160 # 30p
st37=42341 # 24p
st38=42479 # 30p
#
def nto24p(number):
    return int(number*4/5)
#
def nto60p(number):
    return int(number*2)
#
p0=deint_30p[:st1]
p1=tdec_24p[nto24p(st1):nto24p(st2)]
p2=deint_30p[st2:st3]
p3=tdec_24p[nto24p(st3):nto24p(st4)]
#
p4=deint_60p[nto60p(st4):nto60p(sta_4)]
pa_4=tdec_24p[nto24p(sta_4):nto24p(st5)]
#
p5=deint_30p[st5:st6]
p6=tdec_24p[nto24p(st6):nto24p(st7)]
p7=deint_30p[st7:st8]
p8=tdec_24p[nto24p(st8):nto24p(st9)]
p9=deint_30p[st9:st10]
p10=tdec_24p[nto24p(st10):nto24p(st11)]
p11=deint_30p[st11:st12]
p12=tdec_24p[nto24p(st12):nto24p(st13)]
p13=deint_30p[st13:st14]
p14=tdec_24p[nto24p(st14):nto24p(st15)]
p15=deint_30p[st15:st16]
p16=tdec_24p[nto24p(st16):nto24p(st17)]
p17=deint_30p[st17:st18]
p18=tdec_24p[nto24p(st18):nto24p(st19)]
p19=deint_30p[st19:st20]
p20=tdec_24p[nto24p(st20):nto24p(st21)]
p21=deint_30p[st21:st22]
p22=tdec_24p[nto24p(st22):nto24p(st23)]
p23=deint_30p[st23:st24]
p24=tdec_24p[nto24p(st24):nto24p(st25)]
p25=deint_30p[st25:st26]
p26=deint_60p[nto60p(st26):nto60p(st27)]
#
p27=tdec_24p[nto24p(st27):nto24p(sta_27)]
pa_27=deint_60p[nto60p(sta_27):nto60p(st28)]
#
p28=tdec_24p[nto24p(st28):nto24p(st29)]
p29=deint_60p[nto60p(st29):nto60p(st30)]
p30=tdec_24p[nto24p(st30):nto24p(st31)]
p31=deint_30p[st31:st32]
p32=deint_60p[nto60p(st32):nto60p(st33)]
p33=tdec_24p[nto24p(st33):nto24p(st34)]
p34=deint_30p[st34:st35]
p35=tdec_24p[nto24p(st35):nto24p(st36)]
p36=deint_30p[st36:st37]
p37=tdec_24p[nto24p(st37):nto24p(st38)]
p38=deint_30p[st38:]
#
path=pathlib.Path(a)
out=muf.VFRSplice([p0,p1,p2,p3,p4,pa_4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,pa_27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,p38], tcfile=str(path.with_suffix('.tcfile')))
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
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=out
else:
	res=out
res.set_output()
src8.set_output(1)