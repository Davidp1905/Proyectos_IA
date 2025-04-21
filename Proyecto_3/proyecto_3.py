import pandas as pd
import networkx as nx
import os
import itertools

class RedBayesiana:
    # Constructor de la clase RedBayesiana
    #  Inicializa la estructura de grafo dirigida y carga las probabilidades desde los archivos CSV.
    def __init__(self, grafo_path, prob_path):
        self.grafo_path = grafo_path
        self.prob_path = prob_path
        self.grafo = nx.DiGraph()
        self.probabilidades = {}  # Nodo → CPT (DataFrame)
        self._cargar_grafo()
        self._cargar_probabilidades()
    
    # Carga el grafo desde el archivo CSV de aristas
    def _cargar_grafo(self):
        df = pd.read_csv(self.grafo_path)
        for _, fila in df.iterrows():
            self.grafo.add_edge(fila["origen"], fila["destino"])
    
    # Carga las tablas de probabilidad condicional (CPTs) desde archivos CSV.
    # Recorre el directorio de probabilidades especificado y carga en memoria cada archivo como un DataFrame, indexado por el nombre del nodo (sin la extensión .csv)
    def _cargar_probabilidades(self):
        for archivo in os.listdir(self.prob_path):
            if archivo.endswith(".csv"):
                nodo = archivo.replace(".csv", "")
                ruta = os.path.join(self.prob_path, archivo)
                self.probabilidades[nodo] = pd.read_csv(ruta)
    
    # Imprime en consola la estructura de la red bayesiana cargada: nodos y aristas con direcciones
    def mostrar_grafo(self):
        print("Estructura de la red bayesiana:")
        print("Nodos:", list(self.grafo.nodes))
        print("Aristas:")
        for edge in self.grafo.edges:
            print(f"  {edge[0]} → {edge[1]}")
    
    # Muestra la tabla de probabilidad condicional de un nodo específico
    def mostrar_tabla(self, nodo):
        if nodo in self.probabilidades:
            print(f"\nTabla de probabilidad condicional para '{nodo}':")
            print(self.probabilidades[nodo])
        else:
            print(f"No se encontró CPT para el nodo '{nodo}'")
           
    # Realiza inferencia por enumeración para una variable objetivo, dado un conjunto de evidencia     
    # Parámetros:
    #     - objetivo (str): Nombre del nodo cuya probabilidad condicional se desea calcular.
    #     - evidencia (dict): Diccionario con la forma {variable: valor_observado}.

    #     Retorna:
    #     - Un diccionario con la distribución de probabilidad normalizada para los posibles valores del nodo objetivo.   
    def inferir(self, objetivo, evidencia):
        # Realiza inferencia por enumeración:
        # Retorna un diccionario con los valores posibles del nodo objetivo y su probabilidad.
    
        # 1. Obtener todos los valores posibles del nodo objetivo
        valores_objetivo = self.probabilidades[objetivo][objetivo].unique()
        resultado = {}

        # 2. Identificar las variables ocultas (ni objetivo ni evidencia)
        variables = list(self.grafo.nodes)
        ocultas = [v for v in variables if v != objetivo and v not in evidencia]

        # 3. Para cada valor del objetivo, calcular P(x, e)
        for val in valores_objetivo:
            # Construir asignación parcial
            asignacion = evidencia.copy()
            asignacion[objetivo] = val
            resultado[val] = self._enumerar(asignacion, ocultas)

        # 4. Normalizar
        return self._normalizar(resultado)
    
    
    # Calcula la suma total de probabilidades conjuntas para todas las combinaciones posibles de las variables ocultas en una asignación.
    # Parámetros:
    # - asignacion (dictionary): Asignación parcial que incluye la evidencia y el valor del nodo objetivo.
    # - ocultas (list): Lista de nombres de variables ocultas.
    # Retorna:
    # - Suma total de las probabilidades conjuntas para todas las combinaciones de las variables ocultas.
    def _enumerar(self, asignacion, ocultas):
        # Suma sobre todas las combinaciones posibles de variables ocultas
        
        if not ocultas:
            return self._probabilidad_conjunta(asignacion)

        # Obtener valores posibles de cada variable oculta
        dominios = [self.probabilidades[v][v].unique() for v in ocultas]
        combinaciones = list(itertools.product(*dominios))

        total = 0
        for valores in combinaciones:
            extendida = asignacion.copy()
            for i, var in enumerate(ocultas):
                extendida[var] = valores[i]
            total += self._probabilidad_conjunta(extendida)
        return total

    # Calcula la probabilidad conjunta completa para una asignación específica de valores a todas las variables de la red.
    #   Parámetros:
    #    - asignacion (dict): Diccionario con valores asignados a cada nodo.
    #   Retorna:
    #    - El producto de todas las probabilidades locales P(v | padres(v)) según la asignación.
    def _probabilidad_conjunta(self, asignacion):
        # Multiplica las probabilidades locales P(v | padres(v)) de cada nodo
        total = 1.0
        for nodo in self.grafo.nodes:
            total *= self._probabilidad_local(nodo, asignacion)
        return total

    # Busca la probabilidad local P(nodo = valor | padres) en la CPT del nodo correspondiente.
    #   Parámetros:
    #     - nodo (str): Nombre del nodo cuya probabilidad se desea consultar.
    #     - asignacion (dict): Asignación completa que incluye valores para el nodo y sus padres.
    #   Retorna:
    #     - La probabilidad correspondiente extraída de la tabla CPT del nodo.
    #     - Si no se encuentra una coincidencia, retorna un valor muy pequeño (1e-9) para evitar errores de multiplicación por cero.
    def _probabilidad_local(self, nodo, asignacion):
        """
        Busca P(nodo = valor | padres) en la CPT correspondiente.
        """
        df = self.probabilidades[nodo]
        valor = asignacion[nodo]
        padres = list(self.grafo.predecessors(nodo))

        query = {nodo: valor}
        for padre in padres:
            query[padre] = asignacion[padre]

        # Filtrar el dataframe
        filtro = (df[nodo] == valor)
        for p in padres:
            filtro &= (df[p] == query[p])

        fila = df[filtro]
        if fila.empty:
            print(f"\tNo se encontró probabilidad para: {query}")
            return 1e-9  # valor muy pequeño para evitar cero
        return float(fila["prob"].values[0])

    # Normaliza una distribución de probabilidad para que la suma de sus valores sea 1.
    #   Parámetros:
    #     - distribucion (dict): Diccionario {valor: probabilidad_no_normalizada}.
    #   Retorna:
    #     - Un nuevo diccionario con la distribución normalizada.
    def _normalizar(self, distribucion):
        total = sum(distribucion.values())
        if total == 0:
            return {k: 0 for k in distribucion}
        return {k: v / total for k, v in distribucion.items()}

    # Función que muestra todas las multiplicaciones y el paso a paso.
    # Combina las funciones inferir, _enumerar y _probabilidad_conjunta en una
    def inferir_mostrando_traza(self, objetivo, evidencia):
        print(f"\nTrazando P({objetivo} | {', '.join([f'{k}={v}' for k,v in evidencia.items()])})\n")

        valores_objetivo = self.probabilidades[objetivo][objetivo].unique()
        variables = list(self.grafo.nodes)
        ocultas = [v for v in variables if v != objetivo and v not in evidencia]
        resultado = {}

        for val in valores_objetivo:
            print(f"Para {objetivo} = {val}:")
            asignacion = evidencia.copy()
            asignacion[objetivo] = val

            dominios = [self.probabilidades[v][v].unique() for v in ocultas]
            combinaciones = list(itertools.product(*dominios))

            total = 0
            for valores in combinaciones:
                extendida = asignacion.copy()
                for i, var in enumerate(ocultas):
                    extendida[var] = valores[i]

                prob_total = 1.0
                trazas = []
                for nodo in self.grafo.nodes:
                    p = self._probabilidad_local(nodo, extendida)
                    prob_total *= p
                    trazas.append(f"P({nodo}={extendida[nodo]} | padres) = {p:.5f}")

                print("  Combinación:", {k: extendida[k] for k in ocultas})
                print("    " + " * ".join(trazas))
                print(f"    → Producto total: {prob_total:.8f}\n")

                total += prob_total

            resultado[val] = total
            print(f"Suma total (no normalizada) para {val}: {total:.8f}\n")

        print("Distribución sin normalizar:", resultado)
        normalizada = self._normalizar(resultado)
        print("Distribución normalizada:")
        for val, prob in normalizada.items():
            print(f"  P({objetivo}={val} | evidencia) = {prob:.5f}")
        return normalizada


