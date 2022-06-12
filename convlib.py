from PIL import Image as i
from collections import Counter
from math import ceil
import base64

class conv:

    def load(self, filename):
        return i.open(filename)

    def conv(self, pic, bc, xsize=160, ysize=200):
        self.bc=bc        
        self.xsize=xsize
        self.ysize=ysize

        xs=pic.size[0]
        ys=pic.size[1]
        xns=int(((xs*(ysize/2)/ys)//4)*4)
        yns=int(ysize)

        #print(xns,yns)
        pal=i.open("commodore64-1x.png")

        p=pal.getpalette()
        p=[0, 0, 0, 255, 255, 255, 104, 55, 43, 112, 164, 178, 111, 61, 134, 88, 141, 67, 53, 40, 121, 184, 199, 111, 111, 79, 37, 67, 57, 0, 154, 103, 89, 68, 68, 68, 108, 108, 108, 154, 210, 132, 108, 94, 181, 149, 149, 149]
        #adapted from http://unusedino.de/ec64/technical/misc/vic656x/colors/


        canvas= i.new("RGB",(xsize,ysize),(p[3*bc],p[3*bc+1],p[3*bc+2]))

        npic=pic.resize((xns,yns),resample=i.LANCZOS)
        canvas.paste(npic, (int((xsize-xns)/2),0))
        npic=canvas
        xns=xsize
        
        np=[]

        for pees in range(16):
            np=np+p[:16*3]
            
        pal.putpalette(np)
        tmppal=pal.copy()

        qpic=npic.quantize(palette=pal, colors=16, method=3)
        qref=qpic.copy()

       # print(np)
        
        self.bitmapram=bytearray()
        self.colourram=bytearray()
        self.screenram=bytearray()
        #print("yns=" + str(yns))

        for Y in range(0,yns,8):
            for X in range(0,xns,4):
            #    print(X,Y)
                colours=[]
                for x in range(4):
                    for y in range(8):
                        colours.append(qpic.getpixel((x+X,y+Y))%16)

                dis=Counter(colours)
                pali=[]
                palr=[]
               
                qu=len(dis.most_common()[:4])
                cs=dis.most_common()[:4]
                #print(qu,cs)

                for a in dis.most_common()[:4]:
                    if bc is a[0]:
                        use=4
                    else:
                        use=3
                pali.append(np[bc*3])
                pali.append(np[bc*3+1])
                pali.append(np[bc*3+2])
                palr.append(bc)
                
                for a in dis.most_common():
                    if bc == a[0]:
                        continue
                    pali.append(np[a[0]*3])
                    pali.append(np[a[0]*3+1])
                    pali.append(np[a[0]*3+2])
                    palr.append(a[0])
                    if len(palr) == 4:
                        break
                lpalr = len(palr)
                if lpalr == 1:
                    palr=palr+palr+palr+palr
                elif lpalr == 2:
                    palr=palr+palr
                elif lpalr == 3:
                    palr.append(palr[0])

                self.colourram.append(palr[3])
                self.screenram.append((palr[1]<<4)|palr[2])
               
                
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
        bin="ABCtEEeNINCNIdCiAL1AP50ABL1AQJ0ABb1AQZ0ABr1AQp0AB70oQ50A2L0oRJ0A2b0oRZ0A2r0oRp0A2+jQzak7jRHQqRiNFtCpGI0Y0ExNEA=="
        prog=base64.b64decode(bin)
        g=prog+bytearray(4096-len(prog))

        header=bytearray.fromhex('0020')
        with open(filename, "wb") as f:
            f.write(g)
            f.write(header)
            f.write(self.bitmapram)
            f.write(self.screenram)
            f.write(self.colourram)
            n=bytearray()
            n.append(self.bc)
            f.write(n)
 #           self.writebin(filename)

    def writebin(self, filename):
        with open("bitmap_"+filename, "wb") as f:
            f.write(self.bitmapram)
        with open("screen_"+filename, "wb") as f:
            f.write(self.screenram)
        with open("colour_"+filename, "wb") as f:
            f.write(self.colourram)
        with open("bg_"+filename, "wb") as f:
            n=bytearray()
            n.append(self.bc)
            f.write(n)

    def writereu(self,filename):
        with open(filename, "wb") as f:
                f.write(bytes(2**16*32*8))
                f.seek(2**16*2)#back 1
                f.write(self.bitmapram)

                f.seek(2**16*3)#back 1
                f.write(self.screenram)
                f.seek(2**16*4)#back 2
                f.write(self.colourram)
                n=bytearray()
                n.append(self.bc)
                f.write(n)




    def showzoomed(self,pic):
        zpic=pic.resize((self.xsize*8,self.ysize*4),resample=i.NEAREST)
        zpic.show()
        return zpic


    
