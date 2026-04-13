from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3, print_grammar
from solver import Analizador

def test_ejercicio(num, g):
    print(f"\n--- TRABAJANDO EJERCICIO {num} ---")
    print_grammar(g)
    
    sol = Analizador(g)
    print(sol.check_recursividad())
    
    # Ejemplo de prueba rapida para el Ejercicio 3
    if num == 3:
        print("\nPrueba de cadena para Ejercicio 3:")
        sol.set_input("id igual num puntoycoma")
        # Simula el inicio de la recursion
        sol.match("id")
        sol.match("igual")
        sol.match("num")
        sol.match("puntoycoma")

if __name__ == "__main__":
    ejercicios = [EJERCICIO_1, EJERCICIO_2, EJERCICIO_3]
    
    for i, datos in enumerate(ejercicios, 1):
        test_ejercicio(i, datos)
