import glob
import argparse
import os
import sys
import time
import shutil
import cv2
import numpy as np

from pathlib import Path
from my_utils import *

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']  # acceptable image suffixes
LABEL_FORMATS = ['txt']  # acceptable image suffixes

class Indicator():
    def __init__(self, image_folder, ground_truth_folder, prediction_folder, save_folder, num_class, error_thre):
        image_folder_path = str(Path(image_folder).resolve())
        ground_truth_folder_path = str(Path(ground_truth_folder).resolve())
        prediction_folder_path = str(Path(prediction_folder).resolve())
        self.save_path = str(Path(save_folder).resolve())
        self.error_thre = error_thre

        image_files = self.check_path(image_folder_path)
        ground_truth_files = self.check_path(ground_truth_folder_path)
        prediction_files = self.check_path(prediction_folder_path)

        self.images = [x for x in image_files if x.split('.')[-1].lower() in IMG_FORMATS]
        self.ground_truth_labels = [x for x in ground_truth_files if x.split('.')[-1].lower() in LABEL_FORMATS]
        self.prediction_labels = [x for x in prediction_files if x.split('.')[-1].lower() in LABEL_FORMATS]

        self.num_class = num_class
        
        self.check()


    def check_path(self, p):
        if '*' in p:
            files = sorted(glob.glob(p, recursive=True))  # glob
        elif os.path.isdir(p):
            files = sorted(glob.glob(os.path.join(p, '*.*')))  # dir
        elif os.path.isfile(p):
            files = [p]  # files
        else:
            raise Exception(f'ERROR: {p} does not exist')
        return files

    def check(self):
        if len(self.images) != len(self.ground_truth_labels):
            raise Exception(f'ERROR: files number don\'t match in ground truth, please check')
        
        if len(self.images) != len(self.prediction_labels):
            raise Exception(f'ERROR: files number don\'t match in prediction, please check')
    
    def get_label_inform(self, path):
        inform = np.loadtxt(path, usecols=range(0,5), dtype=np.float32, ndmin=2) ####不穩定處###
        return inform

    def test_func(self):
        tp_count, fp_count, fn_count =  np.zeros(self.num_class, dtype=np.int32), np.zeros(self.num_class, dtype=np.int32), np.zeros(self.num_class, dtype=np.int32)
        Error_files = []
        for image, ground_truth_label, prediction_label in zip(self.images, self.ground_truth_labels, self.prediction_labels):
            ground_truth_inform = self.get_label_inform(ground_truth_label)
            prediction_inform = self.get_label_inform(prediction_label)

            matrix = calculate_matrix(self.num_class, 0.5, ground_truth_inform, prediction_inform) #confusion matrix
            tp, fp, fn = get_tp_fp_fn(matrix) #class aware
            
            tp_count += tp
            fp_count += fp
            fn_count += fn

        ##############
        # 0314 find the overboxing and underboxing
            if (fp.sum() + fn.sum()) > self.error_thre:
                #print("Boxing Error: ", prediction_label)
                Error_files.append(image)

        if not os.path.exists(self.save_path): 
            os.mkdir(self.save_path)
        for Error_file in Error_files:
            print(Error_file)
            shutil.copyfile(Error_file, self.save_path+ "/"+ Error_file.split("/")[-1])
        #############
        print('True Positive count:', tp_count)
        print('False Positive count:', fp_count, fp_count.sum())
        print('False Nagative count:', fn_count, fn_count.sum()) 
        
        true_positive, false_positive, false_nagative = sum(tp_count),sum(fp_count),sum(fn_count)

        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_nagative)
        F1 = 2 * precision * recall/(precision + recall)

        print('Precision:', precision)
        print('Recall:', recall)
        print('F1-score:', F1)
        
    def __len__(self): #len(Indicator)
        self.check()
        return len(self.images)
    
    def __getitem__(self, index): #Indicator[0] 
        return self.images[index], self.ground_truth_labels[index], self.prediction_labels[index]

def run(ground_truth_path = ROOT / 'data/ground_truth',  # ground truth label(s) path
        prediction_path = ROOT / 'data/prediction', # prediction label(s) path
        source=ROOT / 'data/images',  # image(s) path
        save_path=ROOT / 'data/save',
        num_class = 5,
        error_thre = 5
        ):

    test = Indicator(source, ground_truth_path, prediction_path, save_path, num_class, error_thre)

    test.test_func()






def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ground-truth-path', type=str, default="../datasets/old/hand_craft_v10/labels/val", help='ground truth label(s) path')
    parser.add_argument('--prediction-path', type=str, default="./runs/detect/0307/old_val/labels", help='prediction label(s) path')
    parser.add_argument('--source', type=str, default="../datasets/old/hand_craft_v10/images/val", help='image(s) path')
    parser.add_argument('--save-path', type=str, default="runs/error", help='save image(s) path')
    parser.add_argument('--num-class', type=int, default=5, help='number of class')
    parser.add_argument('--error-thre', type=int, default=5, help='error threshold')
    

    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
