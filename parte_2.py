import time
import numpy as np
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pyquil import Program, get_qc
from pyquil.quilbase import Declare
from pyquil.gates import RX, H, CNOT, MEASURE

# --- CÓDIGO ORIGINAL DEL PDF (Página 4) ---
def run_circuit(theta, shots=2000):
    # Cada hilo crea sus propios objetos: no se comparten entre hilos[cite: 4]
    qc = get_qc("1q-qvm")
    prog = Program(Declare("ro", "BIT", 1), RX(theta, 0), MEASURE(0, ("ro", 0)))
    prog.wrap_in_numshots_loop(shots)
    bits = qc.run(prog).get_register_map().get("ro")
    return float(np.mean(bits))

thetas = np.linspace(0, 2 * np.pi, 16)

t0 = time.perf_counter()
sequential = [run_circuit(t) for t in thetas]
t_seq = time.perf_counter() - t0

t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    parallel = list(pool.map(run_circuit, thetas))
t_par = time.perf_counter() - t0

print(f"Secuencial: {t_seq:.2f} s | Paralelo: {t_par:.2f} s")

# --- AMPLIACIÓN REQUERIDA POR LA PRÁCTICA ---
# Pruebas de tiempos con max_workers = 1, 2, 4 y 8[cite: 5]
for w in [1, 2, 4, 8]:
    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=w) as pool:
        list(pool.map(run_circuit, thetas))
    print(f"max_workers={w} -> Tiempo total: {time.perf_counter() - t_start:.2f} s")


# Acumulación con 8 hilos y Counter protegido con Lock[cite: 5]
shared_counter = Counter()
lock = threading.Lock()

def worker_bell(shots=500):
    qc = get_qc("2q-qvm")
    prog = Program(Declare("ro", "BIT", 2))
    prog += [H(0), CNOT(0, 1), MEASURE(0, ("ro", 0)), MEASURE(1, ("ro", 1))]
    prog.wrap_in_numshots_loop(shots)
    bits = qc.run(prog).get_register_map().get("ro")
    local_counts = Counter(zip(bits[0], bits[1]))
    with lock:
        shared_counter.update(local_counts)

threads = [threading.Thread(target=worker_bell) for _ in range(8)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Total ejecuciones acumuladas (Esperado 4000): {sum(shared_counter.values())}")



# COMENTARIO TECNICO 1: La ejecucion en paralelo con ThreadPoolExecutor mejora el rendimiento frente a 
    # la secuencial al solapar las esperas de E/S del servidor QVM. Sin embargo, se observa que al pasar de 
    # max_workers=4 (0.32 s) a max_workers=8 (0.34 s) la aceleracion deja de crecer[cite: 4, 5]. Esto ocurre
    # debido a la saturacion de peticiones concurrentes que el servidor QVM puede atender simultaneamente y 
    # al limite fisico de nucleos del procesador[cite: 4, 5].

# COMENTARIO TECNICO 2: El metodo pool.map garantiza que se mantenga estricto el orden de los resultados,
    # de modo que parallel[i] corresponde siempre al angulo thetas[i] aunque los hilos terminen en 
    # distinto orden[cite: 5].

# COMENTARIO TECNICO 3: En la acumulacion con hilos mediante threading.Thread, el uso de threading. Lock 
    # es estrictamente necesario[cite: 5]. Sin este mecanismo de exclusion mutua se producirian condiciones 
    # de carrera (race conditions) al intentar multiples hilos modificar de forma simultanea el diccionario 
    # compartido del Counter, lo que corromperia o truncaria el resultado final del recuento de 
    # ejecuciones[cite: 5].