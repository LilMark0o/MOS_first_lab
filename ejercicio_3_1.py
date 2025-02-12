from pyomo.environ import *
from visualizar_matrices import plot_assignment_heatmap3


aviones = {
    1: {"peso": 30, "volumen": 25},
    2: {"peso": 40, "volumen": 30},
    3: {"peso": 50, "volumen": 35}
}


recursos = {
    1: {"valor": 50, "peso": 15, 'volumen': 8},
    2: {"valor": 100, "peso": 5, 'volumen': 2},
    3: {"valor": 120, "peso": 20, 'volumen': 10},
    4: {"valor": 60, "peso": 18, 'volumen': 12},
    5: {"valor": 40, "peso": 10, 'volumen': 6},
}

recursos_disponibles = RangeSet(1, len(recursos))
aviones_disponibles = RangeSet(1, len(aviones))

Model = ConcreteModel()

Model.x = Var(recursos_disponibles, aviones_disponibles, domain=Binary)


def maximizeFunction(model):
    return sum(Model.x[i, j] * recursos[i]['valor'] for i in recursos_disponibles for j in aviones_disponibles)


Model.obj = Objective(rule=maximizeFunction, sense=maximize)

Model.peso_constraint = ConstraintList()

for j in aviones_disponibles:
    Model.peso_constraint.add(
        sum(Model.x[i, j] * recursos[i]['peso'] for i in recursos_disponibles) <= aviones[j]['peso'])

Model.volumen_constraint = ConstraintList()

for j in aviones_disponibles:
    Model.volumen_constraint.add(
        sum(Model.x[i, j] * recursos[i]['volumen'] for i in recursos_disponibles) <= aviones[j]['volumen'])

Model.dont_repeat_task = ConstraintList()

for i in recursos_disponibles:
    Model.dont_repeat_task.add(
        sum(Model.x[i, j] for j in aviones_disponibles) <= 1)

Model.restriction_one = Constraint(
    expr=Model.x[1, 1] == 0)

Model.restriction_two = Constraint(
    expr=Model.x[3, 1] + Model.x[4, 1] <= 1)

SolverFactory('glpk').solve(Model)


total_valor = sum(Model.x[i, j].value * recursos[i]['valor']
                  for i in recursos_disponibles for j in aviones_disponibles)

print(f"El valor total es: {total_valor}")
for i in recursos_disponibles:
    for j in aviones_disponibles:
        print(f"x[{i},{j}] = {Model.x[i, j].value}")
plot_assignment_heatmap3(Model, list(recursos_disponibles), list(
    aviones_disponibles), 'ejercicio_3_1.png')
