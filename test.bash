# Drew the result
# CIoU and Focal-CIoU
python tools/combin_image.py  --path1 ./runs/detect/0223/dev_jpg --path2 ./runs/detect/0329/dev_jpg --save ./runs/out/C_FC_jpg
python tools/combin_image.py  --path1 ./runs/detect/0223/dev_png --path2 ./runs/detect/0329/dev_png --save ./runs/out/C_FC_png
# EIoU and Focal-EIoU
python tools/combin_image.py  --path1 ./runs/detect/0404/dev_jpg --path2 ./runs/detect/0307/dev_jpg --save ./runs/out/E_FE_jpg
python tools/combin_image.py  --path1 ./runs/detect/0404/dev_png --path2 ./runs/detect/0307/dev_png --save ./runs/out/E_FE_png 
# Total
python tools/combin_image.py  --path1 ./runs/out/C_FC_jpg --path2 ./runs/out/E_FE_jpg --save ./runs/out/C_FC__E_FE_jpg
python tools/combin_image.py  --path1 ./runs/out/C_FC_png --path2 ./runs/out/E_FE_png --save ./runs/out/C_FC__E_FE_png  