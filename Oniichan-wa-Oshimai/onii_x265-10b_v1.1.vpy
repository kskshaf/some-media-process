import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import xvs
import zvs
from dfttest2 import DFTTest
core = vs.core
core.num_threads=16
core.max_cache_size=10000
#OKE:INPUTFILE
a=r'E:\Bangumi BT\[Ioroid] Oniichan wa Oshimai! - 01 [ABEMA WEB-DL 1080p AVC AAC].mkv'
src8=core.lsmas.LWLibavSource(a)
#
flt=mvf.Depth(src8,32)
dft=DFTTest(flt,sigma=2,tbsize=1)
bm3d_b=core.bm3dcpu.BM3Dv2(flt,dft,sigma=[5,4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(flt,bm3d_b,sigma=[1.6,1.0],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5)
src=xvs.rescalef(bm3d,'Debicubic',h=844,b=0.33,c=0.33,mask_dif_pix=2)
src=haf.FineDehalo(src,brightstr=0.4,darkstr=0)
src=haf.EdgeCleaner(src,strength=20,rmode=20)
src=zvs.xdbcas(src,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0.5)
src=mvf.Depth(src,10)
#
src.set_output()
src8.set_output(1)