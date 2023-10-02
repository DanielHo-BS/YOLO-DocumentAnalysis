# Detect by yolov7 with new weights
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_cra1002_slideft_v10/images/val  --device 0 --project runs/detect/0418 --name old_val
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/test  --device 0 --project runs/detect/0418 --name old_test
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/jpg  --device 0 --project runs/detect/0418 --name dev_jpg
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/png  --device 0 --project runs/detect/0418 --name dev_png
# Error Calculate with GT
#python tools/Indicator/indicator_calculator.py --prediction-path ./runs/detect/0418/old_val/labels --source ./runs/detect/0418/old_val --save-path ./runs/error/FIoU_Gaussian
# Drew the result
#python tools/combin_image.py  --path2 ./runs/error/FIoU_Gaussian --save ./runs/out/GT_FCIoU_Gaussian



# CIoU with ca
python detect.py --weights 1002_CA.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val  --device 0 --project runs/detect/1002 --name ca
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path ./runs/detect/1002/ca/labels --source ./runs/detect/1002/ca --save-path ./runs/error/1002_ca
python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/1002_ca --save ./runs/out/1002_slide
