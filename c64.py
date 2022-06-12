#!/usr/bin/python3

# Convert any image to be Commodore c64 compatible - Creates a prg file - start with SYS 4096
#
# Copyright (C) 2022 CE  Sven Wendler @hqqns "8 Bit Hero" on Twitter
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import convlibcal as c
from PIL import Image as i



def showimages(imagename):
    d=c.conv()
    pic=d.load(imagename)

    canvas=i.new("RGB",(160*4,200*4))
    bc=0
    for Y in range(0,200*4,200):
        for X in range (0,160*4,160):
            print(bc)
            out=d.conv(pic,bc)
            bc+=1
            canvas.paste(out,(X,Y))

    canvas=canvas.resize((160*4*4,200*4*2))
    canvas.show()
    #canvas.save("blueeyes_x16.png")


def makeprogname(bg,imagename,progname):
    d=c.conv()
    pic=d.load(imagename)


    out=d.conv(pic,bg)
    d.writeprg(progname+".prg")
    out=d.showzoomed(out)
   # out.save("lagrandejatte.png")

def main():
    if len(sys.argv) < 2:
        
        print("Use in two ways - c to see what the image looks like with each of the 16 background colours")
        print("                - w to write the prg file out for the c64 (bg=background colour 0 t0 15)")
        print("")
        print("Any problems follow me on Twitter and ask for help @hqqns")
        print("")
        print(sys.argv[0] + """ c imagename""")
        print(sys.argv[0] + """ w imagename programname bg | c imagename""")
        exit(1)
    if(sys.argv[1] == 'c'):
            imagename = sys.argv[2]
            showimages(imagename)
    if(sys.argv[1] == 'w'):
        bg = int( sys.argv[4] )
        imagename = sys.argv[2]
        progname = sys.argv[3]
        makeprogname(bg,imagename,progname)

if (__name__ == "__main__"):
    main()


