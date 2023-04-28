# Drew the result
#python detect.py --weights 0329_FCIoU.pt --save-txt --source ../datasets/watermaker/images/val  --device 0 --project runs/detect/0329 --name watermaker_val
#python detect.py --weights 0418_FCIoU.pt --save-txt --source ../datasets/watermaker/images/val  --device 0 --project runs/detect/0418 --name watermaker_val

# Error Calculate with GT
#python tools/Indicator/indicator_calculator.py --ground-truth-path ./runs/detect/0329/watermaker_val/labels --prediction-path ./runs/detect/0418/watermaker_val/labels --source ./runs/detect/0418/watermaker_val --save-path ./runs/error/F_FCIoU_Gaussian
# Drew the result
#python tools/combin_image.py  --path1 ./runs/detect/0329/watermaker_val --path2 ./runs/error/F_FCIoU_Gaussian --save ./runs/out/F_FCIoU_Gaussian

python test.py --weights 0418_FCIoU.pt --data pdf_dataset_old.yaml --task val --project runs/test/0418_FCIoU --v5-metric --save-txt --name old_val --device 0 --batch-size 8
python test.py --weights 0418_FCIoU.pt --data pdf_dataset.yaml --task val --project runs/test/0418_FCIoU --v5-metric --save-txt --name val --device 0 --batch-size 8