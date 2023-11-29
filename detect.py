import time
from ultralytics import YOLO

def main():
    # Load a pretrained YOLOv8n model
    model = YOLO("runs/detect/train2/weights/best.pt")

    # Source directory
    dir = "../datasets/old/hand_craft_v10/images/val"

    # Run inference on directory with arguments
    start = time.time()
    results = model(source = dir, stream = True, device= "0", save = True, save_txt = True)

    # Iteration for clear memory
    while True:
      try:  
        next(results)
      except:
        end = time.time()
        print("-----------------------------------")
        print("Total Time: ", end - start, "s")
        break


if __name__ == "__main__":
    main()
