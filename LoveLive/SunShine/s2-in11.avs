a="F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 6\BDMV\STREAM\00012.m2ts"
video=LWLibavVideoSource(a)
audio=LWLibavAudioSource(a,av_sync=true)
AudioDub(video,audio)
Trim(14476,17573)