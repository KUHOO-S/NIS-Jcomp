from PIL import Image
from Crypto.Cipher import AES
import time
import random


def mmi(a0, p):
    return pow(a0, p-2, p)


def pointAdd(Q, G, p):
    if Q == [0, 0]:
        return G
    if G == [0, 0]:
        return Q
    s = (((G[1]-Q[1]) % p)*mmi(G[0]-Q[0], p)) % p
    xNew = (pow(s, 2, p) - ((G[0]+Q[0]) % p)) % p
    yNew = (((s*((Q[0]-xNew) % p)) % p) - (Q[1] % p)) % p
    return [xNew, yNew]


def pointDouble(G, p, a):
    if G[1] == 0:
        return [0, 0]
    s = (((3*pow(G[0], 2, p) + (a % p)) % p)*mmi(2*G[1], p)) % p
    xNew = (pow(s, 2, p) - ((2*G[0]) % p)) % p
    yNew = yNew = (((s*((G[0]-xNew) % p)) % p) - (G[1] % p)) % p
    return [xNew, yNew]


def kTimesG(k, G, p, a):
    Q = [0, 0]
    for i in range(len(k)):
        if k[i] == "1":
            Q = pointAdd(Q, G, p)
        G = pointDouble(G, p, a)
    return [Q[0], Q[1]]


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits


def AES_Encryption():
    obj = AES.new(AES_key.encode('utf8'), AES.MODE_CFB, AES_IV.encode('utf8'))
    cT = obj.encrypt(imgBytes)

    return cT


def AES_Decryption():
    obj2 = AES.new(AES_key.encode('utf8'), AES.MODE_CFB, AES_IV.encode('utf8'))
    pT = obj2.decrypt(imgBytes)

    return list(pT)


def base256OfCiPi(bigIntList, i, Z, flag):
    xi = bigIntList[i]
    yi = bigIntList[i+1]
    if xi == Z[0]:
        ci = pointDouble([xi, yi], p, a)
    else:
        ci = pointAdd([xi, yi], Z, p)

    l0 = numberToBase(ci[0], 256)
    l1 = numberToBase(ci[1], 256)

    if flag == "C":
        if len(l0) < grpSize+1:
            l0.append(0)
        if len(l1) < grpSize+1:
            l1.append(0)
    elif flag == "P":
        if len(l0) == grpSize-1:
            l0.append(0)
        if len(l1) == grpSize-1:
            l1.append(0)

    return l0, l1


def ECC_Encryption():
    # ECC Encryption over AES Encryption
    # encryption ==> POINT ADDITION OF msg M with the computed SSK
    cTList1 = list(cT1)
    cTList2 = list(cT2)
    cTList3 = list(cT3)
    grpList1 = []
    grpList2 = []
    grpList3 = []
    L = len(cTList1)
    for i in range(0, L, grpSize):
        tmp1 = []
        tmp2 = []
        tmp3 = []
        end = min(L, i+grpSize)
        for j in range(i, end):
            tmp1.append(cTList1[j])
            tmp2.append(cTList2[j])
            tmp3.append(cTList3[j])
        grpList1.append(tmp1)
        grpList2.append(tmp2)
        grpList3.append(tmp3)

    bigIntList1 = []
    bigIntList2 = []
    bigIntList3 = []
    for i in range(len(grpList1)):
        g1i = grpList1[i]
        g2i = grpList2[i]
        g3i = grpList3[i]
        d1i = 0
        d2i = 0
        d3i = 0
        for j in range(len(g1i)):
            d1i += g1i[j]*powersOf256[j]
            d2i += g2i[j]*powersOf256[j]
            d3i += g3i[j]*powersOf256[j]
        bigIntList1.append(d1i)
        bigIntList2.append(d2i)
        bigIntList3.append(d3i)

    if len(bigIntList1) % 2 != 0:
        bigIntList1.append(255)
        bigIntList2.append(255)
        bigIntList3.append(255)

    cipherImg1 = []
    cipherImg2 = []
    cipherImg3 = []
    Z = alphaBetaG
    #print(len(bigIntList1))
    for i in range(0, len(bigIntList1), 2):
        # R
        l0, l1 = base256OfCiPi(bigIntList1, i, Z, "C")
        cipherImg1 += l0 + l1

        # G
        l0, l1 = base256OfCiPi(bigIntList2, i, Z, "C")
        cipherImg2 += l0 + l1

        # B
        l0, l1 = base256OfCiPi(bigIntList3, i, Z, "C")
        cipherImg3 += l0 + l1

    return cipherImg1, cipherImg2, cipherImg3


