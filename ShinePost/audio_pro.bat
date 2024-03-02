@ECHO OFF && CD /D .
set EAC_BIN="D:\OKEGui850\tools\eac3to\eac3to.exe"
set QAAC="D:\OKEGui850\tools\qaac\qaac64.exe"
set EX_DIR="D:\ShinePost\[BDMV][230222][TCBD-1344][シャインポスト][Blu-ray BOX Vol.1]\SHINEPOST_BOX1_DISC2\BDMV\STREAM"
set EX_DIR2="D:\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC1\BDMV\STREAM"
set EX_DIR3="D:\ShinePost\[BDMV][230324][TCBD-1345][シャインポスト][Blu-ray BOX Vol.2 Fin]\SHINEPOST_BOX2_DISC2\BDMV\STREAM"
set OUT_DIR="D:\BD\ShinePost\enc"

::%EAC_BIN% %EX_DIR%\00002.m2ts 2: %OUT_DIR%\04.flac
::%EAC_BIN% %EX_DIR%\00004.m2ts 2: %OUT_DIR%\05.flac
::%EAC_BIN% %EX_DIR%\00005.m2ts 2: %OUT_DIR%\06.flac

::%EAC_BIN% %EX_DIR2%\00002.m2ts 2: %OUT_DIR%\07.flac
::%EAC_BIN% %EX_DIR2%\00004.m2ts 2: %OUT_DIR%\08.flac
::%EAC_BIN% %EX_DIR2%\00005.m2ts 2: %OUT_DIR%\09.flac

::%EAC_BIN% %EX_DIR3%\00002.m2ts 3: 10_2.flac
::%EAC_BIN% %EX_DIR3%\00016.m2ts 3: 11_2.flac
::%EAC_BIN% %EX_DIR3%\00017.m2ts 3: 12_2.flac
::%QAAC% -i -v 320 -q 2 --no-delay -o 12_2.aac 12_2.flac

pause