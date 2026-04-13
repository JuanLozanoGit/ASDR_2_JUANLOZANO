from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from procesador import ProcesadorGramatica

def ejecutar_revision_completa(num, gramatica):
    print("\n" + "#"*70)
    print(f"      INICIANDO REVISIÓN COMPLETA DEL EJERCICIO {num}")
    print("#"*70)
    
    p = ProcesadorGramatica(f"EJ{num}", gramatica)
    p.revisar_recursividad()
    p.calcular_teoria()
    p.revisar_predict_y_ll1()
    p.generar_esqueleto_asdr()

if __name__ == "__main__":
    ejercicios = [EJERCICIO_1, EJERCICIO_2, EJERCICIO_3]
    for i, g in enumerate(ejercicios, 1):
        ejecutar_revision_completa(i, g)
