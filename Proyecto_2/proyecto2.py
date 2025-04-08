# Representación de literales y cláusulas

def crear_literal(predicado, argumentos, negado=False):
    return {
        "negado": negado,
        "predicado": predicado,
        "argumentos": argumentos
    }

# Verificación de si dos literales son complementarios

def es_complementario(l1, l2):
    return (
        l1['predicado'] == l2['predicado'] and
        l1['negado'] != l2['negado'] and
        len(l1['argumentos']) == len(l2['argumentos'])
    )

# Unificación simple

def unificar(arg1, arg2, sustituciones):
    if sustituciones is None:
        return None
    elif arg1 == arg2:
        return sustituciones
    elif es_variable(arg1):
        return unificar_variable(arg1, arg2, sustituciones)
    elif es_variable(arg2):
        return unificar_variable(arg2, arg1, sustituciones)
    else:
        return None

def unificar_literal(l1, l2):
    sustituciones = {}
    for a1, a2 in zip(l1['argumentos'], l2['argumentos']):
        sustituciones = unificar(a1, a2, sustituciones)
        if sustituciones is None:
            return None
    return sustituciones

def unificar_variable(var, val, sustituciones):
    if var in sustituciones:
        return unificar(sustituciones[var], val, sustituciones)
    elif val in sustituciones:
        return unificar(var, sustituciones[val], sustituciones)
    else:
        sustituciones[var] = val
        return sustituciones

def es_variable(arg):
    return arg[0].islower()

# Aplicar sustituciones a una cláusula

def aplicar_sustitucion(clausula, sustituciones):
    nueva = []
    for lit in clausula:
        nuevos_args = [sustituciones.get(arg, arg) for arg in lit['argumentos']]
        nuevo_lit = crear_literal(lit['predicado'], nuevos_args, lit['negado'])
        nueva.append(nuevo_lit)
    return nueva

# Resolver dos cláusulas

def resolver(c1, c2):
    for l1 in c1:
        for l2 in c2:
            if es_complementario(l1, l2):
                sustituciones = unificar_literal(l1, l2)
                if sustituciones is not None:
                    nueva_c1 = [lit for lit in c1 if lit != l1]
                    nueva_c2 = [lit for lit in c2 if lit != l2]
                    resolvente = aplicar_sustitucion(nueva_c1 + nueva_c2, sustituciones)
                    return resolvente
    return None

# Motor principal de resolución
from itertools import combinations

def literal_a_tupla(lit):
    return (lit['negado'], lit['predicado'], tuple(lit['argumentos']))

def clausula_a_frozenset(clausula):
    return frozenset([literal_a_tupla(lit) for lit in clausula])

def resolucion(kb):
    clausulas = [clausula_a_frozenset(clausula) for clausula in kb]
    nuevas = set(clausulas)
    resueltos = set()

    while True:
        combinaciones = list(combinations(nuevas, 2))
        nuevos_resultados = set()
        for c1, c2 in combinaciones:
            par = frozenset([c1, c2])
            if par in resueltos:
                continue
            resueltos.add(par)
            # reconstruir literales desde tuplas para resolver
            cl1 = [crear_literal(pred, list(args), negado) for (negado, pred, args) in c1]
            cl2 = [crear_literal(pred, list(args), negado) for (negado, pred, args) in c2]
            resolvente = resolver(cl1, cl2)
            if resolvente is not None:
                if len(resolvente) == 0:
                    print("Se encontró cláusula vacía. La conclusión es verdadera.")
                    return True
                resolvente_set = clausula_a_frozenset(resolvente)
                if resolvente_set not in nuevas:
                    nuevos_resultados.add(resolvente_set)
        if not nuevos_resultados:
            print("No se pudo demostrar la conclusión. No se encontró contradicción.")
            return False
        nuevas.update(nuevos_resultados)



# Ejemplo del caso de Marco y César
# if __name__ == "__main__":
#     kb = [
#         # 1. Hombre(Marco)
#         [crear_literal("Hombre", ["Marco"])],

#         # 2. Pompeyano(Marco)
#         [crear_literal("Pompeyano", ["Marco"])],

