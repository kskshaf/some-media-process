a="F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 3\BDMV\STREAM\00013.m2ts"
video=LWLibavVideoSource(a)
audio=LWLibavAudioSource(a,av_sync=true)
AudioDub(video,audio)
Trim(12363,0)