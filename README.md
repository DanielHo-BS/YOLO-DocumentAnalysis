# **YOLO-Document Analysis**

Source code: [Official YOLOv7](https://github.com/WongKinYiu/yolov7)

Implementation of paper - [YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors](https://arxiv.org/abs/2207.02696)

## **Introduction**

Using **``YOLOv7``** for **Document Analysis**.

### [Dataset](https://mailntustedutw-my.sharepoint.com/:u:/g/personal/m11107309_ms_ntust_edu_tw/EbEwBG7yy-pNgnj_ILKRItUBPFeCr4B35VlnMoEpPEVE5w?e=PwPRi7)

* Number of dataset

```text
Training: 5018
Validation: 1157
Testing: 316
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

Download [the weight of model](https://mailntustedutw-my.sharepoint.com/:u:/g/personal/m11107309_ms_ntust_edu_tw/EXOa0iMb3KxFpnbe3EUcSvIB5Wlc_UUFqf1XuIz6SfMqcA?e=L75e9B)

```bash
python detect.py --weights <weight.pt> --source <images_path>

# --weights weight/yolov7.pt: load the weight of model.
# --source inference/images: input the path of images.
```

The result will be saved to `./runs/exp`.

### Training

```bash
python train.py --workers 1 --device 0 --batch-size 8 --data data/pdf_dataset.yaml --cfg cfg/training/yolov7_fix_anchor.yaml --weights 'yolov7.pt' --name exp --hyp data/hyp.scratch.p5.mosaic.0.5_custom_augmentation_scale_0.5.yaml --project runs/train

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

```test
IoU: inter / union
GIoU: iou - (c_area - union) / c_area
DIoU: iou - rho2 / c2 
CIoU: iou - (rho2 / c2 + v * alpha) 
WIoU: 1 - normalized_wasserstein
EIoU: iou-(rho2/c2+w_dis/cw2+h_dis/ch2)
Focal-EIoU
```

#### Add new loss

1. Add new loss to ``general.py``.
2. Change loss of **bbox_iou()** from ``loss.py``.

    ```python
    iou = bbox_iou(pbox.T, selected_tbox, x1y1x2y2=False, CIoU=True)  # iou(prediction, target) 預設使用CIoU 方式計算
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
