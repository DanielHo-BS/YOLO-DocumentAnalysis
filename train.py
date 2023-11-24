from ultralytics import YOLO

def main():
    # Create a new YOLO model from scratch
    model = YOLO('yolov8m.yaml').load('yolov8m.pt')
    # Train the model with 1 GPUs
    model.train(data="pdf_dataset_old.yaml",
                mode="detect",
                epochs=300,
                imgsz=640,
                device='0',
                batch=8,)
    
if __name__ == "__main__":
    main()