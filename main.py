from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from solver import ProcesadorGramatica

def ejecutar_laboratorio(num, datos):
    print("\n" + "="*80)
    print(f"   REVISIÓN TÉCNICA PASO A PASO: EJERCICIO {num}")
    print("="*80)
    
    p = ProcesadorGramatica(f"EJ{num}", datos)
    p.eliminar_recursividad()
    p.calcular_conjuntos()
    p.analizar_predict_y_ll1()
    p.imprimir_asdr()

if __name__ == "__main__":
    ejercicios = [EJERCICIO_1, EJERCICIO_2, EJERCICIO_3]
    for i, g in enumerate(ejercicios, 1):
        ejecutar_laboratorio(i, g)
