import vapoursynth as vs
import mvsfunc as mvf
import havsfunc as haf
import xvs,zvs
import vsTAAmbk as taa
core = vs.core
core.max_cache_size=9000
#OKE:INPUTFILE
a=r'E:\BD\MV\BDROM\BDMV\STREAM\00005.m2ts'
src8=core.lsmas.LWLibavSource(a,repeat=True)[6953:16204]
ss=src8
#Deinterlaced(stolen from https://vcb-s.nmm-hd.org)
fm=core.tivtc.TFM(src8,order=1,mode=3,cthresh=6)
deint=haf.QTGMC(src8,Preset="Slower",TFF=True,FPSDivisor=2)
src8=mvf.FilterCombed(fm,deint)
src8=core.tivtc.TDecimate(src8)
src8=core.std.SetFieldBased(src8,0)
src16=src8.fmtc.bitdepth(bits=16)
#
cp=core.std.CropRel(src16,top=90,bottom=90)
m_b=core.std.BoxBlur(cp)
cp=core.edgefixer.Reference(cp,m_b,top=4,bottom=4)
cpy=core.std.ShufflePlanes(cp,0,vs.GRAY)
cpy=haf.FineDehalo(cpy,brightstr=0.4,darkstr=0)
cpy=haf.EdgeCleaner(cpy,strength=20,rmode=20)
cpy=taa.TAAmbk(cpy,aatype=3,aarepair=-20,sharp=-0.5,mtype=3,postaa=True,stabilize=0,opencl=True)
cpn=core.std.ShufflePlanes([cpy,cp],[0,1,2],vs.YUV)
blur=haf.MinBlur(cpn,r=1)
cp=zvs.xdbcas(blur,y=[36,24],cb=[24,16],cr=[24,16],mask=True,casstr=0)
cp=core.std.MergeDiff(cp,core.std.MakeDiff(cpn,blur))
#
cpt=core.std.CropRel(src16,bottom=990)
t_b=core.std.BoxBlur(cpt)
cpt=core.edgefixer.Reference(cpt,t_b,bottom=1)
#
cpb=core.std.CropRel(src16,top=990)
b_b=core.std.BoxBlur(cpb)
cpb=core.edgefixer.Reference(cpb,b_b,top=1)
#
stack=core.std.StackVertical([cpt,cp,cpb])
#
output=src8
#
preview0=src16
preview1=stack #1
preview2=src8 #2
preview3=stack #3
#OKE:DEBUG
Debug=0
if Debug==1:
	n=1868
	src1=zvs.n3pv(preview0,scale=1)#[n]
	src2=zvs.n3pv(preview1,scale=1)#[n]
	#src1=mvf.ToRGB(preview0,depth=8)#[n]
	#src2=mvf.ToRGB(preview1,depth=8)#[n]
	cp=core.butteraugli.butteraugli(src1,src2)
	res=core.std.Interleave([src1,src2])
elif Debug==2:
	res=mvf.ToRGB(preview2,depth=8)
elif Debug==3:
	res=mvf.ToRGB(preview3,depth=8)
elif Debug==4:
	res=cpy
else:
	res=mvf.Depth(stack,10)
res.set_output()
src8.set_output(1)