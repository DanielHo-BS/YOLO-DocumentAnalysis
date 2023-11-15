# Detect by yolov7 with new weights
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_cra1002_slideft_v10/images/val  --device 0 --project runs/detect/0418 --name old_val
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/test  --device 0 --project runs/detect/0418 --name old_test
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/jpg  --device 0 --project runs/detect/0418 --name dev_jpg
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/png  --device 0 --project runs/detect/0418 --name dev_png
# Error Calculate with GT
#python tools/Indicator/indicator_calculator.py --prediction-path ./runs/detect/0418/old_val/labels --source ./runs/detect/0418/old_val --save-path ./runs/error/FIoU_Gaussian
# Drew the result
#python tools/combin_image.py  --path2 ./runs/error/FIoU_Gaussian --save ./runs/out/GT_FCIoU_Gaussian

# 1107_new
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val  --device 0 --project runs/detect/1107 --name val
python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path ./runs/detect/1107/val/labels --source ./runs/detect/1107/val --save-path ./runs/error/1107_new
python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/1107_new --save ./runs/out/1107_new

# other test data
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/noise_form  --device 0 --project runs/detect/1107 --name noise
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/pdf_image/1  --device 0 --project runs/detect/1107 --name pdf_image_1
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/pdf_image/2  --device 0 --project runs/detect/1107 --name pdf_image_2
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/pdf_image/3  --device 0 --project runs/detect/1107 --name pdf_image_3
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/pdf_image/4  --device 0 --project runs/detect/1107 --name pdf_image_4
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/confuse_text/confuse_text_测试1号私募证券投资基金  --device 0 --project runs/detect/1107 --name confuse_text1
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/confuse_text/confuse_text_测试2号私募证券投资基金  --device 0 --project runs/detect/1107 --name confuse_text2
python detect.py --weights 1107_new.pt --save-txt --source ../datasets/test/img/form_text/三峡_layout识别为表格  --device 0 --project runs/detect/1107 --name form_text
