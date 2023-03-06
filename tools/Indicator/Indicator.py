import os
import cv2
import numpy as np

def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def denormalize(x,w,h): #x是np.array w,h是int就好
    n = np.array([w,h,w,h],dtype = 'int64')
    y = x * n
    return y.astype(dtype = 'int64')

def draw_bbox(image,inform,label_type,class_filter = []): #class_filter = [3,4]
    h,w,c = image.shape #height width channel
    colorSet = {0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3: (50, 150, 255), 4: (50, 255, 150), 5: (255, 150, 50)} #dictionery
    classSet = {0: 'text', 1: 'form', 2: 'image', 3: 'header', 4: 'footer', 5: 'unknown'}
    resultSet = {0: 'FP', 1: 'TP', 2: 'FN', 3: 'TN', 4 :''} #0:FP 1:TP 2:FN 3:TN 4:TP(不顯示)
    resultColorSet = {0: (255,0,255), 1: (0,255,255), 2: (255,255,0), 3 : (0,0,0), 4 : (0,0,0)} #0:洋紅 1:黃色 2:青色
    
    result_flag = False
    if label_type == 'prediction':
        bbox_color = (0, 0, 255) #ground_truth 紅色
        bias = 5
    elif label_type == 'ground_truth':
        bbox_color = (0, 255, 0) #ground_truth 綠色
        bias = -5
    else:
        print(f'unknown label_type {label_type}')
        
    if inform.shape[1] == 5:
        xyxy = xywh2xyxy(inform[:,1:])
        dnxyxy = denormalize(xyxy,w,h)
        
    elif inform.shape[1] == 6:
        xyxy = xywh2xyxy(inform[:,1:5])
        dnxyxy = denormalize(xyxy,w,h)
        result_flag = True
        
    for i,bbox in enumerate(dnxyxy):
            
        x_center = int((bbox[2] + bbox[0])/2)
        y_center = int((bbox[3] + bbox[1])/2)
        _class = int(inform[i,0])

        if _class in class_filter:
            continue
            
        image = cv2.circle(image, (int(x_center),int(y_center)), 5, bbox_color, -1)
        alpha = 0.8
        B_ch,G_ch,R_ch = bbox_color
        
        image[bbox[1]:bbox[3],bbox[0]:bbox[2],0] = image[bbox[1]:bbox[3],bbox[0]:bbox[2],0] * alpha + B_ch * (1 - alpha)
        image[bbox[1]:bbox[3],bbox[0]:bbox[2],1] = image[bbox[1]:bbox[3],bbox[0]:bbox[2],1] * alpha + G_ch * (1 - alpha)
        image[bbox[1]:bbox[3],bbox[0]:bbox[2],2] = image[bbox[1]:bbox[3],bbox[0]:bbox[2],2] * alpha + R_ch * (1 - alpha)
        
        image = cv2.rectangle(image, (bbox[0],bbox[1]), (bbox[2],bbox[3]), bbox_color, 3)
            
        text_string = classSet[_class]        
        image = cv2.rectangle(image, (bbox[0],bbox[1]), (bbox[0] + len(text_string)*20,bbox[1] - bias*6), bbox_color, -1)
        image = cv2.putText(image,
                            text_string,
                            (bbox[0]+5,bbox[1]+10-bias*3),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,0,0),
                            2,
                            cv2.LINE_AA)
        
        if result_flag: #result_flag
            result_string = resultSet[inform[i,5]]
            result_color = resultColorSet[inform[i,5]]
            image = cv2.rectangle(image, (int(x_center),int(y_center)), (int(x_center) + len(result_string)*20,int(y_center) - 30), result_color, -1)
            image = cv2.putText(image,
                            result_string,
                            (int(x_center),int(y_center)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255,0,0),
                            2,
                            cv2.LINE_AA)
    return image

def box_iou(box1, box2):
    # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
    """
    Return intersection-over-union (Jaccard index) of boxes.
    Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
    Arguments:
        box1 (Tensor[N, 4])
        box2 (Tensor[M, 4])
    Returns:
        iou (Tensor[N, M]): the NxM matrix containing the pairwise
            IoU values for every element in boxes1 and boxes2
    """

    def box_area(box):
        # box = 4xn
        return (box[2] - box[0]) * (box[3] - box[1])

    area1 = box_area(box1.T)
    area2 = box_area(box2.T)

    # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
    #inter = (torch.min(box1[:, None, 2:], box2[:, 2:]) - torch.max(box1[:, None, :2], box2[:, :2])).clamp(0).prod(2)
    inter = np.clip((np.minimum(box1[:, None, 2:], box2[:, 2:]) - np.maximum(box1[:, None, :2], box2[:, :2])),0,1).prod(2)
    return inter / (area1[:, None] + area2 - inter)  # iou = inter / (area1 + area2 - inter)