#         # 3. ∀x Pompeyano(x) ⇒ Romano(x) → ¬Pompeyano(x) ∨ Romano(x)
#         [crear_literal("Pompeyano", ["x3"], negado=True), crear_literal("Romano", ["x3"])],

#         # 4. Gobernante(Cesar)
#         [crear_literal("Gobernante", ["Cesar"])],

#         # 5. ∀x Romano(x) ⇒ Leal(x, Cesar) ∨ Odia(x, Cesar)
#         #    → ¬Romano(x) ∨ Leal(x, Cesar) ∨ Odia(x, Cesar)
#         [crear_literal("Romano", ["x5"], negado=True), crear_literal("Leal", ["x5", "Cesar"]), crear_literal("Odia", ["x5", "Cesar"])],

#         # 6. ∀x ∀y (Hombre(x) ∧ Gobernante(y) ∧ IntentaAsesinar(x, y)) ⇒ ¬Leal(x, y)
#         #    → ¬Hombre(x) ∨ ¬Gobernante(y) ∨ ¬IntentaAsesinar(x, y) ∨ ¬Leal(x, y)
#         [crear_literal("Hombre", ["x6"], negado=True), crear_literal("Gobernante", ["y6"], negado=True),
#          crear_literal("IntentaAsesinar", ["x6", "y6"], negado=True), crear_literal("Leal", ["x6", "y6"], negado=True)],

#         # 7. IntentaAsesinar(Marco, Cesar)
#         [crear_literal("IntentaAsesinar", ["Marco", "Cesar"])],

#         # 8. ¬Odia(Marco, Cesar) ← negación de la conclusión
#         [crear_literal("Odia", ["Marco", "Cesar"], negado=True)]
#     ]

#     print("\nEjecutando resolución para el caso de Marco y César...")
#     resolucion(kb)



# Ejemplo del caso "¿La curiosidad mató al gato?"
if __name__ == "__main__":
    kb = [
        # 1. ∀x (∀y Animal(y) → Ama(x,y)) → ∃z Ama(z,x)
        # Se transforma en forma clausal: ¬Animal(y) ∨ Ama(x, y)
        [crear_literal("Animal", ["y"], negado=True), crear_literal("Ama", ["x", "y"])],

        # 2. ∀x ∀y (Mata(x,y) ∧ Animal(y)) → ¬∃z Ama(z,x)
        # Se transforma en: ¬Mata(x,y) ∨ ¬Animal(y) ∨ ¬Ama(z,x)
        [crear_literal("Mata", ["x", "y"], negado=True), crear_literal("Animal", ["y"], negado=True), crear_literal("Ama", ["z", "x"], negado=True)],

        # 3. ∀y Animal(y) → Ama(Jack, y) → ¬Animal(y) ∨ Ama(Jack, y)
        [crear_literal("Animal", ["y"], negado=True), crear_literal("Ama", ["Jack", "y"])],

        # 4. Mata(Jack, Tuna) ∨ Mata(Curiosidad, Tuna)
        [crear_literal("Mata", ["Jack", "Tuna"]), crear_literal("Mata", ["Curiosidad", "Tuna"])],

        # 5. Gato(Tuna)
        [crear_literal("Gato", ["Tuna"])],

        # 6. ∀x Gato(x) → Animal(x) → ¬Gato(x) ∨ Animal(x)
        [crear_literal("Gato", ["x"], negado=True), crear_literal("Animal", ["x"])],

        # 7. Negación de la conclusión: ¬Mata(Curiosidad, Tuna)
        [crear_literal("Mata", ["Curiosidad", "Tuna"], negado=True)]
    ]

    print("\nEjecutando resolución para el caso de la curiosidad y el gato...")
    resolucion(kb)


# Ejemplo de teorema matemático: "Si un número es par, entonces su doble también es par"

# if __name__ == "__main__":
#     kb = [
#         # 1. ¬Par(2) ∨ Par(4)
#         [crear_literal("Par", ["2"], negado=True), crear_literal("Par", ["4"])],

#         # 2. Par(2)
#         [crear_literal("Par", ["2"])],

#         # 3. Negación de la conclusión: ¬Par(4)
#         [crear_literal("Par", ["4"], negado=True)]
#     ]

#     print("Ejecutando resolución para el teorema: Si un número es par, entonces su doble también es par...")
#     resolucion(kb)
