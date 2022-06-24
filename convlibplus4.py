# Library to Convert any image to be Commodore Plus/4 compatible - Creates a prg file - start with SYS 3*4096    
# Programs need to be loaded with ,[8 9 10 11],1 then can be started on any plus4 with the command "SYS 3*4096"
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



from PIL import Image as i
from PIL import ImagePalette as ip
from collections import Counter
from math import ceil
import base64

class conv:

    def load(self, filename):
        return i.open(filename)

    def getclosest(self,rgb,pal):
        r=rgb[0]
        g=rgb[1]
        b=rgb[2]
        
        distance=255*255*3
        
        for value in range(256):
            r1=pal[value*3]
            g1=pal[value*3+1]
            b1=pal[value*3+2]
            distr=r1-r
            distb=b1-b
            distg=g1-g
            dist =  distr*distr+distb*distb+distg*distg #maybe give a weighting to green
            print("dist", dist)
            if dist < distance:
                print("distance", distance)
                distance=dist
                color= value

        return color


    def getbest_global(self, pic, pal):
        dithpic=pic.quantize(palette=pal)
        blahpic=pic.quantize(colors=2)
        rgbpal = blahpic.getpalette()
        rgb = (rgbpal[0],rgbpal[1],rgbpal[2])
        a = (self.getclosest(rgb,pal.getpalette()))
        
        rgb = (rgbpal[3],rgbpal[4],rgbpal[5])
        b = (self.getclosest(rgb,pal.getpalette()))
        
        print ("Global colours: ",a,b)
        return (a,b)


    def conv(self, pic,  xsize=160, ysize=200):
        self.xsize=xsize
        self.ysize=ysize

        xs=pic.size[0]
        ys=pic.size[1]
        xns=int(((xs*(ysize/2)/ys)//4)*4)
        yns=int(ysize)

        #print(xns,yns)
        pal=i.open("commodore64-1x.png")

     #1084s bright
        p=[0x00,0x00,0x00,0x27,0x27,0x27,0x60,0x0f,0x10,0x00,0x40,0x3f,0x56,0x04,0x66,0x00,0x4b,0x00,0x1a,0x1a,0x8c,0x35,0x34,0x00,0x53,0x1e,0x00,0x47,0x28,0x00,0x18,0x43,0x00,0x61,0x08,0x34,0x00,0x47,0x1e,0x04,0x29,0x7a,0x28,0x13,0x8f,0x08,0x48,0x00,0x00,0x00,0x00,0x37,0x37,0x37,0x6f,0x1e,0x1f,0x00,0x4f,0x4e,0x65,0x13,0x75,0x04,0x5a,0x05,0x2a,0x2a,0x9c,0x44,0x44,0x00,0x63,0x2e,0x00,0x56,0x38,0x00,0x28,0x52,0x00,0x70,0x17,0x43,0x00,0x56,0x2e,0x14,0x38,0x8a,0x38,0x22,0x9e,0x17,0x58,0x00,0x00,0x00,0x00,0x43,0x43,0x43,0x7c,0x2b,0x2c,0x0b,0x5c,0x5b,0x72,0x20,0x82,0x11,0x67,0x11,0x36,0x37,0xa8,0x51,0x50,0x00,0x6f,0x3a,0x00,0x63,0x44,0x00,0x34,0x5f,0x00,0x7d,0x24,0x50,0x0a,0x63,0x3a,0x21,0x45,0x96,0x45,0x2f,0xab,0x24,0x65,0x00,0x00,0x00,0x00,0x55,0x55,0x55,0x8d,0x3c,0x3d,0x1c,0x6d,0x6c,0x83,0x31,0x93,0x22,0x78,0x22,0x47,0x48,0xb9,0x62,0x61,0x00,0x80,0x4b,0x11,0x74,0x55,0x00,0x45,0x70,0x00,0x8e,0x35,0x61,0x1b,0x74,0x4b,0x32,0x56,0xa7,0x56,0x40,0xbc,0x35,0x76,0x00,0x00,0x00,0x00,0x79,0x79,0x79,0xb2,0x61,0x62,0x40,0x91,0x90,0xa7,0x55,0xb7,0x46,0x9d,0x47,0x6c,0x6c,0xde,0x86,0x86,0x14,0xa5,0x70,0x35,0x99,0x7a,0x22,0x6a,0x94,0x15,0xb3,0x59,0x86,0x3f,0x98,0x70,0x56,0x7b,0xcc,0x7a,0x64,0xe1,0x59,0x9a,0x22,0x00,0x00,0x00,0xa9,0xa9,0xa9,0xe1,0x90,0x91,0x70,0xc1,0xc0,0xd7,0x85,0xe7,0x76,0xcc,0x76,0x9c,0x9c,0xff,0xb6,0xb6,0x44,0xd5,0xa0,0x65,0xc8,0xa9,0x52,0x9a,0xc4,0x45,0xe2,0x89,0xb5,0x6f,0xc8,0xa0,0x86,0xaa,0xfb,0xaa,0x94,0xff,0x89,0xca,0x52,0x00,0x00,0x00,0xc7,0xc7,0xc7,0xff,0xaf,0xb0,0x8f,0xe0,0xdf,0xf6,0xa3,0xff,0x94,0xeb,0x95,0xba,0xba,0xff,0xd4,0xd4,0x62,0xf3,0xbe,0x83,0xe7,0xc8,0x70,0xb8,0xe2,0x63,0xff,0xa7,0xd4,0x8d,0xe7,0xbe,0xa4,0xc9,0xff,0xc8,0xb3,0xff,0xa8,0xe8,0x70,0x00,0x00,0x00,0xfa,0xfa,0xfa,0xff,0xe2,0xe3,0xc2,0xff,0xff,0xff,0xd6,0xff,0xc7,0xff,0xc8,0xed,0xed,0xff,0xff,0xff,0x95,0xff,0xf1,0xb6,0xff,0xfb,0xa3,0xeb,0xff,0x96,0xff,0xda,0xff,0xc0,0xff,0xf1,0xd7,0xfc,0xff,0xfb,0xe6,0xff,0xdb,0xff,0xa3]
        np=[]
        for pees in range(2): 
            np=np+p[:384]
            
        mypal=ip.ImagePalette(palette=np)
        print("mypal",mypal)
        pal.putpalette(np)
        print("pal",pal.getpalette())

        pic=pic.convert("RGB")
        (bc,bc2) = self.getbest_global(pic,pal)
        self.bc=bc
        self.bc2=bc2

        tmppal=pal.copy()

        npic=pic.resize((xns,yns),resample=i.LANCZOS)
        


        canvas= i.new("RGB",(xsize,ysize),(p[3*bc],p[3*bc+1],p[3*bc+2]))

        canvas.paste(npic, (int((xsize-xns)/2),0))
        npic=canvas
        xns=xsize
        
        
        qpic=npic.quantize(palette=pal, colors=128, method=3)
        qref=qpic.copy()

        
        #bitmap mode bit 5 High in $FF06
        # bt 4 hih of $$FF07 for multicolour mode
        #BG0 $FF15
        #BG1 $FF16
        #Border $FF19
        self.bitmapram=bytearray() #location $FF12 Bit2 high for RAM Bits 5 to 3 == bits 15 to 13 of address 8k Bound 0x8000 >> 0100 xxxx xxxx xxxx
        self.lumram=bytearray() #colour ram in char mode bits 7 to 3 of $FF14 == bit 15 to 11 of address 2k bound 
        self.colram=bytearray() #screen ram in char mode added to end of lum ram
        #print("yns=" + str(yns))

        for Y in range(0,yns,8):
            for X in range(0,xns,4):
                colours=[]
                for x in range(4):
                    for y in range(8):
                        colours.append(qpic.getpixel((x+X,y+Y))%384)

                dis=Counter(colours)
                pali=[]
                palr=[]
               
                qu=len(dis.most_common()[:4])
                cs=dis.most_common()[:4]

                pali.append(np[bc*3])
                pali.append(np[bc*3+1])
                pali.append(np[bc*3+2])
                palr.append(bc)
                
               
                for a in dis.most_common():
                    if bc == a[0] or bc2 == a[0]:
                        continue
                    pali.append(np[a[0]*3])
                    pali.append(np[a[0]*3+1])
                    pali.append(np[a[0]*3+2])
                    palr.append(a[0])
                    if len(palr) == 4:
                        break

                pali.append(np[bc2*3])
                pali.append(np[bc2*3+1])
                pali.append(np[bc2*3+2])
                palr.append(bc2)
                lpalr = len(palr)
                
                if lpalr == 1:
                    palr=palr+palr+palr+palr
                elif lpalr == 2:
                    palr=palr+palr
                elif lpalr == 3:
                    palr.append(palr[0])
                
                self.lumram.append(((palr[2]&240)   )| (palr[1]&240) >>4 ) #lum and colour are opp nybbles 
                self.colram.append(((palr[1]&15 )<<4)| (palr[2]&15 )     )
               
                
                epal=[]
                for a in range(ceil(256/qu)):
                    epal += pali

                crop=qpic.crop((X,Y,X+4,Y+8)).convert("RGB")
                tmppal.putpalette(epal[:768])

                crop=crop.quantize(palette=tmppal,method=0,colors=4)

                qref.paste(crop,box=(X,Y))
                npic.paste(crop,box=(X,Y))
                
                for cy in range(8):
                    a=crop.getpixel((0,cy))%4
                    b=crop.getpixel((1,cy))%4
                    c=crop.getpixel((2,cy))%4
                    d=crop.getpixel((3,cy))%4
                    self.bitmapram.append((a<<6)|(b<<4)|(c<<2)|d)
            

        return npic 

    def writeprg(self, filename):
        bin="ADB4rQb/CSCNBv+tB/8JEI0H/60S/wk8KRCNEv+tQF+NFf+tQV+NFv+NGf+pYI0U/w=="
        prog=base64.b64decode(bin)
        g=prog+bytearray(1*4096-len(prog)+2)

        with open(filename, "wb") as f:
            self.bitmapram.append(self.bc)
            self.bitmapram.append(self.bc2)
            self.bitmapram=self.bitmapram+bytearray(8*1024-len(self.bitmapram)) #/ make it 8k
            self.lumram=self.lumram+bytearray(1024-len(self.lumram)) #/ make it 1k
            self.colram=self.colram+bytearray(1024-len(self.colram)) #/ make it 1k
            f.write(g)
            f.write(self.bitmapram)
            f.write(self.lumram)
            f.write(self.colram)

       


    def showzoomed(self,pic):
        zpic=pic.resize((self.xsize*8,self.ysize*4),resample=i.NEAREST)
        zpic.show()
        return zpic


    
