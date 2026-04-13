from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from solver import Procesador

def correr_ejercicio(n, g):
    print("\n" + "="*60)
    print(f" ANALIZANDO EJERCICIO {n}")
    print("="*60)
    sol = Procesador(f"EJ{n}", g)
    sol.revisar_recursividad()
    sol.calcular_follow()
    sol.generar_predict()
    sol.esquema_asdr()

if __name__ == "__main__":
    ejes = [EJERCICIO_1, EJERCICIO_2, EJERCICIO_3]
    for i, g in enumerate(ejes, 1):
        correr_ejercicio(i, g)
