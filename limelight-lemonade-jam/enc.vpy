import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import vsTAAmbk as taa
import zvs
from dfttest2 import DFTTest, Backend
core = vs.core

core.num_threads=8
core.max_cache_size=16000

src=core.ffms2.Source('OP.mp4')
src16=core.fmtc.bitdepth(src, bits=16)

# Denoise
cb = DFTTest(src16, sigma=1.8, tbsize=3, backend = Backend.CPU())
de = haf.EdgeCleaner(cb, strength=15, rmode=20)
db = zvs.xdbcas(de, y=[60,36], cb=[48,24], cr=[48,24], mask=False, limit=[1, 0.6, 5], casstr=0.2)

# AA & SP
aa_y = db.std.ShufflePlanes(0, vs.GRAY)
aa_y = taa.TAAmbk(aa_y, aatype=1, aarepair=0, sharp=-0.6, mtype=3, dark=0.1, postaa=True, stabilize=0)
blur = core.rgvs.RemoveGrain(aa_y, 20)
diff = core.std.MakeDiff(aa_y, blur)
cas = core.cas.CAS(aa_y, 0.26)
aa_y = core.std.MaskedMerge(aa_y, cas, diff)
aa_y = haf.FineDehalo(aa_y, thlimi=60, thlima=180, brightstr=0.9, darkstr=0)
aa = core.std.ShufflePlanes([aa_y, db],[0,1,2],vs.YUV)

# To 10bit
clip_a = mvf.Depth(aa, depth=10)
clip_b = mvf.Depth(db, depth=10)

# Fade: 2084~2108
start = 2083
end  = 2109
end = end + 1

n = end - start - 1

cut_a = clip_a[start:end]
cut_b = clip_b[start:end]
out = core.akarin.Expr([cut_a, cut_b], f"N {n} / y * 1 N {n} / - x * +")
out = clip_a[:start] + out + clip_b[end:]

out.set_output(0)
clip_a.set_output(1)
clip_b.set_output(2)
src.set_output(3)
