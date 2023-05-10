import cv2
import numpy as np
import shutil
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path1', type=str, default="./runs/GT/val", help='ground truth label(s) path')
parser.add_argument('--path2', type=str, default="./runs/error", help='prediction label(s) path')
parser.add_argument('--save', type=str, default="./runs/out", help='save image(s) path')
opt = parser.parse_args()

files1 = os.listdir(opt.path1)
files2 = os.listdir(opt.path2)

if not os.path.exists(opt.save):
    os.mkdir(opt.save)

for i in range(len(files1)):
    if files1[i] == "labels" or files1[i] not in files2:
        continue
    fullPath1 = os.path.join(opt.path1,files1[i])
    fullPath2 = os.path.join(opt.path2,files1[i])
    fullSavePath = os.path.join(opt.save,files1[i])

    img1 = cv2.imread(fullPath1)
    img2 = cv2.imread(fullPath2)
    image = np.concatenate((img1, img2), axis=1)
    #cv2.imshow('image', image)
    #cv2.waitKey(0)
    cv2.imwrite(fullSavePath, image)
    print("Combine two images: ",fullSavePath)
    
print("Done!!\n")
