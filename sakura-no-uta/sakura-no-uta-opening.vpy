import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import xvs,zvs
import nnedi3_resample as nnrs
from dfttest2 import DFTTest
core = vs.core
#src = core.lsmas.LWLibavSource(r'E:\Gal\op.mpg')
src = core.ffms2.Source(r'E:\Gal\op.mpg').fmtc.bitdepth(bits=16)
cb = DFTTest(src, sigma=1.2, tbsize=5)
de = haf.EdgeCleaner(cb, strength=20, rmode=20)
up = nnrs.nnedi3_resample(de, 1920, 1080, nsize=3, qual=2, mode='znedi3', csp=vs.YUV420P16)
db = zvs.xdbcas(up,y=[48,36],cb=[36,24],cr=[36,24],mask=True,casstr=0.08)
mvf.Depth(db, depth=10).set_output()