class Procesador:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g_orig = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}
        self.predicts = {}

    def ejecutar_analisis_completo(self):
        print("\n" + "="*70)
        print(f" REPORTE TECNICO: {self.nombre}")
        print("="*70)

        # 0. ORIGINAL
        print("\n[PASO 0]: GRAMATICA ORIGINAL")
        for nt, reglas in self.g_orig.items():
            print(f"    {nt} -> {' | '.join([' '.join(r) for r in reglas])}")

        # 1. RECURSIVIDAD
        print("\n[PASO 1]: TRANSFORMACION DE RECURSIVIDAD IZQUIERDA")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            if recursivas:
                print(f"    (!) Detectada recursividad en {nt}. Transformando...")
                nt_p = nt + "p"
                no_rec = [r for r in reglas if r[0] != nt]
                nueva_g[nt] = [r + [nt_p] for r in no_rec]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"        Nuevo {nt}  -> {nueva_g[nt]}")
                print(f"        Nuevo {nt_p} -> {nueva_g[nt_p]}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g

        # 2. CONJUNTOS
        print("\n[PASO 2]: CALCULO DE FIRST Y FOLLOW")
        self._calcular_conjuntos()
        for nt in self.g:
            print(f"    {nt}: FIRST = {self.first[nt]} | FOLLOW = {self.follow[nt]}")

        # 3. PREDICCION Y LL(1)
        print("\n[PASO 3]: CONJUNTOS DE PREDICCION Y VERIFICACION LL(1)")
        es_ll1 = True
        for nt, reglas in self.g.items():
            preds_de_este_nt = []
            for r in reglas:
                f_r = self._get_first_seq(r)
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                
                print(f"    P({nt} -> {' '.join(r)}) = {p}")
                
                # Verificar interseccion para condicion LL(1)
                for conjunto_previo in preds_de_este_nt:
                    if not p.isdisjoint(conjunto_previo):
                        es_ll1 = False
                preds_de_este_nt.append(p)
                self.predicts[(nt, tuple(r))] = p

        print(f"\n>>> RESULTADO FINAL: ¿ES LA GRAMATICA LL(1)? {'SI' if es_ll1 else 'NO'}")

        # 4. LOGICA ASDR
        print("\n[PASO 4]: ESQUEMA LOGICO DEL ANALIZADOR (ASDR)")
        for nt in self.g:
            print(f"  En el metodo para {nt}:")
            for (n, reg), p in self.predicts.items():
                if n == nt:
                    print(f"    - Si el token esta en {p}: elegir regla '{' '.join(reg)}'")

    def _calcular_conjuntos(self):
        for nt in self.g: self.first[nt] = self._get_first_nt(nt)
        self.follow = {nt: set() for nt in self.g}
        self.follow[list(self.g.keys())[0]].add('$')
        for _ in range(5):
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in self.g:
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
