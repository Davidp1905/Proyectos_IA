# Proyecto 3:  Métodos probabilísticos

Este proyecto implementa un motor de inferencia por enumeración para redes bayesianas, desarrollado como parte del curso **Introducción a la Inteligencia Artificial**. La herramienta permite calcular distribuciones de probabilidad condicional, visualizar trazas de los cálculos, y probar redes tanto definidas por el estudiante como ejemplos vistos en clase.

## ⚙️ Funcionalidades principales

- Carga dinámica de grafos desde archivos `.csv`.
- Lectura de tablas de probabilidad condicional (CPTs).
- Inferencia por enumeración completa.
- Cálculo de probabilidades conjuntas.
- Normalización automática de resultados.
- Trazas paso a paso del cálculo de inferencia.
- Pruebas con red personalizada (`accidente`) y con red del taller (`appointment`).

---

## ▶️ Ejecución del proyecto

1. Asegúrate de tener Python 3 instalado.
2. Instala las dependencias (solo `pandas` y `networkx`):

```bash
pip install pandas networkx
```

3. Ejecuta el archivo principal:

```bash
python proyecto_3.py
```

---

### ✔️ Red personalizada (accidentes)

Consulta:

```python
P(accidente | clima = niebla, conductor = cansado)
```

Resultado:

```
P(accidente = si) ≈ 0.2261
P(accidente = no) ≈ 0.7738
```

### ✔️ Red del ejemplo de clase

Consulta:

```python
P(appointment | rain = light, maintenance = no)
```

Resultado esperado (como en clase):

```
P(appointment = attend) ≈ 0.81
P(appointment = miss) ≈ 0.19
```

---

## 📋 Generación de trazas

La función `inferir_mostrando_traza(...)` permite mostrar el paso a paso de los cálculos realizados durante la inferencia, incluyendo:

- Combinaciones de variables ocultas
- Multiplicación de factores de probabilidad locales
- Suma total no normalizada
- Distribución final normalizada

Esto permite verificar la **correctitud del motor de inferencia** según el enunciado del proyecto.

---

## 📌 Archivos incluidos

- `proyecto_3.py`: contiene la clase `RedBayesiana` y todos los métodos.
- Carpeta `probabilidades/`: red de accidentes.
- Carpeta `ejemplo_clase/`: red de ejemplo del taller.

---
