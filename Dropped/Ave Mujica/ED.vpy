import vapoursynth as vs

core = vs.core
core.num_threads=16
core.max_cache_size=9000
a = r'/mnt/Disk/BD/Ave_Mujica/BRMM_10925/BDMV/STREAM/00017.m2ts'
src = core.lsmas.LWLibavSource(a)

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

src.set_output()
