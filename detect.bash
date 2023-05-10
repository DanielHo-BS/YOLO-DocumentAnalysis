# Detect by yolov7 with new weights
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val  --device 0 --project runs/detect/0418 --name old_val
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/test  --device 0 --project runs/detect/0418 --name old_test
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/jpg  --device 0 --project runs/detect/0418 --name dev_jpg
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/png  --device 0 --project runs/detect/0418 --name dev_png
# Error Calculate with GT
#python tools/Indicator/indicator_calculator.py --prediction-path ./runs/detect/0418/old_val/labels --source ./runs/detect/0418/old_val --save-path ./runs/error/FIoU_Gaussian
# Drew the result
#python tools/combin_image.py  --path2 ./runs/error/FIoU_Gaussian --save ./runs/out/GT_FCIoU_Gaussian



# CIoU
python detect.py --weights 0223_CIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/train  --device 0 --project runs/detect/0223 --name old_train
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/train --prediction-path ./runs/detect/0223/old_train/labels --source ./runs/detect/0223/old_train --save-path ./runs/error/GT_CIOU_train
python tools/combin_image.py  --path1 ./runs/GT/train --path2 ./runs/error/GT_CIOU_train --save ./runs/out/GT_CIOU_train
# F-CIoU
#python detect.py --weights 0329_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/train  --device 0 --project runs/detect/0329 --name old_train
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/train --prediction-path ./runs/detect/0329/old_train/labels --source ./runs/detect/0329/old_train --save-path ./runs/error/GT_FCIOU_train
python tools/combin_image.py  --path1 ./runs/GT/train --path2 ./runs/error/GT_FCIOU_train --save ./runs/out/GT_FCIOU_train
# EIoU
python detect.py --weights 0404_EIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/train  --device 0 --project runs/detect/0404 --name old_train
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/train --prediction-path ./runs/detect/0404/old_train/labels --source ./runs/detect/0404/old_train --save-path ./runs/error/GT_EIOU_train
python tools/combin_image.py  --path1 ./runs/GT/train --path2 ./runs/error/GT_EIOU_train --save ./runs/out/GT_EIOU_train
# F-EIoU
python detect.py --weights 0307_FEIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/train  --device 0 --project runs/detect/0307 --name old_train
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/train --prediction-path ./runs/detect/0307/old_train/labels --source ./runs/detect/0307/old_train --save-path ./runs/error/GT_FEIOU_train
python tools/combin_image.py  --path1 ./runs/GT/train --path2 ./runs/error/GT_FEIOU_train --save ./runs/out/GT_FEIOU_train