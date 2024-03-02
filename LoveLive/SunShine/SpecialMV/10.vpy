import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
import vsTAAmbk as taa
import fvsfunc as fvf
from dfttest2 import DFTTest
core = vs.core
core.max_cache_size=9000
#OKE:INPUTFILE
a=r'F:\BDMV\Special MV Collection\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)[69265:81166]
src8=core.std.SetFieldBased(src8,0)
src10=mvf.Depth(src8,10)
#
src32=core.fmtc.bitdepth(src8,bits=32)
dft=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,dft,sigma=[6,3],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.5,0.75],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5)
db=zvs.xdbcas(bm3d,y=[36,24],cb=[24,16],cr=[24,16],mask=True,casstr=0)
db=mvf.Depth(db,10)
out=src10[:723]+db[723:]

out.set_output()
src8.set_output(1)