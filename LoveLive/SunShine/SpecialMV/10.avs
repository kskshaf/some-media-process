LoadPlugin("E:\Software\AvisynthRepository\AVSPLUS370_x64\plugins\LSMASHSource.dll")
video=LWLibavVideoSource("F:\BDMV\Special MV Collection\00005.m2ts")
audio=LWLibavAudioSource("E:\BD\MV\BDROM\BDMV\STREAM\00005.wav",av_sync=true)
AudioDub(video,audio)
Trim(69265,81165)