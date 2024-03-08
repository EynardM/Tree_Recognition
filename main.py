from util.helpers import *
from util.objects import *

train_dataset, test_dataset, valid_dataset = get_datasets()
train_dataset.data_augmentation()
train_dataset.init(plot=True)