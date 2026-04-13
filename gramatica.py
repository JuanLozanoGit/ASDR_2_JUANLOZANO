# Definicion de gramaticas para los ejercicios de clase
# 'e' lo usamos para representar epsilon (vacio)

EJERCICIO_1 = {
    'S': [['A', 'uno', 'B', 'C'], ['S', 'dos']],
    'A': [['B', 'C', 'D'], ['A', 'tres'], ['e']],
    'B': [['D', 'cuatro', 'C', 'tres'], ['e']],
    'C': [['cinco', 'D', 'B'], ['e']],
    'D': [['seis'], ['e']]
}

EJERCICIO_2 = {
    'S': [['A', 'B', 'uno']],
    'A': [['dos', 'B'], ['e']],
    'B': [['C', 'D'], ['tres'], ['e']],
    'C': [['cuatro', 'A', 'B'], ['cinco']],
    'D': [['seis'], ['e']]
}

EJERCICIO_3 = {
    'S': [['A', 'B']],
    'A': [['id', 'igual', 'E']],
    'B': [['puntoycoma'], ['e']],
    'E': [['num'], ['id']]
}

def print_grammar(g):
    for nt in g:
        reglas = ' | '.join([' '.join(opcion) for opcion in g[nt]])
        print(f"{nt} -> {reglas}")
