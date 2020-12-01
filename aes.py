from PIL import Image
from Crypto.Cipher import AES
import time
import random
import numpy as np

def AES_Encryption():
    obj = AES.new(AES_key.encode('utf8'), AES.MODE_CBC, AES_IV.encode('utf8'))
    cT = obj.encrypt(imgBytes)

    return cT


def AES_Decryption():
    obj2 = AES.new(AES_key.encode('utf8'), AES.MODE_CBC, AES_IV.encode('utf8'))
    pT = obj2.decrypt(imgBytes)

    return list(pT)


sdef = time.time()
alphaDig = "abcdefghijklmnopqrstuvwxyz0123456789"
chars = len(alphaDig)-1
AES_key = "".join([alphaDig[random.randint(0, chars)] for i in range(16)])
AES_IV = "".join([alphaDig[random.randint(0, chars)] for i in range(16)])

edef = time.time()
se = time.time()
testImg = "./cat.png"
img = Image.open(testImg)
img = img.convert("RGB")
w, h = img.size

rList = []
gList = []
bList = []
for i in range(h):
    for j in range(w):
        R, G, B = img.getpixel((i, j))
        rList.append(R)
        gList.append(G)
        bList.append(B)

imgBytes = bytes(rList)
cT1 = list(AES_Encryption())

imgBytes = bytes(gList)
cT2 = list(AES_Encryption())

imgBytes = bytes(bList)
cT3 = list(AES_Encryption())

height=256
width=256
encryptedImg = Image.new(img.mode, (width, height))
eI = encryptedImg.load()
k = 0
for i in range(width):
    for j in range(height):
        if k < 65536:
            eI[i, j] = (cT1[k], cT2[k], cT3[k])
            k += 1
        else:
            Rx = 255-cT1[-1]
            Gx = 255-cT2[-1]
            Bx = 255-cT3[-1]
            eI[i, j] = (Rx, Gx, Bx)
encryptedImg.save("./encryptedAES_CBC.png")

ee = time.time()

#Decrypt
sd = time.time()

encrypted = Image.open("./encryptedAES_CBC.png")
encrypted = encrypted.convert("RGB")
img=encrypted
w, h = encrypted.size
cR = []
cG = []
cB = []
for i in range(w):
    for j in range(h):
        R, G, B = encrypted.getpixel((i, j))
        cR.append(R)
        cG.append(G)
        cB.append(B)

pTList1, pTList2, pTList3 = cR,cG,cB

origW, origH = img.size
prod = origW*origH

imgBytes = bytes(pTList1)
pR = AES_Decryption()
imgBytes = bytes(pTList2)
pG = AES_Decryption()
imgBytes = bytes(pTList3)
pB = AES_Decryption()

decryptedImg = Image.new("RGB", img.size)
dI = decryptedImg.load()
k = 0
w, h = img.size

for i in range(h):
    for j in range(w):
        dI[i, j] = (pR[k], pG[k], pB[k])
        k += 1
decryptedImg.save('./decryptedAES_CBC.png')
ed = time.time()

defaultTime = edef - sdef
encryptionTime = ee - se
decryptionTime = ed - sd
print("Encryption Time:", round(encryptionTime+defaultTime, 5))
print()
print("Decryption Time:", round(decryptionTime+defaultTime, 5))

