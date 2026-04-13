class Procesador:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}

    def mostrar_paso_a_paso(self):
        print(f"\n{'='*60}")
        print(f"  REVISIÓN TÉCNICA: {self.nombre}")
        print(f{'='*60}")

        # 1. RECURSIVIDAD
        print("\n1. REVISIÓN DE RECURSIVIDAD POR LA IZQUIERDA:")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            if recursivas:
                print(f"   [!] {nt} es recursiva. Transformando...")
                nt_p = nt + "p"
                no_rec = [r for r in reglas if r[0] != nt]
                nueva_g[nt] = [r + [nt_p] for r in no_rec]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"       -> {nt} ahora es: {nueva_g[nt]}")
                print(f"       -> {nt_p} ahora es: {nueva_g[nt_p]}")
            else:
                print(f"   [OK] {nt} no tiene recursividad izquierda.")
                nueva_g[nt] = reglas
        self.g = nueva_g

        # 2. CONJUNTOS
        print("\n2. CÁLCULO DE CONJUNTOS:")
        self._calc_sets()
        for nt in self.g:
            print(f"   NT {nt}: FIRST = {self.first[nt]}, FOLLOW = {self.follow[nt]}")

        # 3. ESQUEMA ANALIZADOR (Lógica de decisión)
        print("\n3. ESQUEMA DEL ANALIZADOR (LÓGICA ASDR):")
        for nt, reglas in self.g.items():
            print(f"\n   Al procesar el No Terminal '{nt}':")
            for r in reglas:
                f_r = self._get_first_seq(r)
                pred = f_r - {'e'}
                if 'e' in f_r: pred.update(self.follow[nt])
                
                print(f"      - Si el token es {pred}:")
                print(f"        ENTONCES aplicar regla: {' '.join(r)}")

    def _calc_sets(self):
        # Lógica simplificada de First/Follow
        for nt in self.g: self.first[nt] = self._get_first_nt(nt)
        self.follow = {nt: set() for nt in self.g}
        self.follow[list(self.g.keys())[0]].add('$')
        for _ in range(3): # Estabilización
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb[0].isupper():
                            sig = r[i+1:]
                            if not sig: self.follow[simb].update(self.follow[nt])
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
