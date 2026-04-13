# Gramaticas originales
# 'e' = epsilon

# Esta tiene recursividad izquierda (S -> S dos)
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
