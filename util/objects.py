from util.imports import *
from util.locations import *
from util.variables import * 
from util.draw import *

class Data:
    def __init__(self, image_path, label_path, id):
        self.id = id
        self.image_path = image_path
        self.label_path = label_path
        self.annotations = None

        self.trees = None
        self.proportions = None

    def __str__(self):
        return f"Id: {self.id}, Annotations: {self.annotations}"
    
    def get_annotations(self) -> None:
        with open(self.label_path, 'r') as file:
            lines = file.readlines()
            annotations = [line.strip().split() for line in lines]
            self.annotations = []
            for annotation in annotations:
                self.annotations.append([int(annotation[0]), float(annotation[1]), float(annotation[2]), float(annotation[3]), float(annotation[4])])
    
    def get_stats(self) -> None:
        nb_trees = {label: 0 for label in INT_TO_LABELS.values()}
        if len(self.annotations) != 0:
            trees_sum = len(self.annotations)
            for annotation in self.annotations:
                tree_type = int(annotation[0])
                label = INT_TO_LABELS[tree_type]
                nb_trees[label] += 1
            proportions = {label: count / trees_sum for label, count in nb_trees.items()}
            self.trees = nb_trees
            self.proportions = proportions
        else:
            for key in list(LABELS_TO_INT.keys()):
                LABELS_TO_INT[key] = 0
            self.trees = LABELS_TO_INT
            self.proportions = LABELS_TO_INT
    
    def init(self) -> None:
        self.get_annotations()
        self.get_stats()

    def plot_proportions(self) -> None:
        labels = list(self.proportions.keys())
        proportions = list(self.proportions.values())

        plt.figure(figsize=(10, 6))
        plt.bar(labels, proportions)
        plt.xlabel('Type d\'arbre')
        plt.ylabel('Proportion')
        plt.title('Proportions des différents types d\'arbres')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
