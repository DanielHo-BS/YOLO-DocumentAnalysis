# Detect by yolov7 with new weights
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val  --device 0 --project runs/detect/0418 --name old_val
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/old/hand_craft_v10/images/test  --device 0 --project runs/detect/0418 --name old_test
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/jpg  --device 0 --project runs/detect/0418 --name dev_jpg
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/dev/png  --device 0 --project runs/detect/0418 --name dev_png
# Error Calculate with GT
#python tools/Indicator/indicator_calculator.py --prediction-path ./runs/detect/0418/old_val/labels --source ./runs/detect/0418/old_val --save-path ./runs/error/FIoU_Gaussian
# Drew the result
#python tools/combin_image.py  --path2 ./runs/error/FIoU_Gaussian --save ./runs/out/GT_FCIoU_Gaussian


python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_21年审计报告  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_2017-2019年审计报告  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_2020年度审计报告  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_2022年1-9月审计报告  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_摘要  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_法律意见书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/2023年利辛县城乡发展建设投资集团有限公司_说明书  --device 0


python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/insurance_保险1  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/insurance_保险2  --device 0

python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/上证山东长信化学科技股份有限公司_上市保荐书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/上证山东长信化学科技股份有限公司_上证山东长信化学科技股份有限公司审计报告 --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/上证山东长信化学科技股份有限公司_发行保荐书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/上证山东长信化学科技股份有限公司_山东长信化学科技股份有限公司招股说明书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/上证山东长信化学科技股份有限公司_法律意见书 --device 0


python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/招股1_保荐书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/招股1_审计报告 --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/招股1_意见书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/招股1_说明书  --device 0

python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/江苏新海连发展有限公司_2006－2008三年连审审计报告  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/江苏新海连发展有限公司_审计报告书 --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/江苏新海连发展有限公司_摘要  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/江苏新海连发展有限公司_法律意见书  --device 0
python detect.py --weights 0516_FCIoU_degrees.pt --save-txt --source /mnt/d/datasets/pdf_layout_detector/pdf_dataset/img/DetectionTest/江苏新海连发展有限公司_说明书  --device 0