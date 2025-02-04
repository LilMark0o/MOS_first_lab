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

total_ganancia = 0
for i in tareas_a_realizar:
    if Model.x[i]() == 1:
        total_ganancia += tareas[i]["prioridad_numero"]

text = f'La ganancia total es de {total_ganancia} puntos de historia'

plot_assignment_heatmap2(
    Model, tareas, title=f'La ganancia total es de {total_ganancia} puntos de historia', filename='ejercicio_1_1.png')
