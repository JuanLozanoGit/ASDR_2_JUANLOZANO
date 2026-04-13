from gramatica import EJERCICIO_1, EJERCICIO_2, EJERCICIO_3
from solver import Procesador

def resolver(num, g):
    print("\n" + "="*60)
    print(f"            ANÁLISIS EJERCICIO {num}")
    print("="*60)
    
    p = Procesador(f"EJ{num}", g)
    # 1. Mostrar original
    print("Gramática Original:")
    for nt, reglas in g.items():
        print(f"  {nt} -> {' | '.join([' '.join(r) for r in reglas])}")
        
    # 2. Transformar
    p.eliminar_recursividad()
    
    # 3. Calcular conjuntos
    # Llenamos FIRST primero
    for nt in p.g: p.calc_first(nt)
    p.calc_follow()
    
    # 4. Mostrar resultados
    print("\nConjuntos FIRST:")
    for nt, s in p.first.items(): print(f"  FIRST({nt}) = {s}")
    
    print("\nConjuntos FOLLOW:")
    for nt, s in p.follow.items(): print(f"  FOLLOW({nt}) = {s}")
    
    p.generar_predict()
    p.esquema_asdr()

if __name__ == "__main__":
    resolver(1, EJERCICIO_1)
    resolver(2, EJERCICIO_2)
    resolver(3, EJERCICIO_3)