def calculate_matrix(nc,iou_thres,ground_truth_inform,prediction_inform):
    ground_truth_classes = ground_truth_inform[:, 0].astype(int)
    ground_truth_xyxy = xywh2xyxy(ground_truth_inform[:,1:])
    prediction_classes = prediction_inform[:, 0].astype(int)
    prediction_xyxy = xywh2xyxy(prediction_inform[:,1:])

    #0:FP 1:TP 2:FN 3:TN TN沒用(背景)
    temp_inform = np.copy(prediction_inform)
    pad = np.ones((temp_inform.shape[0],1))*0 #FP
    temp_inform = np.append(temp_inform,pad,axis= 1)

    temp_inform_2 = np.copy(ground_truth_inform)
    pad_2 = np.ones((temp_inform_2.shape[0],1))*2 #FN
    temp_inform_2 = np.append(temp_inform_2,pad_2,axis= 1)
    
    matrix = np.zeros((nc + 1, nc + 1))
    
    iou = box_iou(ground_truth_xyxy, prediction_xyxy)
    x = np.where(iou > iou_thres)
    
    if x[0].shape[0]:
        matches = np.concatenate((np.stack(x, 1), iou[x[0], x[1]][:, None]), 1)
        if x[0].shape[0] > 1:
            matches = matches[matches[:, 2].argsort()[::-1]]
            matches = matches[np.unique(matches[:, 1], return_index=True)[1]]
            matches = matches[matches[:, 2].argsort()[::-1]]
            matches = matches[np.unique(matches[:, 0], return_index=True)[1]]
    else:
        matches = np.zeros((0, 3))

    n = matches.shape[0] > 0
    m0, m1, _ = matches.transpose().astype(np.int16) #m0是ground truth index m1是prediction index 相同index對應iou > Thres ex: ground truth[0,1,2,3] prediction[0,1,4,5] 0-0 1-1 2-3 4-5

    for i, gc in enumerate(ground_truth_classes):
        j = m0 == i
        if n and sum(j) == 1:
            matrix[prediction_classes[m1[j]], gc] += 1  # correct TP
            
            if prediction_classes[m1[j]] == gc:
                temp_inform[m1[j],5] = 1 # prediction TP
                temp_inform_2[i,5] = 4 #ground truth TP 
            else:
                temp_inform[m1[j],5] = 0 #class FP
                temp_inform_2[i,5] = 0 #class FP
        else:
            matrix[nc, gc] += 1  # background FP
            temp_inform[m1[j],5] = 0 #background FP
    if n:
        for i, dc in enumerate(prediction_classes):
            if not any(m1 == i):
                matrix[dc, nc] += 1  # background FN

    return matrix,temp_inform,temp_inform_2

def get_tp_fp_fn(matrix):
        tp = matrix.diagonal()  # true positives
        fp = matrix.sum(1) - tp  # false positives
        fn = matrix.sum(0) - tp  # false negatives (missed detections)
        return tp[:-1], fp[:-1], fn[:-1]  # remove background class
    
