class Procesador:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}
        self.predict = {}

    def eliminar_recursividad(self):
        print(f"\n>>> {self.nombre}: REVISIÓN DE RECURSIVIDAD")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            no_recursivas = [r for r in reglas if r[0] != nt]
            if recursivas:
                nt_p = nt + "p"
                nueva_g[nt] = [r + [nt_p] for r in no_recursivas]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f" [!] Recursividad eliminada en {nt}. Creado {nt_p}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g

    def calc_first(self, simbolo):
        if not simbolo[0].isupper(): return {simbolo}
        if simbolo in self.first and self.first[simbolo]: return self.first[simbolo]
        res = set()
        for r in self.g.get(simbolo, []):
            if r[0] == 'e': res.add('e')
            else:
                for s in r:
                    f = self.calc_first(s)
                    res.update(f - {'e'})
                    if 'e' not in f: break
                else: res.add('e')
        self.first[simbolo] = res
        return res

    def calc_follow(self):
        nts = list(self.g.keys())
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
                                f_sig = self.calc_first(sig[0])
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig: self.follow[simb].update(self.follow[nt])

    def generar_predict(self):
        print("\n--- TABLA DE PREDICCIÓN ---")
        es_ll1 = True
        for nt, reglas in self.g.items():
            preds_vistos = []
            for r in reglas:
                f_r = self.calc_first(r[0])
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                print(f" PRED({nt} -> {' '.join(r)}) = {p}")
                for v in preds_vistos:
                    if not p.isdisjoint(v): es_ll1 = False
                preds_vistos.append(p)
        print(f"\n¿Cumple LL(1)?: {'SI' if es_ll1 else 'NO'}")

    def esquema_asdr(self):
        print("\n--- ESTRUCTURA ASDR (Funciones) ---")
        for nt in self.g:
            print(f"void proc_{nt}() {{")
            print(f"  // Logica segun simbolos de entrada")
            print(f"}}")
