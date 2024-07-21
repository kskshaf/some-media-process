import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import xvs,zvs
import vsTAAmbk as taa
from dfttest2 import DFTTest
core = vs.core
src = core.ffms2.Source(r'E:\Gal\sakura-no-toki\sakuratoki_chs_v1.1\movie\oe45xltvh.dat').fmtc.bitdepth(bits=16)
cb = DFTTest(src, sigma=1.88, tbsize=3)
de = haf.EdgeCleaner(cb, strength=15, rmode=20)
db = zvs.xdbcas(cb,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0)

aa_y = db.std.ShufflePlanes(0,vs.GRAY)
aa_y = taa.TAAmbk(aa_y,aatype=3,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stablize=2,cycle=1)

aa = core.std.ShufflePlanes([aa_y,db],[0,1,2],vs.YUV)
mvf.Depth(aa, depth=10).set_output()