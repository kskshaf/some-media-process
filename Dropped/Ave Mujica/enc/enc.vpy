import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs, zvs
import os
from ksksfunc import MRcoref
from dfttest2 import DFTTest, Backend
core = vs.core

core.num_threads=8
core.max_cache_size=16000

# 判断第几集，并定义源文件路径
#sp = int(os.environ['ENC_SP']) # 在环境变量中定义
sp = 2
bd_base_path = "/mnt/Disk/BD/Ave_Mujica/"
sp_max = 13 # 最大集数

print('\n\n')
if sp >= 1 and sp <= 7:
    a = f"{bd_base_path}BRMM_10924/BDMV/STREAM/000{str(sp - 1 + 16)}.m2ts"
    # print("集数:", sp, '\n', '路径:', a, '\n')
    # 警告！不要在 vpy 里加 print()
elif sp >=8 and sp <= sp_max:
    a = f"{bd_base_path}BRMM_10925/BDMV/STREAM/000{str(sp - 8 + 16)}.m2ts"
    #print("集数:", sp, '\n', '路径:', a, '\n')
else:
    raise ValueError("请输入正确的集数！")

src = core.lsmas.LWLibavSource(a)

# clip for psnr check
src_ = core.std.ShufflePlanes(src, 0, vs.GRAY)
src_ = src_.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
edge_fix      =  src_.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
merge_part    =  src_.std.BlankClip().std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,255) # For Safety?
src_          =  core.std.MaskedMerge(src_, edge_fix, merge_part)
src_          =  core.std.ShufflePlanes([src_, src], [0, 1, 2], vs.YUV)

# Fix Edge
src16 = core.fmtc.bitdepth(src, bits=16)
src16 = src16.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
src32 = core.fmtc.bitdepth(src16, bits=32)

# Denoise
cb = DFTTest(src32, sigma=6, tbsize=5, backend = Backend.CPU())
bm3d_b=core.bm3dcpu.BM3Dv2(src32, cb,sigma=[4, 2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32, bm3d_b,sigma=[1.5, 0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)

# Rescale
bm3d_y = core.std.ShufflePlanes(bm3d, 0, vs.GRAY)
rescale_y = MRcoref(bm3d_y, 'Debilinear', h=806, mask_dif_pix=2.6, mthr=[3,3], blur_mask=True, aa_m=2, dehalo=2, brightstr=1, thlima=200, dering=1, drthr=3, aalimit=[2,10])
e_cln = haf.EdgeCleaner(rescale_y, strength=16, rmode=20)
clip = core.std.ShufflePlanes([e_cln, bm3d], [0, 1, 2], vs.YUV)

# Deband
res  = zvs.xdbcas(clip, y=[48,36], cb=[36,32], cr=[36,32], mask=False, casstr=0)
res  = mvf.Depth(res, depth=10)
res_ed  = zvs.xdbcas(bm3d, y=[48,36], cb=[36,32], cr=[36,32], mask=False, casstr=0)
res_ed  = mvf.Depth(res_ed, depth=10)
# _res_ed  = core.text.Text(res_ed, text="ED", scale=5)

###   BRMM_10924   ###
# 01: None
# 02: 31528-33685
# 03: 31529-33686
# 04: 30856-33013
# 05: 29276-31432
# 06: = 03
# 07: = 03
###   BRMM_10925   ###
# 08: = 03
# 09: = 02
# 10: None
# 11: 31527-33684
# 12: 2542-4698
# 13: None

if sp == 2 or sp == 9:
    ed_start, ed_end = 31528, 33685+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
elif sp == 3 or sp == 6 or sp == 7 or sp == 8:
    ed_start, ed_end = 31529, 33686+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
elif sp == 4:
    ed_start, ed_end = 30856, 33013+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
elif sp == 5:
    ed_start, ed_end = 29276, 31432+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
elif sp == 11:
    ed_start, ed_end = 31527, 33684+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
elif sp == 12:
    ed_start, ed_end = 2542, 4698+1
    res = res[:ed_start] + res_ed[ed_start:ed_end] + res[ed_end:]
else:
    pass

res.set_output()
src_.set_output(1)
