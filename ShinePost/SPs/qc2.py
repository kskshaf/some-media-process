#!/home/ksks/myenc/bin python3.11
# Original source code is from https://www.nmm-hd.org/newbbs/viewtopic.php?f=23&t=1813

import sys

d_y = {}
d_u = {}
d_v = {}

for l in sys.stdin:
    l = l.strip()
    if not l:
        continue

    parts = l.split(" ")
    if len(parts) != 5:
        continue

    frame, psnr_y , psnr_u, psnr_v = int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])

    if psnr_y < 30:
        #list_y.append(psnr_y)
        #frame_y.append(frame)
        psnr_y = '%s' % (psnr_y)
        d_y.update({psnr_y: frame})

    elif psnr_u < 40:
        psnr_u = '%s' % (psnr_u)
        d_u.update({psnr_u: frame})

    elif psnr_v < 40:
        psnr_v = '%s' % (psnr_v)
        d_v.update({psnr_v: frame})

if d_y == {} and d_u == {} and d_v == {}:
    print("Every planes are OK!!!")

elif d_y != {}:
    print("==============FUCKING_Y==============")
    [print("Frame:", fnm, "PSNR_Y:", list(d_y.keys())[list(d_y.values()).index(fnm)]) for fnm in sorted(d_y.values())]
    print("===================================")

elif d_u != {}:
    print("==============FUCKING_U==============")
    [print("Frame:", fnm, "PSNR_U:", list(d_u.keys())[list(d_u.values()).index(fnm)]) for fnm in sorted(d_u.values())]
    print("===================================")

elif d_v != {}:
    print("==============FUCKING_V==============")
    [print("Frame:", fnm, "PSNR_V:", list(d_v.keys())[list(d_v.values()).index(fnm)]) for fnm in sorted(d_v.values())]
    print("===================================")
#list(d_y.keys())[list(d_y.values()).index(fum)]
#list(d.keys())[list(d.values()).index('12')]
#print(d_y)

