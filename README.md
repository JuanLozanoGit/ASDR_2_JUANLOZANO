# ASDR_2_JUANLOZANO

## Requisitos del Sistema:

1. **Python 3.x** instalado.
2. Una terminal (Linux, macOS o Windows).

## Instalación:

Solo necesitas descargar los archivos y situarte en el directorio del proyecto:

```bash
git clone https://github.com/JuanLozanoGit/ASDR_EJERCICIOS_JUANLOZANO
cd ASDR_EJERCICIOS_JUANLOZANO
```

## Guía de Uso:

1. **Configuración:**
   Las gramáticas de los ejercicios están definidas en `gramatica.py`. Se utiliza `'e'` para representar la cadena vacía ($\epsilon$).

2. **Ejecución:**
   Para procesar los ejercicios y ver el paso a paso, ejecuta:
   ```bash
   python3 main.py
   ```

3. **Interpretación de resultados:**
   El programa genera un reporte por cada ejercicio que incluye:
   * **Gramática Original:** Estado inicial de las reglas.
   * **Revisión de Recursividad:** Proceso de transformación para eliminar recursividad izquierda inmediata.
   * **Conjuntos FIRST y FOLLOW:** Base matemática del análisis.
   * **Veredicto LL(1):** Validación de si la gramática es apta para análisis predictivo.
   * **Esquema ASDR:** Lógica de decisiones para la implementación de las funciones del analizador.

## Estructura de Archivos:

* **`gramatica.py`**: Repositorio de las gramáticas de los 3 ejercicios.
* **`solver.py`**: Contiene el motor de cálculo de conjuntos, el transformador de reglas y la lógica de predicción.
* **`main.py`**: Script principal que ejecuta la revisión técnica de forma secuencial.
