# Gramaticas originales para el laboratorio
# 'e' representa la cadena vacia (epsilon)

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
    'S': [['A', 'dos'], ['e']],
    'A': [['B', 'uno', 'S']],
    'B': [['tres', 'C'], ['e']],
    'C': [['cuatro'], ['cinco']]
}
