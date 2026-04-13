class ProcesadorGramatica:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}
        self.predict = {}

    def eliminar_recursividad(self):
        print(f"\n--- PASO 1: REVISIÓN Y TRANSFORMACIÓN DE RECURSIVIDAD ---")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            no_recursivas = [r for r in reglas if r[0] != nt]
            
            if recursivas:
                print(f"  [!] Detectada recursividad izquierda en {nt} -> {recursivas}")
                nt_p = nt + "p"
                # Transformación estándar: A -> b A' | A' -> a A' | e
                nueva_g[nt] = [r + [nt_p] for r in no_recursivas]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"      Nueva producción: {nt} -> {' | '.join([' '.join(x) for x in nueva_g[nt]])}")
                print(f"      Nueva producción: {nt_p} -> {' | '.join([' '.join(x) for x in nueva_g[nt_p]])}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g

    def calcular_conjuntos(self):
        print(f"\n--- PASO 2: CÁLCULO DE CONJUNTOS (FIRST Y FOLLOW) ---")
        nts = list(self.g.keys())
        
        # Lógica FIRST
        for nt in nts:
            self.first[nt] = self._get_first(nt)
            print(f"  FIRST({nt}) = {self.first[nt]}")
            
        # Lógica FOLLOW
        self.follow = {nt: set() for nt in nts}
        self.follow[nts[0]].add('$')
        print(f"  Iniciando FOLLOW con símbolo inicial: FOLLOW({nts[0]}) incluye '$'")
        
        for _ in range(len(nts)): # Iterar para propagar
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in nts:
                            sig = r[i+1:]
                            antes = set(self.follow[simb])
                            if not sig:
                                self.follow[simb].update(self.follow[nt])
                            else:
                                f_sig = self._get_first_de_secuencia(sig)
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig:
                                    self.follow[simb].update(self.follow[nt])
                            if antes != self.follow[simb]:
                                print(f"  Actualizando FOLLOW({simb}) usando regla {nt}->{' '.join(r)}: {self.follow[simb]}")

    def _get_first(self, simbolo):
        if not simbolo[0].isupper(): return {simbolo}
        res = set()
        for r in self.g.get(simbolo, []):
            if r[0] == 'e': res.add('e')
            else:
                for s in r:
                    f = self._get_first(s)
                    res.update(f - {'e'})
                    if 'e' not in f: break
                else: res.add('e')
        return res

    def _get_first_de_secuencia(self, secuencia):
        res = set()
        for s in secuencia:
            f = self._get_first(s)
            res.update(f - {'e'})
            if 'e' not in f: break
        else: res.add('e')
        return res

    def analizar_predict_y_ll1(self):
        print(f"\n--- PASO 3: CONJUNTOS DE PREDICCIÓN Y REGLAS ---")
        es_ll1 = True
        for nt, reglas in self.g.items():
            vistos = []
            for r in reglas:
                f_r = self._get_first_de_secuencia(r)
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                print(f"  P({nt} -> {' '.join(r)}) = FIRST({r}) U FOLLOW({nt}) si aplica = {p}")
                for v in vistos:
                    if not p.isdisjoint(v):
                        print(f"  [ERROR] Conflicto LL(1) en NT '{nt}': {p} e {v} no son disjuntos.")
                        es_ll1 = False
                vistos.append(p)
                self.predict[(nt, tuple(r))] = p
        print(f"\n> CONCLUSIÓN: {'CUMPLE LL(1)' if es_ll1 else 'NO CUMPLE LL(1)'}")

    def imprimir_asdr(self):
        print(f"\n--- PASO 4: ESQUEMA DEL ANALIZADOR SINTÁCTICO DESCENDENTE RECURSIVO ---")
        for nt in self.g:
            print(f"def proc_{nt}():")
            print(f"    print('Entrando a {nt}, token actual:', token)")
            primera = True
            for (n, reg), p in self.predict.items():
                if n == nt:
                    cond = "if" if primera else "elif"
                    print(f"    {cond} token in {list(p)}:")
                    for token_reg in reg:
                        if token_reg == 'e':
                            print(f"        pass # Derivación vacía")
                        elif token_reg[0].isupper():
                            print(f"        proc_{token_reg}()")
                        else:
                            print(f"        match('{token_reg}')")
                    primera = False
            print(f"    else: error('Token inesperado en {nt}')\n")
