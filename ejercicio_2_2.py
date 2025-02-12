from pyomo.environ import *
from visualizar_matrices import plot_assignment_heatmap
horas = {
    1: 8,
    2: 10,
    3: 6
}

trabajos = {
    1: {"ganancia": 50, "tiempo": 4},
    2: {"ganancia": 60, "tiempo": 5},
    3: {"ganancia": 40, "tiempo": 3},
    4: {"ganancia": 70, "tiempo": 6},
    5: {"ganancia": 30, "tiempo": 2}
}

horas_disponibles = RangeSet(1, len(horas))
tareas_a_realizar = RangeSet(1, len(trabajos))

Model = ConcreteModel()

Model.x = Var(horas_disponibles, tareas_a_realizar, domain=Binary)


def maximizeFunction(model):
    return sum(Model.x[i, j] * trabajos[j]['ganancia'] for i in horas_disponibles for j in tareas_a_realizar)


Model.obj = Objective(rule=maximizeFunction, sense=maximize)

Model.time_constraint = ConstraintList()

for i in horas_disponibles:
    Model.time_constraint.add(
        sum(Model.x[i, j] * trabajos[j]['tiempo'] for j in tareas_a_realizar) <= horas[i])

Model.dont_repeat_task = ConstraintList()

for j in tareas_a_realizar:
    Model.dont_repeat_task.add(
        sum(Model.x[i, j] for i in horas_disponibles) <= 1)

Model.restriction_one = Constraint(
    expr=sum(Model.x[i, 1] for i in horas_disponibles if i != 1) == 0)

Model.restriction_two = Constraint(
    expr=Model.x[2, 3] == 0)

SolverFactory('glpk').solve(Model)

total_ganancia = sum(Model.x[i, j].value * trabajos[j]['ganancia']
                     for i in horas_disponibles for j in tareas_a_realizar)

print(f"La ganancia total es: {total_ganancia}")

plot_assignment_heatmap(Model, list(
    horas_disponibles), list(tareas_a_realizar), 'ejercicio_2_2.png', f"La ganancia total es: {total_ganancia}")
