import vapoursynth as vs
import sys
import types
from importlib.machinery import SourceFileLoader
core = vs.core

#Load output.
def loadout(sourceScript):
    loader = SourceFileLoader('source', sourceScript)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)
    output = vs.get_output(index = 1).clip
    return output

# Load source & ripped files.
srcpath = "10.vpy"
rippath = "10.hevc"
src = loadout(srcpath)
rip = core.lsmas.LWLibavSource(rippath)

# Print Error if frame number not match.
if src.num_frames != rip.num_frames:
    raise ValueError("Frame numbers not MATCH!")

assert rip.format.color_family in [vs.YUV, vs.GRAY], "only support YUV or Gray input"

def force8bit(clip):
    if clip.format.bits_per_sample == 8:
        return clip
    return clip.resize.Spline64(format=clip.format.replace(bits_per_sample=8).id, dither_type='none')
src = force8bit(src)
rip = force8bit(rip)

# Get the clips in same dimention.
if src.width != rip.width or src.height != rip.height:
    src = src.resize.Bicubic(rip.width, rip.height)

src_planes = [ src.std.ShufflePlanes(i, vs.GRAY) for i in range(src.format.num_planes) ]
rip_planes = [ rip.std.ShufflePlanes(i, vs.GRAY) for i in range(rip.format.num_planes) ]

# runtime function to print psnr value to console.
def callback(n, f):
    print("RPCOUT:", n, ' '.join([ str(p.props.PlanePSNR) for p in f ]), flush=True, file=sys.stdout)
    return rip

# Compare.
cmp_planes = [ core.complane.PSNR(a, b) for (a, b) in zip(rip_planes, src_planes) ]
cmp = core.std.FrameEval(rip, callback, prop_src=cmp_planes)
cmp.set_output()