class Dataset:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.name = os.path.basename(data_folder)
        self.dataset_stats = {'nb_trees': {}, 'proportions': {}}

        self.elements = []
        self.augmented_elements = []

    def __str__(self):
        stats_str = "\nStatistics:\n"
        for key, value in self.dataset_stats.items():
            stats_str += f"{key}: {value}\n"
        return f"Name: {self.name}\n{stats_str}"

    def populate(self) -> None:
        for file in os.listdir(os.path.join(self.data_folder, 'images')):
            if file.endswith('.JPG'):
                file_id = os.path.splitext(file)[0]
                image_path = os.path.join(self.data_folder, 'images', file)
                label_file = file_id + '.txt'
                label_path = os.path.join(self.data_folder, 'labels', label_file)
                if os.path.isfile(label_path):
                    element = Data(image_path, label_path, file_id)
                    self.elements.append(element)

    def get_stats(self) -> None:
        nb_trees_total = {label: 0 for label in INT_TO_LABELS.values()}
        total_trees = 0
        for element in self.elements + self.augmented_elements:
            element.get_annotations()
            element.get_stats()
            total_trees += sum(element.trees.values())
            for label, count in element.trees.items():
                nb_trees_total[label] += count

        proportions_total = {label: count / total_trees for label, count in nb_trees_total.items()}

        self.dataset_stats['nb_trees'] = nb_trees_total
        self.dataset_stats['proportions'] = proportions_total
        
    # def init(self, plot=False) -> None:
    #     self.get_stats()
    #     if plot:
    #         self.plot_proportions()

    def plot_proportions(self):
        labels = list(self.dataset_stats['proportions'].keys())
        proportions = list(self.dataset_stats['proportions'].values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, proportions)
        plt.xlabel('Type d\'arbre')
        plt.ylabel('Proportion')
        plt.title(f'{self.name} Dataset - Proportions des différents types d\'arbres')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def data_augmentation(self, k=2):
        # Sélection des images à augmenter
        selected_elements = []
        for element in self.elements:
            if (element.proportions['Larch-H'] >= element.proportions['Larch-LD'] * k) or \
                (element.proportions['Larch-HD'] >= element.proportions['Larch-LD'] * k):
                selected_elements.append(element)

        for element in selected_elements:
            image = cv2.imread(element.image_path)
            filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

            # Appliquer les rotations et autres filtres
            for angle in range(3):
                rotated_image = cv2.rotate(image, angle)
                filtered_rotated_image = cv2.GaussianBlur(rotated_image, (5, 5), 0)

                # Rotation des annotations (boîtes englobantes)
                rotated_annotations = []
                for annotation in element.annotations:
                    tree_type, x, y, box_width, box_height = annotation

                    if angle == 2:
                        rotated_x = y  # Swap x and y
                        rotated_y = 1 - x  # Adjust y
                        rotated_box_width = box_height
                        rotated_box_height = box_width

                    elif angle == 1:
                        rotated_x = 1 - x  # Swap x and y
                        rotated_y = 1 - y   # Adjust y
                        rotated_box_width = box_width
                        rotated_box_height = box_height

                    elif angle ==  0:
                        rotated_x = 1 - y  # Swap x and y
                        rotated_y = x  # Adjust y
                        rotated_box_width = box_height
                        rotated_box_height = box_width

                    # Ajouter les nouvelles coordonnées de la boîte englobante à la liste des annotations
                    rotated_annotations.append([tree_type, rotated_x, rotated_y, rotated_box_width, rotated_box_height])

                # Image basique rotated
                filename = f"{element.id}_{angle}"
                augmented_image_path = os.path.join(TRAIN_DATASET_IMAGES_PATH, filename+".jpg")
                cv2.imwrite(augmented_image_path, rotated_image)

                augmented_label_path = os.path.join(TRAIN_DATASET_LABELS_PATH, filename+".txt")
                with open(augmented_label_path, 'w') as f:
                    for annotation in rotated_annotations:
                        f.write(' '.join(map(str, annotation)) + '\n')

                augmented_element = Data(augmented_image_path, augmented_label_path, filename)
                self.augmented_elements.append(augmented_element)

                # Image basique rotated filtered
                filtered_image_path = os.path.join(TRAIN_DATASET_IMAGES_PATH, filename+"_f"+".jpg")
                cv2.imwrite(filtered_image_path, filtered_rotated_image)

                filtered_label_path = os.path.join(TRAIN_DATASET_LABELS_PATH, filename+"_f"+".txt")
                with open(filtered_label_path, 'w') as f:
                    for annotation in rotated_annotations:
                        f.write(' '.join(map(str, annotation)) + '\n')

                augmented_element = Data(filtered_image_path, filtered_label_path, filename+"_f")
                self.augmented_elements.append(augmented_element)

            # Image basique filtered
            filtered_label_path = os.path.join(TRAIN_DATASET_LABELS_PATH, filename+"_f"+".txt")
            with open(filtered_label_path, 'w') as f:
                for annotation in element.annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            # Image basique mirrored
            mirrored_image = cv2.flip(image, 1)
            mirrored_annotations = [[ann[0], 1 - ann[1], ann[2], ann[3], ann[4]] for ann in element.annotations]
            mirrored_image_path = os.path.join(TRAIN_DATASET_IMAGES_PATH, filename+"_m"+".jpg")
            mirrored_label_path = os.path.join(TRAIN_DATASET_LABELS_PATH, filename+"_m"+".txt")          
            cv2.imwrite(mirrored_image_path, mirrored_image)

            with open(mirrored_label_path, 'w') as f:
                for annotation in mirrored_annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            augmented_element = Data(mirrored_image_path, mirrored_label_path, filename+"_m")
            self.augmented_elements.append(augmented_element)
            
            # Image basique mirrored filtered
            mirrored_filtered_image = cv2.flip(filtered_image, 1)  
            mirrored_filtered_path = os.path.join(TRAIN_DATASET_IMAGES_PATH, filename+"_f_m"+".jpg")
            mirrored_filtered_label_path = os.path.join(TRAIN_DATASET_LABELS_PATH, filename+"_f_m"+".txt")
            cv2.imwrite(mirrored_filtered_path, mirrored_filtered_image)
            
            with open(mirrored_filtered_label_path, 'w') as f:
                for annotation in mirrored_annotations:
                    f.write(' '.join(map(str, annotation)) + '\n')

            augmented_element = Data(mirrored_image_path, mirrored_filtered_label_path, filename+"_f_m")
            self.augmented_elements.append(augmented_element)