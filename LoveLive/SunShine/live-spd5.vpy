from vapoursynth import core
import vapoursynth as vs
import pathlib
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import mufvfrmod as mfm
import vsutil as vst
import xvs,zvs
import lvsfunc as lvf
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 5\BDMV\STREAM\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
#STAFF
staff=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=2).std.SetFieldBased(0)
staff8=staff
staff=mvf.Depth(staff,10)
#
src8=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=1)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
mvd=zvs.zmdg(src16,tr=2,thsad=210,truemotion=False,thscd1=280,limit=300,cs=True)
src32=mvd.fmtc.bitdepth(bits=32)
#Denoise
cb32=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb32,sigma=[5,2.6],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2.5,1.3],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.4,brightstr=0.1)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
dhaf=haf.EdgeCleaner(dhaf,strength=24,rmode=24)
#Deband for Live
db16=core.neo_f3kdb.Deband(dhaf,15,60,48,48,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
dout=mvf.Depth(db16,10)
#
def nto60p(number):
    return int(number*2)
#
stnum=289600
p0=dout[:nto60p(stnum)]
p1=staff[stnum:]
#path=pathlib.Path(a)
#out=mfm.VFRSplice([p0,p1], tcfile=str(path.with_suffix('.tcfile')), cfr_ref=src8)
clipa = p0 + p1
clipb = src8
fpn = round(clipa.num_frames * clipb.fps.numerator / clipb.num_frames)
fpd = clipb.fps.denominator
out = core.std.AssumeFPS(clipa, fpsnum=fpn, fpsden=fpd)
#out=p0+p1
# Output for RPC.
pc0=src8[:nto60p(stnum)]
pc1=staff8[stnum:]
pcout=pc0+pc1
#[289600:]
###Part for encode
# part1 [:120752]
# part2 [120752:240316]
# part3 [240316:345827]
# part4 [345827:468562]
# part5 [468562:]

#
preview0=src8
preview1=db16
preview2=src8
preview3=staff
#OKE:DEBUG
Debug=0
if Debug==1:
	n=145224
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=mvd
else:
	res=out
res.set_output()
pcout.set_output(1)