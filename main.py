from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from solver import Procesador

if __name__ == "__main__":
    ejes = [("EJERCICIO 1", EJERCICIO_1), 
            ("EJERCICIO 2", EJERCICIO_2), 
            ("EJERCICIO 3", EJERCICIO_3)]
    
    for nombre, datos in ejes:
        p = Procesador(nombre, datos)
        p.mostrar_paso_a_paso()
