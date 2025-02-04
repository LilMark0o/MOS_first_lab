from pyomo.environ import *

# Conjunto de proyectos y categorías
I = 5  # Número de proyectos
J = 4  # Número de categorías
proyectos = RangeSet(1, I)
categorias = RangeSet(1, J)

# Parámetros
# Costo de cada proyecto en cada categoría
costo = {(i, j): (10 + i * 5 + j * 3) for i in proyectos for j in categorias}
valor = {(i, j): (20 + i * 7 + j * 4)
         for i in proyectos for j in categorias}  # Retorno esperado
presupuesto = 100  # Presupuesto total disponible
max_proyectos = 5  # Número máximo de proyectos que se pueden seleccionar
min_proyectos_categoria = 1  # Mínimo de proyectos a seleccionar en cada categoría
max_costo_proyecto = 30  # Costo máximo permitido por proyecto

# Modelo
Model = ConcreteModel()

# Variables de decisión
# 1 si se selecciona el proyecto en la categoría, 0 si no
Model.x = Var(proyectos, categorias, domain=Binary)


def maximizeFunction(model):
    return sum(model.x[i, j] * valor[i, j] for i in proyectos for j in categorias)


# Función objetivo: Maximizar el retorno total
Model.obj = Objective(rule=maximizeFunction, sense=maximize)

# Restricción de presupuesto
Model.budget_constraint = Constraint(expr=sum(
    Model.x[i, j] * costo[i, j] for i in proyectos for j in categorias) <= presupuesto)

# Restricción de número máximo de proyectos
Model.max_projects_constraint = Constraint(expr=sum(
    Model.x[i, j] for i in proyectos for j in categorias) <= max_proyectos)

# Restricción de mínimo de proyectos por categoría
Model.min_projects_per_category = ConstraintList()
for j in categorias:
    Model.min_projects_per_category.add(
        sum(Model.x[i, j] for i in proyectos) >= min_proyectos_categoria)

# Restricción de costo máximo por proyecto
Model.max_cost_per_project = ConstraintList()
for i in proyectos:
    for j in categorias:
        Model.max_cost_per_project.add(
            Model.x[i, j] * costo[i, j] <= max_costo_proyecto)

# Resolver el modelo
SolverFactory('glpk').solve(Model)

# Mostrar resultados
Model.display()
