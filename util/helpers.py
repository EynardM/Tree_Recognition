from util.imports import *
from util.locations import *
from util.objects import *

def create_dataset(dataset_path):
    dataset = Dataset(dataset_path)
    dataset.populate()
    dataset.init()
    return dataset

def get_datasets():
    train_dataset = create_dataset(TRAIN_DATASET_PATH)
    test_dataset = create_dataset(TEST_DATASET_PATH)
    valid_dataset = create_dataset(VALID_DATASET_PATH)
    return train_dataset, test_dataset, valid_dataset