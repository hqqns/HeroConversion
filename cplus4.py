#!/usr/bin/python3

# Convert any image to be Commodore Plus/4 compatible - Creates a prg file - start with SYS 3*1024 
#
# Copyright (C) 2022 CE  Sven Wendler
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


import convlibplus4         as c
from PIL import Image as i
import sys

print (sys.argv[1:])

d=c.conv()
for image in sys.argv[1:]:
    pic=d.load(image)
    canvas=i.new("RGB",(160*4,200*4))
    bc=0
    out=d.conv(pic)
    out=d.showzoomed(out)
    d.writeprg(image+".prg")

    print("Image saved to \n" + image + ".prg")
