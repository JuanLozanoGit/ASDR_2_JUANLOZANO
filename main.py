from gramatica import EJERCICIO_1, EJERCICIO_2
from procesador import ProcesadorGramatica

def ejecutar_analisis(id_ej, gram):
    print(f"\n{'#'*30}")
    print(f"   EJERCICIO {id_ej}")
    print(f"{'#'*30}")
    
    proc = ProcesadorGramatica(gram)
    print("Gramatica Original:")
    proc.mostrar()
    
    # Transformacion
    proc.eliminar_recursividad()
    print("\nGramatica Transformada:")
    proc.mostrar()
    
    # Calculos
    proc.calcular_tablas()
    
    print("\n--- Analizador Sintactico (ASDR) ---")
    print("Simulando proceso de emparejar (match) para cadena de prueba...")
    # Aqui iria la logica de consumo de tokens basado en PREDICT

if __name__ == "__main__":
    ejecutar_analisis(1, EJERCICIO_1)
    ejecutar_analisis(2, EJERCICIO_2)
