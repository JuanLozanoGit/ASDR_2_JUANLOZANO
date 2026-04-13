class ProcesadorGramatica:
    def __init__(self, gramatica):
        self.g = gramatica
        self.first = {}
        self.follow = {}
        self.predict = {}

    def eliminar_recursividad(self):
        nueva_g = {}
        print("\n--- Eliminando Recursividad Izquierda ---")
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            no_recursivas = [r for r in reglas if r[0] != nt]
            
            if recursivas:
                nuevo_nt = nt + "p"
                # Reglas originales modificadas
                nueva_g[nt] = [r + [nuevo_nt] for r in no_recursivas]
                # Nuevas reglas para el terminal prima
                nueva_g[nuevo_nt] = [r[1:] + [nuevo_nt] for r in recursivas] + [['e']]
                print(f"NT {nt} transformado en {nt} y {nuevo_nt}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g
        return nueva_g

    def get_first(self, simbolo):
        if not (simbolo.isupper() or (len(simbolo)>1 and simbolo[0].isupper())): # Terminal
            return {simbolo}
        if simbolo in self.first and self.first[simbolo]:
            return self.first[simbolo]
        
        res = set()
        for regla in self.g.get(simbolo, []):
            if regla[0] == 'e':
                res.add('e')
            else:
                for s in regla:
                    f = self.get_first(s)
                    res.update(f - {'e'})
                    if 'e' not in f: break
                else: res.add('e')
        return res

    def calcular_tablas(self):
        nts = list(self.g.keys())
        # FIRST
        for nt in nts: self.first[nt] = self.get_first(nt)
        
        # FOLLOW
        self.follow = {nt: set() for nt in nts}
        self.follow[nts[0]].add('$')
        for _ in range(len(nts)): # Iteracion para estabilizar
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in nts:
                            sig = r[i+1:]
                            if not sig:
                                self.follow[simb].update(self.follow[nt])
                            else:
                                f_sig = self.get_first(sig[0])
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig:
                                    self.follow[simb].update(self.follow[nt])
        
        # PREDICT
        print("\n--- Conjuntos de Prediccion ---")
        es_ll1 = True
        for nt, reglas in self.g.items():
            preds_nt = []
            for i, r in enumerate(reglas):
                f_r = self.get_first(r[0])
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                self.predict[(nt, i)] = p
                print(f"PREDICT({nt} -> {' '.join(r)}) = {p}")
                
                # Check LL1
                for anterior in preds_nt:
                    if not p.isdisjoint(anterior): es_ll1 = False
                preds_nt.append(p)
        
        print(f"\n¿Es la gramatica LL(1)?: {'SI' if es_ll1 else 'NO'}")

    def mostrar(self):
        for nt, reglas in self.g.items():
            print(f"{nt} -> {' | '.join([' '.join(r) for r in reglas])}")
