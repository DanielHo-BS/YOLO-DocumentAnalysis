# DIoU Fine-Turn: score-thres, iou-thres and sigma
# iou-thres: 0.1~0.6
# score-thres: 0.3~0.8
# sigma: 0.1

#### iou-thres: 0.1####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.3 --device 0 --project runs/diou_ft --name 01_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_03/labels --source runs/diou_ft/01_03/ --save-path ./runs/error/diou_ft/01_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_03 --save ./runs/out/diou_ft/01_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.4 --device 0 --project runs/diou_ft --name 01_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_04/labels --source runs/diou_ft/01_04/ --save-path ./runs/error/diou_ft/01_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_04 --save ./runs/out/diou_ft/01_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.5 --device 0 --project runs/diou_ft --name 01_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_05/labels --source runs/diou_ft/01_05/ --save-path ./runs/error/diou_ft/01_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_05 --save ./runs/out/diou_ft/01_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.6 --device 0 --project runs/diou_ft --name 01_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_06/labels --source runs/diou_ft/01_06/ --save-path ./runs/error/diou_ft/01_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_06 --save ./runs/out/diou_ft/01_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.7 --device 0 --project runs/diou_ft --name 01_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_07/labels --source runs/diou_ft/01_07/ --save-path ./runs/error/diou_ft/01_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_07 --save ./runs/out/diou_ft/01_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.1 --score-thres 0.8 --device 0 --project runs/diou_ft --name 01_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/01_08/labels --source runs/diou_ft/01_08/ --save-path ./runs/error/diou_ft/01_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/01_08 --save ./runs/out/diou_ft/01_08

#### iou-thres: 0.2####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.3 --device 0 --project runs/diou_ft --name 02_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_03/labels --source runs/diou_ft/02_03/ --save-path ./runs/error/diou_ft/02_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_03 --save ./runs/out/diou_ft/02_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.4 --device 0 --project runs/diou_ft --name 02_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_04/labels --source runs/diou_ft/02_04/ --save-path ./runs/error/diou_ft/02_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_04 --save ./runs/out/diou_ft/02_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.5 --device 0 --project runs/diou_ft --name 02_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_05/labels --source runs/diou_ft/02_05/ --save-path ./runs/error/diou_ft/02_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_05 --save ./runs/out/diou_ft/02_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.6 --device 0 --project runs/diou_ft --name 02_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_06/labels --source runs/diou_ft/02_06/ --save-path ./runs/error/diou_ft/02_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_06 --save ./runs/out/diou_ft/02_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.7 --device 0 --project runs/diou_ft --name 02_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_07/labels --source runs/diou_ft/02_07/ --save-path ./runs/error/diou_ft/02_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_07 --save ./runs/out/diou_ft/02_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.2 --score-thres 0.8 --device 0 --project runs/diou_ft --name 02_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/02_08/labels --source runs/diou_ft/02_08/ --save-path ./runs/error/diou_ft/02_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/02_08 --save ./runs/out/diou_ft/02_08

#### iou-thres: 0.3####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.3 --device 0 --project runs/diou_ft --name 03_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_03/labels --source runs/diou_ft/03_03/ --save-path ./runs/error/diou_ft/03_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_03 --save ./runs/out/diou_ft/03_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.4 --device 0 --project runs/diou_ft --name 03_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_04/labels --source runs/diou_ft/03_04/ --save-path ./runs/error/diou_ft/03_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_04 --save ./runs/out/diou_ft/03_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.5 --device 0 --project runs/diou_ft --name 03_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_05/labels --source runs/diou_ft/03_05/ --save-path ./runs/error/diou_ft/03_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_05 --save ./runs/out/diou_ft/03_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.6 --device 0 --project runs/diou_ft --name 03_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_06/labels --source runs/diou_ft/03_06/ --save-path ./runs/error/diou_ft/03_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_06 --save ./runs/out/diou_ft/03_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.7 --device 0 --project runs/diou_ft --name 03_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_07/labels --source runs/diou_ft/03_07/ --save-path ./runs/error/diou_ft/03_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_07 --save ./runs/out/diou_ft/03_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.3 --score-thres 0.8 --device 0 --project runs/diou_ft --name 03_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/03_08/labels --source runs/diou_ft/03_08/ --save-path ./runs/error/diou_ft/03_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/03_08 --save ./runs/out/diou_ft/03_08

