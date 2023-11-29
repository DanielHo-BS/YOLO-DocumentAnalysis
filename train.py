from ultralytics import YOLO

def main():
    # Create a new YOLO model from scratch
    model = YOLO('./yolov8m.pt')
    # Train the model with 1 GPUs
    model.train(data="pdf_dataset.yaml",
                mode="detect",
                epochs=500,
                imgsz=640,
                device='0',
                batch=16,
                resume=True,)
    
if __name__ == "__main__":
    main()