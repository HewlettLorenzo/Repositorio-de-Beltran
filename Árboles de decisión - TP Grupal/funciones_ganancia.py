from funciones_entropia import calcular_entropia

# Calcula la ganancia de información para un atributo:
# divisiones: lista de tuplas [(positivos, negativos), ...]
def ganancia_informacion(total_p, total_n, divisiones):
    entropia_total = calcular_entropia(total_p, total_n)
    total = total_p + total_n
    entropia_ponderada = 0

    for (p, n) in divisiones:
        peso = (p + n) / total
        entropia_ponderada += peso * calcular_entropia(p, n)

    return entropia_total - entropia_ponderada