#### iou-thres: 0.4####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.3 --device 0 --project runs/diou_ft --name 04_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_03/labels --source runs/diou_ft/04_03/ --save-path ./runs/error/diou_ft/04_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_03 --save ./runs/out/diou_ft/04_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.4 --device 0 --project runs/diou_ft --name 04_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_04/labels --source runs/diou_ft/04_04/ --save-path ./runs/error/diou_ft/04_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_04 --save ./runs/out/diou_ft/04_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.5 --device 0 --project runs/diou_ft --name 04_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_05/labels --source runs/diou_ft/04_05/ --save-path ./runs/error/diou_ft/04_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_05 --save ./runs/out/diou_ft/04_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.6 --device 0 --project runs/diou_ft --name 04_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_06/labels --source runs/diou_ft/04_06/ --save-path ./runs/error/diou_ft/04_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_06 --save ./runs/out/diou_ft/04_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.7 --device 0 --project runs/diou_ft --name 04_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_07/labels --source runs/diou_ft/04_07/ --save-path ./runs/error/diou_ft/04_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_07 --save ./runs/out/diou_ft/04_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.4 --score-thres 0.8 --device 0 --project runs/diou_ft --name 04_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/04_08/labels --source runs/diou_ft/04_08/ --save-path ./runs/error/diou_ft/04_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/04_08 --save ./runs/out/diou_ft/04_08


#### iou-thres: 0.5####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.3 --device 0 --project runs/diou_ft --name 05_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_03/labels --source runs/diou_ft/05_03/ --save-path ./runs/error/diou_ft/05_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_03 --save ./runs/out/diou_ft/05_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.4 --device 0 --project runs/diou_ft --name 05_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_04/labels --source runs/diou_ft/05_04/ --save-path ./runs/error/diou_ft/05_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_04 --save ./runs/out/diou_ft/05_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.5 --device 0 --project runs/diou_ft --name 05_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_05/labels --source runs/diou_ft/05_05/ --save-path ./runs/error/diou_ft/05_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_05 --save ./runs/out/diou_ft/05_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.6 --device 0 --project runs/diou_ft --name 05_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_06/labels --source runs/diou_ft/05_06/ --save-path ./runs/error/diou_ft/05_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_06 --save ./runs/out/diou_ft/05_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.7 --device 0 --project runs/diou_ft --name 05_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_07/labels --source runs/diou_ft/05_07/ --save-path ./runs/error/diou_ft/05_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_07 --save ./runs/out/diou_ft/05_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.5 --score-thres 0.8 --device 0 --project runs/diou_ft --name 05_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/05_08/labels --source runs/diou_ft/05_08/ --save-path ./runs/error/diou_ft/05_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/05_08 --save ./runs/out/diou_ft/05_08

#### iou-thres: 0.6####
# score-thres 0.3
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.3 --device 0 --project runs/diou_ft --name 06_03
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_03/labels --source runs/diou_ft/06_03/ --save-path ./runs/error/diou_ft/06_03
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_03 --save ./runs/out/diou_ft/06_03
# score-thres 0.4
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.4 --device 0 --project runs/diou_ft --name 06_04
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_04/labels --source runs/diou_ft/06_04/ --save-path ./runs/error/diou_ft/06_04
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_04 --save ./runs/out/diou_ft/06_04
# score-thres 0.5
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.5 --device 0 --project runs/diou_ft --name 06_05
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_05/labels --source runs/diou_ft/06_05/ --save-path ./runs/error/diou_ft/06_05
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_05 --save ./runs/out/diou_ft/06_05
# score-thres 0.6
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.6 --device 0 --project runs/diou_ft --name 06_06
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_06/labels --source runs/diou_ft/06_06/ --save-path ./runs/error/diou_ft/06_06
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_06 --save ./runs/out/diou_ft/06_06
# score-thres 0.7
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.7 --device 0 --project runs/diou_ft --name 06_07
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_07/labels --source runs/diou_ft/06_07/ --save-path ./runs/error/diou_ft/06_07
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_07 --save ./runs/out/diou_ft/06_07
# score-thres 0.8
#python detect.py --weights 0627_FC_ND.pt --save-txt --source ../datasets/old/hand_craft_v10/images/val --iou-thres 0.6 --score-thres 0.8 --device 0 --project runs/diou_ft --name 06_08
#python tools/Indicator/indicator_calculator.py --ground-truth-path ../datasets/old/hand_craft_v10/labels/val --prediction-path runs/diou_ft/06_08/labels --source runs/diou_ft/06_08/ --save-path ./runs/error/diou_ft/06_08
#python tools/combin_image.py  --path1 ./runs/GT/val --path2 ./runs/error/diou_ft/06_08 --save ./runs/out/diou_ft/06_08