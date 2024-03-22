import numpy as np
import matplotlib.pyplot as plt

# Modèles
models = ['n_train', 'n_aug', 's_train', 's_aug', 'm_train', 'm_aug', 'l_train', 'l_aug']

# Accuracy pour chaque modèle
accuracies = {
    'n_train': [0.78, 0.58, 0.88, 0.77],
    'n_aug': [0.76, 0.60, 0.91, 0.68],
    's_train': [0.77, 0.54, 0.89, 0.69],
    's_aug': [0.81, 0.57, 0.91, 0.65],
    'm_train': [0.78, 0.57, 0.88, 0.79],
    'm_aug': [0.76, 0.58, 0.90, 0.72],
    'l_train': [0.77, 0.58, 0.90, 0.67],
    'l_aug': [0.79, 0.68, 0.89, 0.73]
}

# Transformation des accuracies en un tableau 2D
accuracies_array = np.array([accuracies[model] for model in models])

# Tracer les courbes pour chaque modèle
for i, model in enumerate(models):
    plt.plot(range(len(accuracies[model])), accuracies[model], marker='o', label=model)

# Mettre en forme le graphique
plt.xlabel('Classe')
plt.ylabel('Accuracy')
plt.title('Performance des modèles en termes d\'accuracy')
plt.xticks(range(len(accuracies_array[0])), labels=range(len(accuracies_array[0])))
plt.legend()
plt.grid(True)

# Afficher le graphique
plt.show()

# Calculer la somme des accuracies pour chaque modèle
sum_accuracies = {model: sum(values) for model, values in accuracies.items()}

# Trier les modèles par somme d'accuracy décroissante
sorted_models_by_sum = sorted(sum_accuracies, key=sum_accuracies.get, reverse=True)

# Afficher le classement des modèles
print("Classement des modèles en fonction de la somme des accuracies :")
for i, model in enumerate(sorted_models_by_sum):
    print(f"{i+1}. {model}: {sum_accuracies[model]}")
