# Proyecto 2: Motor de Inferencia por Resolución

Este proyecto implementa un motor de inferencia lógico basado en el algoritmo de **resolución por refutación** para lógica de primer orden, desarrollado en Python. Permite probar si una conclusión se deduce de una base de conocimiento, utilizando tanto resolución tradicional como resolución dirigida por la meta.

## 📌 Características

- Resolución clásica entre todos los pares de cláusulas.
- Resolución dirigida por la meta: comienza desde la negación de la conclusión.
- Unificación de variables simbólicas.
- Ejecución de ejemplos clásicos como:
  - Marco odia a César.
  - ¿La curiosidad mató al gato?
  - Teoremas matemáticos simples como “Si un número es par, entonces su doble también es par”.

## 🧠 Estructura del Código

- `crear_literal`: construye un literal con predicado y argumentos.
- `resolver`: aplica resolución entre dos cláusulas.
- `resolucion(lista_clausulas)`: resolución tradicional.
- `resolucion_dirigida(lista_clausulas)`: resolución enfocada en la meta.
- `lista_clausulas`: base de conocimiento, lista de cláusulas en forma normal conjuntiva (FNC).

## ▶ Ejecución

```bash
python motor_resolucion.py
