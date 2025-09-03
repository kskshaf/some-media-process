import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs, zvs
import os
from ksksfunc import MRcoref
from dfttest2 import DFTTest
core = vs.core

core.num_threads=4
core.max_cache_size=6000

a = r'/mnt/Disk/BD/Ave_Mujica/BRMM_10924/BDMV/STREAM/00016.m2ts'
src = core.lsmas.LWLibavSource(a)

# clip for psnr check
src_ = core.std.ShufflePlanes(src, 0, vs.GRAY)
src_ = src_.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
edge_fix      =  src_.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
merge_part =  src_.std.BlankClip().std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,255) # For Safety?
src_             =  core.std.MaskedMerge(src_, edge_fix, merge_part)
src_             =  core.std.ShufflePlanes([src_, src], [0, 1, 2], vs.YUV)

# Fix Edge
src16 = core.fmtc.bitdepth(src, bits=16)
src16 = src16.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
src32 = core.fmtc.bitdepth(src16, bits=32)

# Denoise
cb = DFTTest(src32, sigma=6, tbsize=5)
bm3d_b=core.bm3dcpu.BM3Dv2(src32, cb,sigma=[4, 2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32, bm3d_b,sigma=[1.5, 0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)

# Rescale
bm3d_y = core.std.ShufflePlanes(bm3d, 0, vs.GRAY)
rescale_y = MRcoref(bm3d_y, 'Debilinear', h=806, mask_dif_pix=2.7, mthr=[3,3], blur_mask=True, aa_m=2, dehalo=2, brightstr=0.55, dering=1)
e_cln = haf.EdgeCleaner(rescale_y, strength=15, rmode=20)
clip = core.std.ShufflePlanes([e_cln, bm3d], [0, 1, 2], vs.YUV)

# Deband
res  = zvs.xdbcas(clip, y=[48,36], cb=[36,32], cr=[36,32], mask=False, casstr=0)
res  = mvf.Depth(res, depth=10)

res.set_output()
src_.set_output(1)