def ECC_Decryption():
    cipherBigList1 = []
    cipherBigList2 = []
    cipherBigList3 = []
    for i in range(0, len(cR), step):
        d1i = 0
        d2i = 0
        d3i = 0
        k = 0
        for j in range(i, i+step):
            d1i += cR[j]*powersOf256[k]
            d2i += cG[j]*powersOf256[k]
            d3i += cB[j]*powersOf256[k]
            k += 1
        cipherBigList1.append(d1i)
        cipherBigList2.append(d2i)
        cipherBigList3.append(d3i)

    cL = len(cipherBigList1)
    pTList1 = []
    pTList2 = []
    pTList3 = []
    Z = [alphaBetaG[0], -1*alphaBetaG[1]]
    for i in range(0, cL, 2):
        # R
        l0, l1 = base256OfCiPi(cipherBigList1, i, Z, "P")
        pTList1 += l0 + l1

        # G
        l0, l1 = base256OfCiPi(cipherBigList2, i, Z, "P")
        pTList2 += l0 + l1

        # B
        l0, l1 = base256OfCiPi(cipherBigList3, i, Z, "P")
        pTList3 += l0 + l1

    return pTList1, pTList2, pTList3


sdef = time.time()
# randomly choose 16 bytes of AES key and IV
alphaDig = "abcdefghijklmnopqrstuvwxyz0123456789"
chars = len(alphaDig)-1
AES_key = "".join([alphaDig[random.randint(0, chars)] for i in range(16)])
AES_IV = "".join([alphaDig[random.randint(0, chars)] for i in range(16)])
# defining ECC params
p = 8948962207650232551656602815159153422162609644098354511344597187200057010413552439917934304191956942765446530386427345937963894309923928536070534607816947
a =6294860557973063227666421306476379324074715770622746227136910445450301914281276098027990968407983962691151853678563877834221834027439718238065725844264138
b =3245789008328967059274849584342077916531909009637501918328323668736179176583263496463525128488282611559800773506973771797764811498834995234341530862286627
x0 =6792059140424575174435640431269195087843153390102521881468023012732047482579853077545647446272866794936371522410774532686582484617946013928874296844351522
y0 =6592244555240112873324748381429610341312712940326266331327445066687010545415256461097707483288650216992613090185042957716318301180159234788504307628509330
G = [x0, y0]
# defining private keys
alpha =bin(9426890448883247745626185743057242473809693764078951663494238777294707070023223798882976159207729119823605850588608460429412647567360897409117209856022401)[2:][::-1]
beta =bin(9619275968248211985332842594956369871234381391917297615810447731933374561248187549880587917558907265126128418967967816764706783230897486752408974005133)[2:][::-1]
# public key of recvr
betaG = kTimesG(beta, G, p, a)
# computing the shared secret key at the sender end
alphaBetaG = kTimesG(alpha, betaG, p, a)
# finding the group Size
grpSize = len(numberToBase(p, 256))-1
# finding powers of 256 till grp size
powersOf256 = [1]
for i in range(1, grpSize+3):
    powersOf256.append(powersOf256[-1]*256)

edef = time.time()
se = time.time()
testImg = "./cat.png"
img = Image.open(testImg)
img = img.convert("RGB")
w, h = img.size
print(w)
print(h)
rList = []
gList = []
bList = []
for i in range(h):
    for j in range(w):
        R, G, B = img.getpixel((i, j))
        rList.append(R)
        gList.append(G)
        bList.append(B)
# R
imgBytes = bytes(rList)
cT1 = AES_Encryption()
# G
imgBytes = bytes(gList)
cT2 = AES_Encryption()
# B
imgBytes = bytes(bList)
cT3 = AES_Encryption()
#print(len(cT3), len(imgBytes))
cR, cG, cB = ECC_Encryption()
lenCi = len(cR)
print(lenCi)
print(len(cG))
height = (lenCi//256)+1
width = 256
#print(height)
#height=20
encryptedImg = Image.new(img.mode, (width, height))
eI = encryptedImg.load()
k = 0
for i in range(width):
    for j in range(height):
        if k < lenCi:
            eI[i, j] = (cR[k], cG[k], cB[k])
            k += 1
        else:
            Rx = 255-cR[-1]
            Gx = 255-cG[-1]
            Bx = 255-cB[-1]
            eI[i, j] = (Rx, Gx, Bx)
encryptedImg.save("./encryptedAES.png")
ee = time.time()
# Decryption
sd = time.time()
step = grpSize+1
encrypted = Image.open("./encryptedAES.png")
encrypted = encrypted.convert("RGB")
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
end = len(cR)
for i in range(len(cR)-1, 0, -1):
    if cR[i-1] == 255-cR[i]:
        end = i
        break

cR = cR[:end]
cG = cG[:end]
cB = cB[:end]
# print(len(cR))

pTList1, pTList2, pTList3 = ECC_Decryption()

#print("pT", len(pTList1), len(pTList2), len(pTList3))
origW, origH = img.size
prod = origW*origH
pTList1 = pTList1[:prod]
pTList2 = pTList2[:prod]
pTList3 = pTList3[:prod]
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
decryptedImg.save('./decryptedAES.png')
ed = time.time()
defaultTime = edef - sdef
encryptionTime = ee - se
decryptionTime = ed - sd
print("Encryption Time:", round(encryptionTime+defaultTime, 5))
print()
print("Decryption Time:", round(decryptionTime+defaultTime, 5))
