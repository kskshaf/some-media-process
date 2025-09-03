import vapoursynth as vs
import mvsfunc as mvf
import muvsfunc as muf
import havsfunc as haf
from ksksfunc import MRcoref, ContraDering
from dfttest2 import DFTTest
core = vs.core

core.num_threads=16
core.max_cache_size=9000
a = r'/mnt/Disk/BD/Ave_Mujica/BRMM_10924/BDMV/STREAM/00017.m2ts'
src = core.lsmas.LWLibavSource(a)

src16=core.fmtc.bitdepth(src, bits=16)
src32=core.fmtc.bitdepth(src, bits=32)
#Denoise
cb=DFTTest(src32,sigma=5,tbsize=5)
#tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,cb,sigma=[4, 2.4],block_step=8,bm_range=7,radius=0,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1, 0.6],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
src = core.std.ShufflePlanes(bm3d, 0, vs.GRAY)

abc=0
show_dm=False

if abc:
    show='mask'
else:
    show='result'

#rs_mask=MRcoref(src,'Debilinear', h=806,show=show, blur_mask=0)#mask_dif_pix=2.6,mthr=[6,5],
rs_mask=MRcoref(src, 'Debilinear', h=806, mask_dif_pix=2.6, mthr=[3,3], blur_mask=True, aa_m=2, dehalo=2, brightstr=0.5, dering=1, drthr=2)
rs_mask2=MRcoref(src, 'Debilinear', h=806, mask_dif_pix=2.6, mthr=[3,3], blur_mask=True, aa_m=2, dehalo=2, brightstr=1.2, thlima=220, dering=1, drthr=2, aalimit=[2,10])
#rs_mask3=MRcoref(src, 'Debilinear', h=806, mask_dif_pix=2.6, mthr=[3,3], blur_mask=True, aa_m=2, dehalo=2, brightstr=1.2, thlima=220, dering=1, drthr=3.6, muf_dr_thr=2, cdr_mrad=1, cdr_mthr=110, cdr_csrange=1, cdr_rpmode=23, cdr_thr=100, cdr_elast=2.5, aalimit=[2,10])
rs_mask3=haf.MinBlur(rs_mask2,1)
#haf.EdgeCleaner(rs_mask2, strength=15, rmode=18)
#ContraDering(rs_mask2, mrad=1.2, mthr=115, csrange=1, rpmode=23)
#haf.HQDeringmod(rs_mask2, show=True, mrad=1.2, mthr=115)
rs_mask4=ContraDering(rs_mask2, mrad=1, mthr=110, csrange=1, rpmode=23)
rs_mask4=mvf.LimitFilter(rs_mask4, rs_mask2, thr=3, elast=3)
rs_mask5=haf.HQDeringmod(rs_mask2, show=True, mrad=1.2, mthr=115)

#rs_mask3=muf.mdering(rs_mask2,thr=15)
#rs_mask2=haf.EdgeCleaner(rs_mask2, strength=20, rmode=20)
#rs_mask2=haf.FineDehalo(rs_mask2, thlimi=60, thlima=150, brightstr=1, darkstr=0)

#src_ = core.std.ShufflePlanes(src16, 0, vs.GRAY)
src_ = bm3d
rs_mask = core.std.ShufflePlanes([rs_mask, bm3d], [0, 1, 2], vs.YUV)
rs_mask2 = core.std.ShufflePlanes([rs_mask2, bm3d], [0, 1, 2], vs.YUV)

if show_dm:
    pass
else:
    rs_mask3 = core.std.ShufflePlanes([rs_mask3, bm3d], [0, 1, 2], vs.YUV)
    rs_mask4 = core.std.ShufflePlanes([rs_mask4, bm3d], [0, 1, 2], vs.YUV)

#rs_mask3 = core.std.ShufflePlanes([rs_mask3, bm3d], [0, 1, 2], vs.YUV)
#edge_fix      =  src_.edgefixer.Continuity(left=2, top=2, right=2, bottom=2)
#merge_part =  src_.std.BlankClip().std.CropRel(2,2,2,2).std.AddBorders(2,2,2,2,65535) # For Safety?
#src               =  core.std.MaskedMerge(src_, edge_fix, merge_part)

src1 = mvf.ToRGB(rs_mask2, depth=8)
src2 = mvf.ToRGB(rs_mask3, depth=8)
compare = core.butteraugli.butteraugli(src1, src2)

src16.set_output()
rs_mask.set_output(1)
rs_mask2.set_output(2)
rs_mask3.set_output(3)
rs_mask4.set_output(4)
compare.set_output(5)