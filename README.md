# Práctica 7: Computación Cuántica y Natural

Implementación en Python (PyQuil) y simulación mediante QVM y Docker de tres bloques prácticos sobre ruido cuántico, paralelización y control de flujo.

## Estructura del Proyecto
* **`parte_1.py`**: Simulación de ruido de amortiguamiento de amplitud, barrido de gamma, estado de Bell con decoherencia y canal despolarizante con $N$ puertas[cite: 3].
* **`parte_2.py`**: Paralelización de ejecuciones con `ThreadPoolExecutor` y control de exclusión mutua mediante `threading.Lock`[cite: 5].
* **`parte_3.py`**: Control de flujo condicional (`if_then` / etiquetas) ejecutado sobre QVM y compilado mediante el servidor `quilc`[cite: 5, 6].

## Requisitos y Entorno
* Python 3.12[cite: 3]
* Docker (contenedores para QVM y quilc)[cite: 3, 6]
* PyQuil, NumPy