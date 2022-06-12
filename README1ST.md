# HeroConversion - Hi I'm Sven (@hqqns on Twitter)
Convert images to vintage computer compatible formats - c64 and plus/4 - more comming

PIL or Pillow python library required.

Help is below and in a video - see below

-------------------------------------------------
Create plus/4 image program (prg)
  # ./plus4 <image>
  
Load on original plus/4 or 
  # xplus4 <image>.prg
On the plus/4: 
  SYS 3*4096
-------------------------------------------------
Create c64 image program (prg)
  # ./c64 c <image>
  
This will show a 4x4 matrix of images - each has a diffrent background colour set 
Choose witch looks best (0 to 15) then us it like this:
  # ./c64 w <image> <programname> bg 
  
Load on original Commodore 64 or 
  # x64 <image>
On c64:
  SYS 4096
  
---------------------------------------------------

Video of Instructions:
  
-------------------------------------------------  
  
Follow me on Twitter (@hqqns) to get limited support
