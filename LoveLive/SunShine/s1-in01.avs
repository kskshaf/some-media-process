a="F:\BDMV\[220329] ラブライブ! サンシャイン!! Blu-ray BOX\BD\Disc 1\BDMV\STREAM\00013.m2ts"
video=LWLibavVideoSource(a)
audio=LWLibavAudioSource(a,av_sync=true)
AudioDub(video,audio)
Trim(29507,33949)