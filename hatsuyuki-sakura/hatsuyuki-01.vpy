import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import vsTAAmbk as taa
import xvs,zvs
import nnedi3_resample as nnrs
from dfttest2 import DFTTest
core = vs.core

src = core.ffms2.Source('hatuyuki_op.wmv')
src = src.fmtc.bitdepth(bits=16)
src_y = src.std.ShufflePlanes(0, vs.GRAY)
src_y = core.edgefixer.Continuity(src, left=1, top=1, right=1, bottom=1)
src = core.std.ShufflePlanes([src_y, src], [0, 1, 2], vs.YUV)

cb = DFTTest(src, sigma=3, tbsize=3)
cb = haf.EdgeCleaner(cb, strength=15, rmode=20)

aa_y = cb.std.ShufflePlanes(0, vs.GRAY)
aa_y = taa.TAAmbk(aa_y, aatype=3, aarepair=-20, sharp=-0.5, mtype=3, postaa=True, stablize=2, cycle=1)
aa = core.std.ShufflePlanes([aa_y, cb], [0,1,2], vs.YUV)

up = nnrs.nnedi3_resample(aa, 1920, 1080, nsize=3, qual=2, mode='znedi3', csp=vs.YUV420P16)
db1 = zvs.xdbcas(up, y=[48,36], cb=[36,24], cr=[36,24], mask=True, casstr=0)
db2 = zvs.xdbcas(haf.EdgeCleaner(up, strength=20, rmode=20), y=[48,36], cb=[36,24], cr=[36,24], mask=False, limit=[1, 0.7, 10], casstr=0)

db = db1[:4165] + db2[4165:]
mvf.Depth(db, depth=10).set_output()
