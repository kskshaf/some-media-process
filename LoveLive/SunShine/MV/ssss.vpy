from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import xvs,zvs
from dfttest2 import DFTTest
#OKE:MEMORY
core.max_cache_size=11000
#OKE:INPUTFILE
a=r'E:\A\[Setsugen] smile smile ship Start! [LACM-24090]\DISC 2\[Setsugen] smile smile ship Start! Animation PV [SUB ENG].mkv'
src8=core.lsmas.LWLibavSource(a,repeat=True)
src8=core.std.SetFieldBased(src8,0)
src16=core.fmtc.bitdepth(src8,bits=16)
src32=core.fmtc.bitdepth(src8,bits=32)
#Denoise
cb=DFTTest(src32,sigma=5,tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4,2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1,0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#AA
aa_y=core.std.ShufflePlanes(bm3d,0,vs.GRAY)
aa_y=taa.TAAmbk(aa_y,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,cycle=0)
aa=core.std.ShufflePlanes([aa_y,bm3d],[0,1,2],vs.YUV)
#Deband
db1=zvs.xdbcas(aa,mask=True,casstr=0)
db1=mvf.Depth(db1,10)
db2=zvs.xdbcas(bm3d,mask=True,casstr=0)
db2=mvf.Depth(db2,10)
out10=db2[:600]+db1[600:7226]+db2[7226:7824]
#
preview0=src8
preview1=aa
preview2=src8
preview3=out10
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1372
	src1=mvf.ToRGB(preview0,depth=8)
	src2=mvf.ToRGB(preview1,depth=8)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
	#res=core.text.ClipInfo(res)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	src8=src8[1456]+src8[2656]+src8[3564]+src8[6666]
else:
	res=out10
res.set_output()
src8[:7824].set_output(1)