class Indicator():
    def __init__(self,image_folder,ground_truth_folder,prediction_folder):
        self.image_folder = image_folder
        self.ground_truth_folder = ground_truth_folder
        self.prediction_folder = prediction_folder
        
        self.image_files = os.listdir(image_folder)
        self.ground_truth_files = os.listdir(ground_truth_folder)
        self.prediction_files = os.listdir(prediction_folder)

        self.image_num = len(self.image_files)
        self.ground_truth_num = len(self.ground_truth_files)
        self.prediction_num = len(self.prediction_files)
        
        self.image_formet = 'jpg'
        self.label_formet = 'txt'

        self.nc = 5
        self.iou_thres = 0.5
        self.check()
        
    def check(self):
        
        if self.image_num != self.ground_truth_num:
            print(f'files number don\'t match')
            
        for image_file in self.image_files:
            image_path = os.path.join(self.image_folder,image_file)
            ground_truth_path = os.path.join(self.ground_truth_folder,image_file[:-3] + self.label_formet)
            if not (os.path.isfile(image_path) & os.path.isfile(ground_truth_path)):
                print(f'missing ground truth file {image_file[:-3]}{self.label_formet}')
                
        for ground_truth_file in self.ground_truth_files:
            image_path = os.path.join(self.image_folder,ground_truth_file[:-3] + self.image_formet)
            ground_truth_path = os.path.join(self.ground_truth_folder,ground_truth_file)
            if not (os.path.isfile(image_path) & os.path.isfile(ground_truth_path)):
                print(f'missing image file {ground_truth_file[:-3]}{self.image_formet}')
                
    def check_exist(self,filename):
        image_exist,ground_truth_exist,prediction_exist = False,False,False

        if filename in self.image_files:
            image_exist = True
        if filename[:-3] + self.label_formet in self.ground_truth_files:
            ground_truth_exist = True
        if filename[:-3] + self.label_formet in self.prediction_files:
            prediction_exist = True
        
        return image_exist,ground_truth_exist,prediction_exist
    
    def read_inform(self,index = 0,filename = None,label_type = 'ground_truth'): #'prediction'
        if filename != None:
            if filename in self.image_files:
                index = self.image_files.index(filename)
            else:
                print(f'{filename} not found')
                return 0
        
        image_exist,ground_truth_exist,prediction_exist = self.check_exist(self.image_files[index])
        
        if ground_truth_exist and label_type == 'ground_truth':
            label_path = os.path.join(self.ground_truth_folder,self.image_files[index][:-3] + self.label_formet)
        elif prediction_exist and label_type == 'prediction':
            label_path = os.path.join(self.prediction_folder,self.image_files[index][:-3] + self.label_formet)
        else:
            print(f'error,unknown label_type {label_type} or {filename} not exist')
            return 0

        ret = np.loadtxt(label_path, usecols=range(0,5), dtype=np.float32, ndmin=2) ####不穩定處###
            
        return ret
        
    def visualize(self,index = 0,filename = None,save = False): #temp.draw(index,filename)
        #print(f'{index} {filename}')
        if filename != None:
            if filename in self.image_files:
                index = self.image_files.index(filename)
            else:
                print(f'{filename} not found')
                return 0
            
        image_exist,ground_truth_exist,prediction_exist = self.check_exist(self.image_files[index])

        image_path = os.path.join(self.image_folder,self.image_files[index])
        image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR) #中文路徑
        
        if ground_truth_exist and prediction_exist: #下次應做成5個為ground truth 6個為prediction
            ground_truth_inform = self.read_inform(index,label_type = 'ground_truth')
            prediction_inform = self.read_inform(index,label_type = 'prediction')
            matrix,prediction_inform,ground_truth_inform = calculate_matrix(self.nc,self.iou_thres,ground_truth_inform,prediction_inform) #confusion matrix

            image = draw_bbox(image,ground_truth_inform,'ground_truth') 
            image = draw_bbox(image,prediction_inform,'prediction')
            
            print(matrix)
            tp, fp, fn = get_tp_fp_fn(matrix)
            tp, fp, fn = sum(tp),sum(fp),sum(fn)
            print(tp, fp, fn)
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            F1 = 2 * precision * recall/(precision + recall)
            print(precision,recall,F1)
            image_type = 'all'
            
        elif ground_truth_exist:
            ground_truth_inform = self.read_inform(index,label_type = 'ground_truth')
            image = draw_bbox(image,ground_truth_inform,'ground_truth')
            image_type = 'groun_truth'
            
        elif prediction_exist:
            prediction_inform = self.read_inform(index,label_type = 'prediction')
            image = draw_bbox(image,prediction_inform,'prediction')
            image_type = 'prediction'

        else:
            print('no label exist')
        
        h,w,c = image.shape
        image = cv2.resize(image, (int(w/3),int(h/3)), interpolation=cv2.INTER_AREA)
        cv2.imshow('visualize',image)
        if save:
            os.makedirs('./out',exist_ok = True)
            #cv2.imwrite('./out/' + os.path.basename(imageFile)[:-4] + '_yolov5_visualize.png', image)
            cv2.imencode('.jpg', image)[1].tofile('./out/' + os.path.basename(filename)[:-4] + image_type + '_visualize.png') #中文
        
    def __len__(self): #len(Indicator)
        return len(self.image_files)
    
    def __getitem__(self, index): #Indicator[0]
        return self.image_files[index]
    
def main(image_folder,ground_truth_folder,prediction_folder):
    temp = Indicator(image_folder,ground_truth_folder,prediction_folder)
    #print(len(temp))
    #print(temp[0])
    temp.visualize(filename = 'research3537_010.jpg',save = True)
    
    print('finish')



if __name__ in '__main__':
    ground_truth_folder = r'C:\Users\m1100\Desktop\dev\week29\Indicator calculation\training labels'
    prediction_folder = r'C:\Users\m1100\Desktop\dev\week29\Indicator calculation\prediction of training set'
    image_folder = r'C:\Users\m1100\Desktop\dev\week29\Indicator calculation\training images'
    os.makedirs('./out',exist_ok = True)
    
    main(image_folder,ground_truth_folder,prediction_folder)
    
