import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsutil
from ksksfunc import DBMask
import fvsfunc as fvf
import kagefunc as kgf
import xvs
import zvs
import nnedi3_resample as nnrs
#from vsmlrt import DPIR, DPIRModel, Backend
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=10000
# down8d() was written by x_x.
def down8d(clip):
    amp1=clip.fmtc.bitdepth(bits=8,dmode=8,ampo=1.5)
    amp2=clip.fmtc.bitdepth(bits=8,dmode=8,ampo=2)
    dmask=core.std.Expr(clip.std.ShufflePlanes(0,vs.GRAY).fmtc.bitdepth(bits=8),'x 100 > 0 255 ?')
    res_d=core.std.MaskedMerge(amp1,amp2,dmask)
    return res_d
#
def crossfademod(clipa,clipb,start,end):
    #clipa=clipa.text.Text(text='A-A',alignment=7)
    #clipb=clipb.text.Text(text='B-B',alignment=4)
    fd=kgf.crossfade(clipa[start:end+3],clipb[start:end+3],end-start+2)
    #fd=fd.text.Text(text='FD',alignment=1)
    fade=clipa[:start]+fd[:-3]+clipb[end+1:]
    return fade
#
a=r'E:\A\audio\floflo_ed.wmv'
srca=core.lsmas.LWLibavSource(a).std.AssumeFPS(fpsnum=30000,fpsden=1001)
srca=srca.fmtc.bitdepth(bits=16)
#
b=r'E:\A\フローラル・フローラブ\__Unpack__\OMV\floflo_ingame_ed.ogv'
srcb=core.lsmas.LWLibavSource(b).std.AssumeFPS(fpsnum=30000,fpsden=1001)
srcb=core.std.Levels(srcb,min_in=0,max_in=255,min_out=16,max_out=235,planes=[0])
srcb=core.std.Levels(srcb,min_in=0,max_in=255,min_out=16,max_out=240,planes=[1,2])
srcb=srcb.fmtc.bitdepth(bits=16)
#
csp=vs.YUV420P16
srcb_d=DFTTest(srcb,sigma=5,tbsize=1)
srca_d=DFTTest(xvs.getY(srca),sigma=4,tbsize=3)
srcm_d=core.std.ShufflePlanes([srca_d,srcb_d],[0,1,2],vs.YUV)
srcm_d=nnrs.nnedi3_resample(srcm_d,1920,1080,nsize=3,qual=2,mode='znedi3',csp=csp)#
ecl=haf.EdgeCleaner(srcb_d,strength=20,rmode=18)
ecl=nnrs.nnedi3_resample(ecl,1920,1080,nsize=3,qual=2,mode='znedi3',csp=csp)#
fade=crossfademod(ecl,srcm_d,50,70)
#
dbk=DBMask(fade)
db4=core.neo_f3kdb.Deband(fade,8,36,24,24,0,0,sample_mode=2)
db4=core.neo_f3kdb.Deband(db4,15,24,16,16,0,0,sample_mode=2)
db4=mvf.LimitFilter(db4,fade,thr=0.6,thrc=0.5,elast=2.0)
db4=core.std.MaskedMerge(db4,fade,dbk,first_plane=True)
out=db4
out_264=down8d(db4)
#
#srcm=core.std.ShufflePlanes([srca,srcb],[0,1,2],vs.YUV)
#srcm=nnrs.nnedi3_resample(srcm,1920,1080,nsize=3,qual=2,mode='znedi3')#,csp=csp
#
preview0=fade
preview1=db4 #1
preview2=srcb #2
preview3=fade #3
#
Debug=4
if Debug==1:
	n=1868
	src1=mvf.ToRGB(preview0,depth=8)#[n]
	src2=mvf.ToRGB(preview1,depth=8)#[n]
	cp=core.butteraugli.butteraugli(src1,src2)
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