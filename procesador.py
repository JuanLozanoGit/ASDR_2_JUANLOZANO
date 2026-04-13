class ProcesadorGramatica:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}
        self.predict = {}

    def revisar_recursividad(self):
        print(f"\n--- [FASE 1] REVISIÓN DE RECURSIVIDAD IZQUIERDA: {self.nombre} ---")
        nueva_g = {}
        cambio = False
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            no_recursivas = [r for r in reglas if r[0] != nt]
            if recursivas:
                cambio = True
                nt_p = nt + "p"
                nueva_g[nt] = [r + [nt_p] for r in no_recursivas]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"  > SE DETECTÓ RECURSIVIDAD EN {nt}. Transformando a {nt} y {nt_p}...")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g
        if not cambio: print("  > No se encontró recursividad izquierda inmediata.")

    def obtener_first(self, simbolo):
        if not simbolo[0].isupper(): return {simbolo}
        if simbolo in self.first and self.first[simbolo]: return self.first[simbolo]
        res = set()
        for r in self.g.get(simbolo, []):
            if r[0] == 'e': res.add('e')
            else:
                for s in r:
                    f = self.obtener_first(s)
                    res.update(f - {'e'})
                    if 'e' not in f: break
                else: res.add('e')
        return res

    def calcular_teoria(self):
        print("\n--- [FASE 2] CÁLCULO DE CONJUNTOS (FIRST & FOLLOW) ---")
        nts = list(self.g.keys())
        # First
        for nt in nts:
            self.first[nt] = self.obtener_first(nt)
            print(f"  FIRST({nt}) = {self.first[nt]}")
        
        # Follow
        self.follow = {nt: set() for nt in nts}
        self.follow[nts[0]].add('$')
        for _ in range(len(nts)):
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in nts:
                            sig = r[i+1:]
                            if not sig: self.follow[simb].update(self.follow[nt])
                            else:
                                f_sig = self.obtener_first(sig[0])
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig: self.follow[simb].update(self.follow[nt])
        for nt in nts: print(f"  FOLLOW({nt}) = {self.follow[nt]}")

    def revisar_predict_y_ll1(self):
        print("\n--- [FASE 3] CONJUNTOS DE PREDICCIÓN Y VALIDACIÓN LL(1) ---")
        es_ll1 = True
        for nt, reglas in self.g.items():
            conjuntos_nt = []
            for r in reglas:
                f_r = self.obtener_first(r[0])
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                print(f"  PREDICT({nt} -> {' '.join(r)}) = {p}")
                for ya_visto in conjuntos_nt:
                    if not p.isdisjoint(ya_visto): es_ll1 = False
                conjuntos_nt.append(p)
        
        print(f"\nRESULTADO FINAL: {'ES LL(1)' if es_ll1 else 'NO ES LL(1) (Requiere refactorización)'}")

    def generar_esqueleto_asdr(self):
        print("\n--- [FASE 4] ESQUEMA DE ANALIZADOR (ASDR) ---")
        for nt in self.g:
            print(f"def proc_{nt}():")
            print(f"    # Lógica de emparejar según PREDICT...")
