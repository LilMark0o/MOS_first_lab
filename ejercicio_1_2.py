from pyomo.environ import *
from visualizar_matrices import plot_assignment_heatmap
tareas = {
    1: {"puntos_historia": 5, "prioridad": "Máxima"},
    2: {"puntos_historia": 3, "prioridad": "Media alta"},
    3: {"puntos_historia": 13, "prioridad": "Alta"},
    4: {"puntos_historia": 1, "prioridad": "Media baja"},
    5: {"puntos_historia": 21, "prioridad": "Mínima"},
    6: {"puntos_historia": 2, "prioridad": "Media"},
    7: {"puntos_historia": 2, "prioridad": "Alta"},
    8: {"puntos_historia": 5, "prioridad": "Alta"},
    9: {"puntos_historia": 8, "prioridad": "Baja"},
    10: {"puntos_historia": 13, "prioridad": "Máxima"},
    11: {"puntos_historia": 21, "prioridad": "Alta"}
}

prioridad_numero = {
    "Mínima": len(tareas)**1,
    "Baja": len(tareas)**2,
    "Media baja": len(tareas)**3,
    "Media": len(tareas)**4,
    "Media alta": len(tareas)**5,
    "Alta": len(tareas)**6,
    "Máxima": len(tareas)**7,
}

for k, v in tareas.items():
    v["prioridad_numero"] = prioridad_numero[v["prioridad"]]

numero_desarrolladores = 4

tareas_a_realizar = RangeSet(1, len(tareas))
desarrolladores_disponibles = RangeSet(1, numero_desarrolladores)
presupuesto_maximo = 13

Model = ConcreteModel()

Model.x = Var(desarrolladores_disponibles, tareas_a_realizar, domain=Binary)


def maximizeFunction(model):
    return sum(model.x[i, j] * tareas[j]["prioridad_numero"] for i in desarrolladores_disponibles for j in tareas_a_realizar)


Model.obj = Objective(rule=maximizeFunction, sense=maximize)

Model.story_points_constraint = ConstraintList()
for i in desarrolladores_disponibles:
    Model.story_points_constraint.add(
        sum(Model.x[i, j] * tareas[j]["puntos_historia"] for j in tareas_a_realizar) <= presupuesto_maximo)

Model.dont_repeat_task = ConstraintList()
for j in tareas_a_realizar:
    Model.dont_repeat_task.add(
        sum(Model.x[i, j] for i in desarrolladores_disponibles) <= 1)

SolverFactory('glpk').solve(Model)
total_task_per_priority = {}
for i in tareas_a_realizar:
    for j in desarrolladores_disponibles:
        if Model.x[j, i]() == 1:
            if tareas[i]["prioridad"] in total_task_per_priority:
                total_task_per_priority[tareas[i]["prioridad"]] += 1
            else:
                total_task_per_priority[tareas[i]["prioridad"]] = 1
title = 'Cantidad de tareas por prioridad: '
texts = []
for k, v in total_task_per_priority.items():
    texts.append(f'{k}: {v}')
title += ', '.join(texts)
plot_assignment_heatmap(Model, list(
    desarrolladores_disponibles), list(tareas_a_realizar), title=title, file='ejercicio_1_2.png')
