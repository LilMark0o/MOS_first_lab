from pyomo.environ import *
from visualizar_matrices import plot_assignment_heatmap2


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

tareas_a_realizar = RangeSet(1, len(tareas))
presupuesto_maximo = 52

Model = ConcreteModel()

Model.x = Var(tareas_a_realizar, domain=Binary)


def maximizeFunction(model):
    return sum(model.x[i] * tareas[i]["prioridad_numero"] for i in tareas_a_realizar)


Model.obj = Objective(rule=maximizeFunction, sense=maximize)

Model.story_points_constraint = Constraint(expr=sum(
    Model.x[i] * tareas[i]["puntos_historia"] for i in tareas_a_realizar) <= presupuesto_maximo)

SolverFactory('glpk').solve(Model)

total_task_per_priority = {}
for i in tareas_a_realizar:
    if Model.x[i]() == 1:
        total_task_per_priority[tareas[i]["prioridad"]] = total_task_per_priority.get(
            tareas[i]["prioridad"], 0) + 1
title = 'Cantidad de tareas por prioridad: '
texts = []
for k, v in total_task_per_priority.items():
    texts.append(f'{k}: {v}')
title += ', '.join(texts)


plot_assignment_heatmap2(
    Model, tareas, title=title, filename='ejercicio_1_1.png')
