import cv2
import numpy as np
import shutil
import os

PATH1 = "./runs/GT"
PATH2 = "./runs/error/FEIoU"
SAVEPATH = "./runs/out/GT_FEIoU_Error"

files1 = os.listdir(PATH1)
files2 = os.listdir(PATH2)

if not os.path.exists(SAVEPATH):
    os.mkdir(SAVEPATH)

for i in range(len(files1)):
    if files1[i] == "labels" or files1[i] not in files2:
        continue
    fullPath1 = os.path.join(PATH1,files1[i])
    fullPath2 = os.path.join(PATH2,files1[i])
    fullSavePath = os.path.join(SAVEPATH,files1[i])

    img1 = cv2.imread(fullPath1)
    img2 = cv2.imread(fullPath2)
    image = np.concatenate((img1, img2), axis=1)
    #cv2.imshow('image', image)
    #cv2.waitKey(0)
    cv2.imwrite(fullSavePath, image)
    print("Combine two images: ",fullSavePath)
    
print("Done!!\n")
