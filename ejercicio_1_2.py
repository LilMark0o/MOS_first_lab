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
    "Mínima": 1 * len(tareas),
    "Baja": 2 * len(tareas),
    "Media baja": 3 * len(tareas),
    "Media": 4 * len(tareas),
    "Media alta": 5 * len(tareas),
    "Alta": 6 * len(tareas),
    "Máxima": 7 * len(tareas)
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
total_ganancia = 0
for i in desarrolladores_disponibles:
    for j in tareas_a_realizar:
        if Model.x[i, j]() == 1:
            total_ganancia += tareas[j]["prioridad_numero"]

plot_assignment_heatmap(Model, list(
    desarrolladores_disponibles), list(tareas_a_realizar), title=f'La ganancia total es de {total_ganancia} puntos de historia', file='ejercicio_1_2.png')
