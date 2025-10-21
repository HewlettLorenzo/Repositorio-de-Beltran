import math

# Dataset de ejemplo
datos = [
    {"edad": 22, "departamento": "IT", "nivel_educativo": "terciario", "en_formacion": True},
    {"edad": 24, "departamento": "IT", "nivel_educativo": "universitario", "en_formacion": True},
    {"edad": 21, "departamento": "RRHH", "nivel_educativo": "terciario", "en_formacion": True},
    {"edad": 35, "departamento": "IT", "nivel_educativo": "universitario", "en_formacion": False},
    {"edad": 40, "departamento": "Finanzas", "nivel_educativo": "maestría", "en_formacion": False},
    {"edad": 29, "departamento": "RRHH", "nivel_educativo": "universitario", "en_formacion": False},
    {"edad": 23, "departamento": "IT", "nivel_educativo": "terciario", "en_formacion": True},
    {"edad": 38, "departamento": "Finanzas", "nivel_educativo": "universitario", "en_formacion": False}
]

# Separar positivos y negativos
positivos, negativos = [d for d in datos if d["en_formacion"]], [d for d in datos if not d["en_formacion"]]
P, N = len(positivos), len(negativos)

# FOIL Gain simplificada
def foil_gain(p, n, P, N):
    def safe_log(x): return math.log2(x) if x > 0 else 0
    return (p + n) * (safe_log(p / (p + n)) - safe_log(P / (P + N))) if p + n else 0

# Evaluación automática de reglas
print("Reglas FOIL inducidas y FOIL Gain:\n")
for attr in ["departamento", "nivel_educativo", "edad"]:
    for val in sorted({d[attr] for d in datos}):
        if attr == "edad":
            p, n = sum(d[attr] <= val and d["en_formacion"] for d in datos), sum(d[attr] <= val and not d["en_formacion"] for d in datos)
            cond = f"{attr} ≤ {val}"
        else:
            p, n = sum(d[attr] == val and d["en_formacion"] for d in datos), sum(d[attr] == val and not d["en_formacion"] for d in datos)
            cond = f"{attr} == '{val}'"
        print(f"Condición: {cond}\n p={p}, n={n}, FOIL Gain={foil_gain(p,n,P,N):.3f}\n")

# Regla simple final
def regla_simple():
    reglas = []
    for attr in ["departamento", "nivel_educativo", "edad"]:
        unicos = {d[attr] for d in positivos} - {d[attr] for d in negativos}
        if unicos: reglas.append(f"{attr} in {unicos}")
    return " OR ".join(reglas)

print("Regla inducida simple:", regla_simple())