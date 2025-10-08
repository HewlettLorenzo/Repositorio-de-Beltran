import math

# Calcular la entropía de un conjunto binario.
def calcular_entropia(positivos, negativos):
    if positivos == 0 or negativos == 0:
        return 0
    total = positivos + negativos
    p = positivos / total
    n = negativos / total
    return - (p * math.log2(p) + n * math.log2(n))
