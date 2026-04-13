class Procesador:
    def __init__(self, nombre, g_original):
        self.nombre = nombre
        self.g = {k: [list(r) for r in v] for k, v in g_original.items()}
        self.first = {}
        self.follow = {}
        self.predict = {}

    def revisar_recursividad(self):
        print(f"\n>>> PASO 1: REVISION DE RECURSIVIDAD ({self.nombre})")
        nueva_g = {}
        for nt, reglas in self.g.items():
            recursivas = [r for r in reglas if r[0] == nt]
            no_recursivas = [r for r in reglas if r[0] != nt]
            
            if recursivas:
                print(f"  [!] Detectada recursividad en {nt}: {recursivas}")
                nt_p = nt + "p"
                # Transformacion: A -> bA' | A' -> aA' | e
                nueva_g[nt] = [r + [nt_p] for r in no_recursivas]
                nueva_g[nt_p] = [r[1:] + [nt_p] for r in recursivas] + [['e']]
                print(f"      Nueva forma: {nt} -> {nueva_g[nt]}")
                print(f"      Nueva forma: {nt_p} -> {nueva_g[nt_p]}")
            else:
                nueva_g[nt] = reglas
        self.g = nueva_g

    def calcular_first(self, simbolo):
        if not simbolo[0].isupper(): return {simbolo}
        if simbolo in self.first: return self.first[simbolo]
        res = set()
        for r in self.g.get(simbolo, []):
            if r[0] == 'e': res.add('e')
            else:
                for s in r:
                    f = self.calcular_first(s)
                    res.update(f - {'e'})
                    if 'e' not in f: break
                else: res.add('e')
        self.first[simbolo] = res
        return res

    def calcular_follow(self):
        print(f"\n>>> PASO 2: CONJUNTOS FIRST Y FOLLOW")
        nts = list(self.g.keys())
        for nt in nts: self.calcular_first(nt)
        for nt, val in self.first.items(): print(f"  FIRST({nt}) = {val}")

        self.follow = {nt: set() for nt in nts}
        self.follow[nts[0]].add('$')
        
        for _ in range(len(nts)):
            for nt, reglas in self.g.items():
                for r in reglas:
                    for i, simb in enumerate(r):
                        if simb in nts:
                            sig = r[i+1:]
                            if not sig:
                                self.follow[simb].update(self.follow[nt])
                            else:
                                f_sig = self.calcular_first(sig[0])
                                self.follow[simb].update(f_sig - {'e'})
                                if 'e' in f_sig: self.follow[simb].update(self.follow[nt])
        for nt, val in self.follow.items(): print(f"  FOLLOW({nt}) = {val}")

    def generar_predict(self):
        print(f"\n>>> PASO 3: CONJUNTOS DE PREDICCION (LL1)")
        for nt, reglas in self.g.items():
            for r in reglas:
                f_r = self.calcular_first(r[0])
                p = f_r - {'e'}
                if 'e' in f_r: p.update(self.follow[nt])
                self.predict[(nt, tuple(r))] = p
                print(f"  P({nt} -> {' '.join(r)}) = {p}")

    def esquema_asdr(self):
        print(f"\n>>> PASO 4: ESQUEMA ANALIZADOR (ASDR)")
        for nt in self.g:
            print(f"def proc_{nt}():")
            first_regla = True
            for (n, reg), p in self.predict.items():
                if n == nt:
                    token_list = list(p)
                    instr = "if" if first_regla else "elif"
                    print(f"    {instr} token in {token_list}:")
                    for s in reg:
                        if s == 'e': print(f"        pass")
                        elif s[0].isupper(): print(f"        proc_{s}()")
                        else: print(f"        match('{s}')")
                    first_regla = False
            print(f"    else: error('Error en {nt}')\n")
