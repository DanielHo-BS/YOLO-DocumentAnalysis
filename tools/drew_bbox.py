import argparse
import cv2
import random
import numpy as np
import os
from tqdm import tqdm

def visualize(imageFile,informFile,saveFlag = False): #給路徑位置
    #image = cv2.imread(imageFile)
    image = cv2.imdecode(np.fromfile(imageFile, dtype=np.uint8), cv2.IMREAD_COLOR) #中文
    h,w,c = image.shape #height width channel
    colorSet = {0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3: (255, 255, 0), 4: (255, 0, 255), 5: (0, 0, 0)}
    #cv2.imshow('mask',image)
    if os.path.exists(opt.save + os.path.basename(imageFile)[:-4] + '.jpg'):
        return None
    with open(informFile,'r') as f:
        for line in f.readlines():
            if len(line.split(' ')) == 1:
                print("Skip line of file:", imageFile)
                continue
            _class,x_center, y_center, box_width, box_height = line.split(' ')
            _class = int(_class)
            x_center = float(x_center)*w
            y_center = float(y_center)*h
            box_width = float(box_width)*w
            box_height = float(box_height)*h
            if _class > 4:
                print(informFile)
                continue

            x1 = int(x_center - box_width/2)
            y1 = int(y_center - box_height/2)
            x2 = int(x_center + box_width/2)
            y2 = int(y_center + box_height/2)

            randomset = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            image = cv2.circle(image, (int(x_center),int(y_center)), 5, colorSet[_class], -1)
            #image = cv2.putText(image, f'({int(x_center)} {int(y_center)} {int(box_width)} {int(box_height)})', (int(x_center) + 5, int(y_center) + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colorSet[_class], 1, cv2.LINE_AA) #cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
            #image = cv2.putText(image, f'(Area {int(box_width*box_height)})', (int(x_center) + 5, int(y_center) + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, randomset , 2, cv2.LINE_AA) #cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
            #image = cv2.rectangle(image, (x1,y1), (x2,y2), randomset, 3)
            image = cv2.rectangle(image, (x1,y1), (x2,y2), colorSet[_class], 3)
            
    #cv2.imshow('mask',image)
    if saveFlag:
        os.makedirs(opt.save,exist_ok = True)
        cv2.imwrite(opt.save + os.path.basename(imageFile)[:-4] + '.jpg', image)
        #cv2.imencode('.jpg', image)[1].tofile(opt.save + os.path.basename(imageFile)[:-4] + '.jpg') #中文
    return image

def main(imageFolder,labelFolder,fileName = None):
    if fileName:
        for imageFile in os.listdir(imageFolder):
            if fileName == imageFile[:-4]:
                imageFile = os.path.join(imageFolder, imageFile)
                break
        for labelFile in os.listdir(labelFolder):
            if fileName == labelFile[:-4]:
                labelFile = os.path.join(labelFolder, labelFile)
                break
        visualize(imageFile,labelFile,True) #給True儲存
        
    else:
        imageList = os.listdir(imageFolder)
        labelList = os.listdir(labelFolder)
        with tqdm(total=len(imageList)) as pbar:
            pbar.set_description('Processing:')
            for imageFile in imageList:
                if imageFile[:-4]+".txt" in labelList:
                    labelFile = os.path.join(labelFolder, imageFile[:-4]+".txt")
                    imageFile = os.path.join(imageFolder, imageFile)
                    visualize(imageFile,labelFile,True) #給True儲存
                else:
                    print("Not find the label: ",imageFile)
                pbar.update(1)


if __name__ in '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--imageFolder', type=str, default="../datasets/old/hand_craft_v10/images/train/", help='ground truth label(s) path')
    parser.add_argument('--labelFolder', type=str, default="../datasets/old/hand_craft_v10/labels/train/", help='prediction label(s) path')
    parser.add_argument('--save', type=str, default="./runs/out/GT/train/", help='save image(s) path')
    opt = parser.parse_args()
    #main(imageFolder,labelFolder,'temp')
    main(opt.imageFolder,opt.labelFolder)