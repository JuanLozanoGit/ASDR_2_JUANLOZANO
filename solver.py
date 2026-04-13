class Procesador:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}

    def ejecutar_analisis_completo(self):
        print("\n" + "="*60)
        print(f" ANALISIS PASO A PASO: {self.nombre}")
        print("="*60)

        # --- PASO 1: RECURSIVIDAD ---
        print("\n[1] REVISION DE RECURSIVIDAD IZQUIERDA:")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            if recursivas:
                print(f"    - Detectada en {nt}. Aplicando transformacion A -> bA' / A' -> aA'...")
                nt_p = nt + "p"
                no_rec = [r for r in reglas if r[0] != nt]
                nueva_g[nt] = [r + [nt_p] for r in no_rec]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"      Antes: {nt} -> {reglas}")
                print(f"      Despues: {nt} -> {nueva_g[nt]} | {nt_p} -> {nueva_g[nt_p]}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g

        # --- PASO 2: FIRST Y FOLLOW ---
        print("\n[2] CALCULO DE CONJUNTOS:")
        self._calcular_conjuntos()
        for nt in self.g:
            print(f"    - {nt}: FIRST = {self.first[nt]}, FOLLOW = {self.follow[nt]}")

        # --- PASO 3: LOGICA ASDR ---
        print("\n[3] ESQUEMA DE DECISION (ASDR):")
        for nt, reglas in self.g.items():
            print(f"\n    Para el No Terminal '{nt}':")
            for r in reglas:
                # Calcular prediccion para la regla
                f_r = self._get_first_seq(r)
                pred = f_r - {'e'}
                if 'e' in f_r: pred.update(self.follow[nt])
                
                print(f"      * Si el proximo token es {pred}:")
                print(f"        -> Se expande con la regla: {' '.join(r)}")

    def _calcular_conjuntos(self):
        # Primero calculamos FIRST
        for nt in self.g: self.first[nt] = self._get_first_nt(nt)
        # Luego FOLLOW
        self.follow = {nt: set() for nt in self.g}
        self.follow[list(self.g.keys())[0]].add('$')
        for _ in range(5): # Iteracion para estabilizar conjuntos
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in self.g: # Es No Terminal
                            sig = r[i+1:]
                            if not sig:
                                self.follow[simb].update(self.follow[nt])
                            else:
                                f_sig = self._get_first_seq(sig)
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig: self.follow[simb].update(self.follow[nt])

    def _get_first_nt(self, nt):
        res = set()
        for r in self.g.get(nt, []):
            if r[0] == 'e': res.add('e')
            elif not r[0][0].isupper(): res.add(r[0])
            else: res.update(self._get_first_nt(r[0]))
        return res

    def _get_first_seq(self, seq):
        if seq[0] == 'e': return {'e'}
        if not seq[0][0].isupper(): return {seq[0]}
        return self.first.get(seq[0], set())
