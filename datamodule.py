from util.helpers import *
from util.objects import *
from util.decorators import *

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

    datasets = {
        'train': train_dataset,
        'augmented': augmented_dataset,
        'test': test_dataset,
        'valid': valid_dataset
    }

    for name, dataset in datasets.items():
        if name == 'train':
            new_dataset_folder = RUN_TRAIN_DATASET
        elif name == 'augmented':
            new_dataset_folder = RUN_AUGMENTED_DATASET
        elif name == 'test':
            new_dataset_folder = RUN_TEST_DATASET
        else:
            new_dataset_folder = RUN_VALID_DATASET
        generate_dataset(new_dataset_folder, dataset)
        
if __name__ == "__main__":
    main()
