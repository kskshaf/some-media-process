import vapoursynth as vs
import havsfunc as haf
import mvsfunc as mvf
import vsTAAmbk as taa
import ksksfunc as ksf
import fvsfunc as fvf
import xvs
import zvs
core = vs.core
#OKE:MEMORY
core.max_cache_size=9500
#OKE:INPUTFILE
a=r'F:\BDMV\[BDMV][220727][Blend S][BD-BOX]\DISC1\BDMV\STREAM\00007.m2ts'
src=core.lsmas.LWLibavSource(a)
src16=src.fmtc.bitdepth(bits=16)
src32=src.fmtc.bitdepth(bits=32)
#Denoise
tms=core.ttmpsm.TTempSmooth(src32,7,[2,2,2])
bm3d_b=core.bm3dcpu.BM3Dv2(src32,tms,sigma=[5,3],block_step=8,bm_range=7,radius=1,ps_num=2,ps_range=4)
bm3d=core.bm3dcpu.BM3Dv2(src32,bm3d_b,sigma=[1.4,0.8],block_step=7,bm_range=7,radius=1,ps_num=2,ps_range=5).fmtc.bitdepth(bits=16)
#diff=core.std.MakeDiff(src16,bm3d)
#Rescale&EdgeClean
rs=xvs.rescalef(bm3d,kernel='Despline16',h=872.9,mask=True,mask_dif_pix=4.2)
ec=haf.EdgeCleaner(rs,strength=12,rmode=24)
ec=haf.FineDehalo(ec,darkstr=0.0,brightstr=0.4)
#LumaAA
luma_dn=core.std.ShufflePlanes(bm3d,0,vs.YUV)
aa=taa.TAAmbk(luma_dn,aatype=1,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stablize=2)
aa=core.std.ShufflePlanes([aa,bm3d],[0,1,2],vs.YUV)
#Deband
rs=zvs.xdbcas(ec,y=[36,24],cb=[32,18],cr=[32,18],mask=True,casstr=0.5)
aa=zvs.xdbcas(aa,y=[36,24],cb=[32,18],cr=[32,18],mask=True,casstr=0.5)
#Separate OP&ED
res=fvf.rfs(rs,aa,"[864 3020] [30897 32989]")  #
#
preview0=src16 #1
preview1=res #1
preview2=src #2
preview3=aa #3
#GetPlane Preview
get_plane=0
plane=2
if get_plane:
    preview0=mvf.GetPlane(preview0,plane)
    preview1=mvf.GetPlane(preview1,plane)
#OKE:DEBUG
Debug=2
if Debug==1:
	n=1868
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	#cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=res
else:
	res=mvf.Depth(res,10)
res.set_output()
src.set_output(1)