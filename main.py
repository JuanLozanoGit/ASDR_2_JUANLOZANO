from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from solver import Procesador

if __name__ == "__main__":
    # Lista de ejercicios a procesar
    ejes = [
        ("EJERCICIO 1", EJERCICIO_1),
        ("EJERCICIO 2", EJERCICIO_2),
        ("EJERCICIO 3", EJERCICIO_3)
    ]
    
    for nombre, datos in ejes:
        app = Procesador(nombre, datos)
        app.ejecutar_analisis_completo()
