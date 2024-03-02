from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil as vst
import zvs
import muvsfunc as muf
import lvsfunc as lvf
from dfttest2 import DFTTest
#FixBorder
def fixborder(clip):
    fbr=core.std.CropRel(clip,bottom=4)
    fbr=core.edgefixer.Continuity(fbr,top=2,left=5,right=5,radius=24)
    blur1=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur1,left=8,right=8,radius=24)
    fbr=core.std.AddBorders(fbr,bottom=4)
    fbr=core.fb.FillBorders(fbr,bottom=4,interlaced=False,mode='fillmargins')
    blur=core.std.BoxBlur(fbr,planes=0,hradius=1,vradius=2,vpasses=1)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=4,radius=8)
    fbr=core.edgefixer.Reference(fbr,blur,bottom=6,radius=24)
    return fbr
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Special Disc 4\BDMV\STREAM\00006.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)
#src8=core.lsmas.LWLibavSource(a,decoder='h264_qsv')
source=src8#mvf.GetPlane(src8,1)
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
fm=core.tivtc.TFM(src8,order=1,mode=3,cthresh=6)
deint=haf.QTGMC(src8,Preset="Slower",TFF=True)
src8=mvf.FilterCombed(fm,deint)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
src32=src8.fmtc.bitdepth(bits=32)
#FixBorder&Denoise
fb=fixborder(src16)

cb=DFTTest(fb,sigma=3.6,tbsize=5)
mvd=zvs.zmdg(cb,tr=3,thsad=200,truemotion=True,thscd1=300,limit=560,cs=True)

bly=haf.MinBlur(cb.std.ShufflePlanes(0,vs.GRAY),2)
mask=core.tcanny.TCanny(bly,sigma=1,t_h=2,t_l=1.5,mode=0,op=1)
mask=mask.std.Maximum().std.Maximum().std.Minimum().std.Inflate().std.Inflate()
cb32=cb.fmtc.bitdepth(bits=32)

bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb32,sigma=[5,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[2.5,1.2],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
bm3d=core.std.MaskedMerge(mvd,bm3d,mask)
#Dehalo(cv13790595)
halo_f=haf.FineDehalo(vst.get_y(bm3d),showmask=4)
mask_outer=vst.iterate(halo_f,core.std.Maximum,2).std.Inflate()
mask_inner=vst.iterate(mask_outer,core.std.Minimum,3)
halos=core.std.Expr([mask_outer,mask_inner],'x y -')
dehalo=haf.DeHalo_alpha(bm3d,rx=2.0,ry=2.0,darkstr=0.6,brightstr=0.2)
dhaf=core.std.MaskedMerge(bm3d,dehalo,halos)
#Deband for Live
db16=core.neo_f3kdb.Deband(dhaf,15,60,48,48,0,0,sample_mode=4)
db16=mvf.LimitFilter(db16,dhaf,thr=0.6,thrc=0.5,elast=2.5)
dbm=lvf.mask.detail_mask(dhaf,brz_a=0.025,brz_b=0.045)
db16=core.std.MaskedMerge(db16,dhaf,dbm)
#
#part1 [:152021]
#part2 [152021:153085]
#part3 [153085:153302]
#part4 [153302:162794] #24p
#part5 [162794:162952]
#part6 [162952:163764] #24p
#part7 [163764:]
#
st1=153302 #24p
st2=162794 #30p
st3=162952 #24p
st4=163764 #30p
#
#src8=haf.daa(src8)
#path=pathlib.Path(a)
#out=muf.VFRSplice([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14], tcfile=str(path.with_suffix('.tcfile')))
#out=core.std.AssumeFPS(out,fpsnum=114514,fpsden=1000)
#
preview0=src8
preview1=db16
preview2=src8#.resize.Bicubic(1280,720)#(1600,900)
preview3=bm3d
#OKE:DEBUG
Debug=2
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
	res=db16
else:
	res=mvf.Depth(db16,10)
res.set_output()
src8.set_output(1)

