from util.imports import *
from util.objects import *
from util.locations import *
from util.helpers import *
from util.parameters import *
import wandb
def train_yolov8(yolo_size, augmented=False):
    # création du data.yaml
    if augmented:
        train_images_path = RUN_AUGMENTED_DATASET+'/images'
        save_dir = MODELS_AUGMENTED
        prefix = "augmented"
    else:
        train_images_path = RUN_TRAIN_DATASET+'/images'
        save_dir = MODELS_TRAIN
        prefix = "train"
    
    valid_images_path = RUN_VALID_DATASET+'/images'
    create_data_yaml(train_images_path, valid_images_path)

    # train
    yolo = YOLO(f'yolov8{yolo_size}.pt')
    run = wandb.init(project="YOLOv8", entity="rally2023", name=f"run_{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}")
    yolo.train(data='data.yaml', epochs=EPOCHS, batch=BATCH_SIZE,
                save_period=10, patience=50, name=f"{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}")
    
    save_name = f"yolov8_{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}.pt"
    model_run = wandb.init(project="YOLOv8_Models", entity="rally2023", job_type="model_logging")
    model_run.log_model(path=os.path.join(save_dir, save_name), name=f"yolov8_{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}.pt")
    model_run.finish()
    run.finish()


if __name__ == "__main__":
    train_yolov8('n')
    train_yolov8('n', augmented=True)

    train_yolov8('s')
    train_yolov8('s', augmented=True)

