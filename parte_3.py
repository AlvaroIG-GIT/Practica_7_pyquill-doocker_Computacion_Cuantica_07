from pyquil import Program, get_qc
from pyquil.gates import H, X, I, MEASURE



# CÓDIGO ORIGINAL 
from pyquil.gates import H, X, I, MEASURE
prog_original = Program()
ro_orig = prog_original.declare("ro", "BIT", 2)
prog_original += [H(0), MEASURE(0, ro_orig[0])]
prog_original.if_then(ro_orig[0], Program(X(1)), Program(I(1)))
prog_original += MEASURE(1, ro_orig[1])
prog_original.wrap_in_numshots_loop(1000)

print("PROGRAMA QUIL ORIGINAL GENERADO ")
print(prog_original)


# CÓDIGO EDITADO Y EJECUTABLE 
print("EJECUCIÓN DEL PROGRAMA EDITADO ")

# Definición del circuito mediante código Quil plano para evitar errores de Placeholders
quil_code = """
DECLARE ro BIT[2]
H 0
MEASURE 0 ro[0]
JUMP-WHEN @THEN ro[0]
I 1
JUMP @END
LABEL @THEN
X 1
LABEL @END
MEASURE 1 ro[1]
"""

prog = Program(quil_code)
prog.wrap_in_numshots_loop(1000)

qc = get_qc("2q-qvm")
result = qc.run(prog)

print("Resultados de memoria clasica (ro):")
print(result.get_register_map().get("ro"))


# COMENTARIO TÉCNICO 1: Los resultados obtenidos muestran únicamente las parejas de estados 
     # |00> y |11>. Esto confirma que si el primer cúbit medido es 0, se ejecuta la puerta I(1) 
     # dejándolo en 0 (generando |00>); mientras que si es 1, se aplica X(1) invirtiéndolo a 1 
     # (generando |11>), evitando completamente estados cruzados como |01> o |10>.

# COMENTARIO TÉCNICO 2: La correcta visualización de estos patrones de medida valida que la 
     # estructura de control de flujo condicional evalúa de forma exitosa el registro clásico resultante 
     # de la primera medida para aplicar operaciones dinámicas sobre el circuito subsiguiente.
     
     
# COMENTARIO TECNICO 3: La ejecucion de este programa con control de flujo condicional requiere tener 
    # levantados en paralelo los contenedores de Docker: el servidor QVM en el puerto 5000 para la simulacion 
    # de los circuitos y el servidor de compilacion quilc en el puerto 5555 para traducir y resolver de forma 
    # dinamica las instrucciones de salto y etiquetas (LABEL y JUMP).