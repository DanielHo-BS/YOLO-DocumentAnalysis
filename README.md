# **YOLO-Document Analysis**

Source code: [Official YOLOv7](https://github.com/WongKinYiu/yolov7)

Implementation of paper - [YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors](https://arxiv.org/abs/2207.02696)

## **Introduction**

Using **``YOLOv7``** for **Document Analysis (Layout)**.

<img src=./images/test1.png width="250" > <img src=./images/prediction1.png width="250" >

<img src=./images/test2.png width="250" > <img src=./images/prediction2.png width="250" >


### [Dataset](https://mailntustedutw-my.sharepoint.com/:u:/g/personal/m11107309_ms_ntust_edu_tw/EbEwBG7yy-pNgnj_ILKRItUBPFeCr4B35VlnMoEpPEVE5w?e=PwPRi7)

* Number of dataset

```text
Without DocLayNet:
Training set: 7006
Validation set: 2936

With DocLayNet:
Training set: 57006
Validation set: 12936
```

* Yaml

```yaml
train: ../datasets/hand_craft_v10/images/train
val: ../datasets/hand_craft_v10/images/val
test: ../datasets/hand_craft_v10/images/test

# number of classes: 
nc: 5

# class names: 
names: [ 'text', 'form', 'image', 'header', 'footer' ]
```

## **Usage**

### Install

```bash
pip install -r requirement.txt
```

### Detect

Download [the weight of model](https://mailntustedutw-my.sharepoint.com/:f:/g/personal/m11107309_ms_ntust_edu_tw/Ep0SVoz2m2dJjCPQkv7SoJQB6lI7ppW-wu2xc5QJmcbimQ?e=aNOFOr)

```bash
python detect.py --weights <weight.pt> --source <images_path>

# --weights weight/yolov7.pt: load the weight of model.
# --source inference/images: input the path of images.
```

The result will be saved to `./runs/exp`.

### Training

```bash
python train.py --device 0,1 --batch-size 16 --weights ./yolov7.pt
# --worker: maximum number of dataloader workers
# --device: cuda device, i.e. 0 or 0,1,2,3 or cpu
# --batch_size: total batch size for all GPUs
# --data: data.yaml path
# --cfg: model.yaml path
# --weights: initial weights path
# --hyp: hyperparameters path
# --project: save to project
# --name: save to project/name
```

### Loss

* IoU: inter / union
* GIoU: iou - (c_area - union) / c_area
* DIoU: iou - rho2 / c2
* CIoU: iou - (rho2 / c2 + v * alpha)
* WIoU: 1 - normalized_wasserstein
* EIoU: iou-(rho2/c2+w_dis/cw2+h_dis/ch2)
* Focal
* SIoU

#### Add new loss

1. Add new loss to ``general.py``.
2. Change loss of **bbox_iou()** from ``loss.py``.

```python
iou = bbox_iou(pbox.T, selected_tbox, x1y1x2y2=False, <which IoU>=True, Focal=False)  
# iou(prediction, target) 預設使用CIoU 方式計算
```

### NMS

* NMS (W/O 不使用torchvision)
* NMS
* Soft NMS
* W/O NMS

Change the nms of ``non_max_suppression_alt``  from ``general.py``.

```python
#i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS 1227 (不使用torchvision)
#i = nms(boxes, scores, iou_thres).to('cuda:0' if torch.cuda.is_available() else 'cpu') # 1227 自訂義nms 排列依面積決定
i = soft_nms(boxes, scores, iou_thres, sigma, score_threshold).to('cuda:0' if torch.cuda.is_available() else 'cpu')
#i = torch.tensor([i for i in range(len(boxes))]).to('cuda:0' if torch.cuda.is_available() else 'cpu') # 無nms 1227 dev
```

#### Add IoU to NMS

Change the IoU of ``box_iou_for_nms`` from ``general.py``.

* GIoU
* DIoU
* CIoU
* SIoU
* EIou

```python
iou = box_iou_for_nms(bboxes[i], bboxes[order[1:]], DIoU=True).squeeze()
```

### Tools

```bash
# Drew the bbox with labels
python tools/drew_bbox.py

# Combine two images in one.
python tools/combin_images.py

# Calculator error IOU
python tools/Indicator/indicator_calculator.py
```

## **Rerence**

[Official YOLOv7](https://github.com/WongKinYiu/yolov7)

[Yoloair](https://github.com/iscyy/yoloair)

[DocLayNet](https://github.com/DS4SD/DocLayNet)

[Augraphy](https://github.com/sparkfish/augraphy)

[YOLOv8](https://github.com/ultralytics/ultralytics/tree/4ac93d82faf3324d18a233090445e83cfac62ce2)
