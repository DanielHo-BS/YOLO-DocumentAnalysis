# old data without DocLayNet:
# Training set: 7006
# Validation set: 2936

# Drew the GT label
#python ./tools/drew_bbox.py --save ./runs/GT/train/
#python ./tools/drew_bbox.py --imageFolder ../datasets/old/hand_craft_v10/images/val/ --labelFolder ../datasets/old/hand_craft_v10/labels/val/ --save ./runs/GT/val/

# Detect by yolov7 with weights(C/E/FC/FE)
#python detect.py --weights 0223_CIoU.pt --save-txt --source ../datasets/pdf_layout_detector/pdf_dataset/total  --device 0 --project runs/detect/0605 --name c
#python detect.py --weights 0404_EIoU.pt --save-txt --source ../datasets/pdf_layout_detector/pdf_dataset/total  --device 0 --project runs/detect/0605 --name e
#python detect.py --weights 0329_FCIoU.pt --save-txt --source ../datasets/pdf_layout_detector/pdf_dataset/total  --device 0 --project runs/detect/0605 --name fc
#python detect.py --weights 0307_FEIoU.pt --save-txt --source ../datasets/pdf_layout_detector/pdf_dataset/total  --device 0 --project runs/detect/0605 --name fe

# Error Calculate with c/e fc/fe -- c/fc e/fe -- c/fe e/fc
#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/c/labels --prediction-path ./runs/detect/0605/e/labels --source ./runs/detect/0605/c --save-path ./runs/error/c_e
#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/fc/labels --prediction-path ./runs/detect/0605/fe/labels --source ./runs/detect/0605/fc --save-path ./runs/error/fc_fe

#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/c/labels --prediction-path ./runs/detect/0605/fc/labels --source ./runs/detect/0605/c --save-path ./runs/error/c_fc
#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/e/labels --prediction-path ./runs/detect/0605/fe/labels --source ./runs/detect/0605/e --save-path ./runs/error/e_fe

#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/c/labels --prediction-path ./runs/detect/0605/fe/labels --source ./runs/detect/0605/c --save-path ./runs/error/c_fe
#python tools/Indicator/indicator_calculator.py --ground-truth-path  ./runs/detect/0605/e/labels --prediction-path ./runs/detect/0605/fc/labels --source ./runs/detect/0605/fc --save-path ./runs/error/e_fc

# Drew the result
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/FCIoURot_GTV --save ./runs/out/FCIoURot_GTV
#python tools/combin_image.py  --path1 ./runs/GT/train --path2 ./runs/error/FCIoURot_GTT --save ./runs/out/FCIoURot_GTT

# score-thres: 0.4 & sigma: 0.1 iou-thres: 0.1
#python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --score-thres 0.4 --sigma 0.1 --iou-thres 0.1 --device cpu --project runs/soft_nms --name 04_01_01
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/soft_nms/04_01_01/labels --source runs/soft_nms/04_01_01/ --save-path ./runs/error/04_01_01
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/04_01_01 --save ./runs/out/04_01_01

# score-thres: 0.4 & sigma: 0.3 iou-thres: 0.1
#python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --score-thres 0.4 --sigma 0.3 --iou-thres 0.1 --device cpu --project runs/soft_nms --name 04_03_01
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/soft_nms/04_03_01/labels --source runs/soft_nms/04_03_01/ --save-path ./runs/error/04_03_01
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/04_03_01 --save ./runs/out/04_03_01

python detect.py --weights 0918_siou.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --device 0 --project runs/detect/0918 --name offset
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/detect/0918/offset/labels --source runs/detect/0918/offset/ --save-path ./runs/error/offset
python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/offset --save ./runs/out/offset