# Ejemplo de uso
if __name__ == "__main__":
    
    # Ejemplo de clase
    # Para probar el otro ejemplo, comentar esta parte y descomentar la de abajo
    # Cargar datos ejemplo clase
    ej_clase = RedBayesiana("ejemplo_clase/graph.csv", "ejemplo_clase")
    
    # Mostrar la estructura de la red bayesiana
    ej_clase.mostrar_grafo()

    resultado = ej_clase.inferir_mostrando_traza("appointment", {
        "rain": "light",
        "maintenance": "no"
    })
    
    resultado = ej_clase.inferir("appointment", {
        "rain": "light",
        "maintenance": "no"
    })
    print("\nResultado de la inferencia:")
    for val, prob in resultado.items():
        print(f"P(accidente = {val}) = {prob:.4f}")

"""
    # Ejemplo propio accidentes
    
    # Cargar datos del ejemplo
    # red = RedBayesiana(grafo_path="probabilidades/graph.csv", prob_path="probabilidades")
    
    # Mostrar la estructura de la red bayesiana
    # red.mostrar_grafo()
    
    # Mostrar la tabla de probabilidades. Se cambia el nodo para ver otra tabla (clima, trafico, visibilidad, conductor, vehiculo, accidente)
    # red.mostrar_tabla("vehiculo")  
    
    

    # Ejemplos, en efecto son muchos, pero se puede escoger de estos u otros más sencillos :D
    resultado = red.inferir("accidente", evidencia={
        "clima": "lluvioso",
        "conductor": "cansado",
        "vehiculo": "mala"
    })

    print("\nResultado de la inferencia:")
    for val, prob in resultado.items():
        print(f"P(accidente = {val}) = {prob:.4f}")
        
    resultado = red.inferir("accidente", {
        "clima": "niebla",
        "conductor": "cansado"
    })
    print("Caso 1:", resultado)

    resultado = red.inferir("accidente", {
        "clima": "soleado",
        "vehiculo": "buena",
        "visibilidad": "buena"
    })
    print("Caso 2:", resultado)

    resultado = red.inferir("accidente", {
        "conductor": "cansado",
        "vehiculo": "mala",
        "visibilidad": "mala"
    })
    print("Caso 3:", resultado)

    
    # resultado = red.inferir("accidente", {
    #     "clima": "niebla",
    #     "conductor": "cansado"
    # })

    """
    
