from util.helpers import *
from util.objects import *
from util.decorators import *
from tqdm import trange
from statistics import stdev

def get_augmented_dataset(train_dataset: Dataset):
    train_dataset.get_stats()

    datasets = []
    for i in trange(len(np.arange(6.0, -0.2, -0.2))):
        k = np.arange(6.0, -0.2, -0.2)[i]
        train_dataset_copy = deepcopy(train_dataset)
        train_dataset_copy.data_augmentation(k=k)
        train_dataset_copy.get_stats()
        datasets.append(train_dataset_copy)
    
    min_dispersion = float('inf')
    optimal_i = None
    for i, dataset in enumerate(datasets):
        proportions = dataset.dataset_stats['proportions']
        dispersion = stdev(proportions.values())
        if dispersion < min_dispersion:
            min_dispersion = dispersion
            optimal_i = i

    return datasets[optimal_i]

def main():
    train_dataset, test_dataset, valid_dataset = get_datasets()
    augmented_dataset = get_augmented_dataset(train_dataset=train_dataset)
    dict_datasets = {
        'train': train_dataset,
        'augmented': augmented_dataset,
        'test': test_dataset,
        'valid': valid_dataset
    }
    
    save_datasets(dict_datasets)
    
    loaded_datasets = load_datasets()
    print(loaded_datasets)
if __name__ == "__main__":
    main()
