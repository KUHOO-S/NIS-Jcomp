from PIL import Image
import numpy as np
import skimage.measure
colorIm1=Image.open('encryptedAES_ECC.png')
    
entropy1 = skimage.measure.shannon_entropy(colorIm1)
print(entropy1)
colorIm2=Image.open('encryptedAES.png')
    
entropy2 = skimage.measure.shannon_entropy(colorIm2)
print(entropy2)