class Analizador:
    def __init__(self, gramatica):
        self.g = gramatica
        self.tokens = []
        self.idx = 0
        self.token_actual = None

    def set_input(self, cadena):
        self.tokens = cadena.split()
        self.idx = 0
        self.avanzar()

    def avanzar(self):
        if self.idx < len(self.tokens):
            self.token_actual = self.tokens[self.idx]
            self.idx += 1
        else:
            self.token_actual = "$" # Fin de cadena

    def match(self, esperado):
        if self.token_actual == esperado:
            print(f"Match exitoso: {esperado}")
            self.avanzar()
        else:
            print(f"Error: se esperaba {esperado} y llego {self.token_actual}")
            return False
        return True

    # Metodo simple para verificar si la gramatica es LL(1) 
    # (Comprueba si hay recursividad izquierda basica)
    def check_recursividad(self):
        for nt, reglas in self.g.items():
            for r in reglas:
                if r[0] == nt:
                    return f"Ojo: El no terminal '{nt}' tiene recursividad izquierda."
        return "Gramatica limpia de recursividad inmediata."
