from util.imports import *
from util.objects import *
from util.locations import *
from util.helpers import *
from util.parameters import *
import wandb
os.environ["WANDB_MODE"] = "dryrun"
def train_yolov8(yolo_size, augmented=False):
    # création du data.yaml
    if augmented:
        train_images_path = RUN_AUGMENTED_DATASET+'/images'
        save_dir = MODELS_AUGMENTED
        prefix = "augmented"
    else :
        train_images_path = RUN_TRAIN_DATASET+'/images'
        save_dir = MODELS_TRAIN
        prefix = "train"
    valid_images_path = RUN_VALID_DATASET+'/images'
    create_data_yaml(train_images_path, valid_images_path)

    # train
    yolo = YOLO(f'yolov8{yolo_size}.pt') 
    run = wandb.init(project="YOLOv8", entity="rally2023", name=f"run_{prefix}_{EPOCHS}_{BATCH_SIZE}_{LR}")
    yolo.train(data='./data.yaml', epochs=EPOCHS, batch=BATCH_SIZE, lr0=LR,
                save_period=10, patience=50)
    save_name = f"yolov8_{yolo_size}_{EPOCHS}_{BATCH_SIZE}_{LR}.pt"
    yolo.save(os.path.join(save_dir, save_name))
    run.log_model(path=os.path.join(save_dir, save_name), name=f"yolov8_{yolo_size}_{EPOCHS}_{BATCH_SIZE}_{LR}.pt")


if __name__ == "__main__":
    train_yolov8('n')
    train_yolov8('n', augmented=True)