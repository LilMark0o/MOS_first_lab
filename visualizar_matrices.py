from pyomo.environ import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_assignment_heatmap(model, desarrolladores, tareas, file='ejercicio_1_2.png', title="Asignación de tareas a desarrolladores"):
    assignment_matrix = np.zeros((len(desarrolladores), len(tareas)))

    for i in desarrolladores:
        for j in tareas:
            if model.x[i, j].value > 0.8:
                assignment_matrix[i-1, j-1] = 1

    plt.figure(figsize=(10, 6))
    sns.heatmap(assignment_matrix, annot=True, cmap="Blues",
                cbar=False, xticklabels=tareas, yticklabels=desarrolladores)
    if '2_1' in file:
        plt.xlabel("Trabajos a realizar")
        plt.ylabel("Trabajadores")
    else:
        plt.xlabel("Tareas")
        plt.ylabel("Desarrolladores")
    plt.title(title)
    plt.savefig(file)


def plot_assignment_heatmap2(model, tareas, title="Asignación de tareas a desarrolladores", filename='ejercicio_1_1.png'):
    # Extraer las tareas seleccionadas
    selected_tasks = [i for i in tareas if model.x[i].value > 0.5]

    # Crear la matriz de visualización
    task_labels = list(tareas.keys())
    task_values = [1 if i in selected_tasks else 0 for i in task_labels]

    plt.figure(figsize=(10, 2))
    sns.heatmap([task_values], annot=True, cmap="Blues", cbar=False,
                xticklabels=task_labels, yticklabels=["Seleccionadas"])
    plt.xlabel("Tareas")
    plt.title(title)
    plt.savefig(filename)


def plot_assignment_heatmap3(model, aviones, recursos, file='ejercicio_3_1.png', title="Asignación de recursos a aviones"):
    assignment_matrix = np.zeros((len(aviones), len(recursos)))

    for i in aviones:
        for j in recursos:
            if model.x[i, j].value > 0.8:
                assignment_matrix[i-1, j-1] = 1  # Ajuste de índices a base 0

    plt.figure(figsize=(10, 6))
    sns.heatmap(assignment_matrix, annot=True, cmap="Blues",
                cbar=False, xticklabels=recursos, yticklabels=aviones)
    
    plt.xlabel("Aviones")
    plt.ylabel("Recursos")
    plt.title(title)
    plt.savefig(file)
    plt.close()