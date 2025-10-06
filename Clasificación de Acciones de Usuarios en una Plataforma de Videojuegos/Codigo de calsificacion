
# Clasificación de objetos tecnológicos con reglas simples

# Datos de ejemplo (tabla)
objetos = [
    {"Objeto": "Smartphone", "Portátil": True, "Conectividad": ["WiFi", "4G"], "Pantalla táctil": True},
    {"Objeto": "Laptop", "Portátil": True, "Conectividad": ["WiFi"], "Pantalla táctil": False},
    {"Objeto": "Smartwatch", "Portátil": True, "Conectividad": ["Bluetooth"], "Pantalla táctil": True},
    {"Objeto": "Impresora", "Portátil": False, "Conectividad": ["USB"], "Pantalla táctil": False},
    {"Objeto": "Tablet", "Portátil": True, "Conectividad": ["WiFi"], "Pantalla táctil": True},
    {"Objeto": "PC de escritorio", "Portátil": False, "Conectividad": ["Ethernet"], "Pantalla táctil": False}
]

# Nuevos ejemplos
nuevos = [
    {"Objeto": "Consola de juego", "Portátil": False, "Conectividad": ["WiFi y Ethernet"], "Pantalla táctil": False},
    {"Objeto": "e-reader", "Portátil": True, "Conectividad": ["Wifi"], "Pantalla táctil": True},
    {"Objeto": "Camara digital", "Portátil": True, "Conectividad": ["Usb"], "Pantalla táctil": False},
    {"Objeto": "Camara digital", "Portátil": False, "Conectividad": ["Usb"], "Pantalla táctil": True}
]


# Función de clasificación según reglas
def clasificar(objeto):
    if objeto["Portátil"] and objeto["Pantalla táctil"]:
        return "Dispositivo móvil"
    elif objeto["Portátil"] and not objeto["Pantalla táctil"]:
        return "Computadora"
    elif not objeto["Portátil"] and "Ethernet" in objeto["Conectividad"]:
        return "Computadora"
    elif not objeto["Portátil"] and not objeto["Pantalla táctil"]:
        return "Periférico"
    else:
        return "Desconocido"

# Clasificación de la tabla original
print("Clasificación de objetos de ejemplo:")
for obj in objetos:
    categoria = clasificar(obj)
    print(f"- {obj['Objeto']} → {categoria}")

# Clasificación de nuevos ejemplos
print("\nClasificación de nuevos ejemplos:")
for obj in nuevos:
    categoria = clasificar(obj)
    print(f"- {obj['Objeto']} → {categoria}")