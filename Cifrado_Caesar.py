x=0
mensaje="a"
clave=0

def dividir_en_bloques(texto, tamaño_bloque=5):
    """Divide el texto en bloques de tamaño especificado (por defecto 5)"""
    bloques = []
    for i in range(0, len(texto), tamaño_bloque):
        bloques.append(texto[i:i+tamaño_bloque])
    return ' '.join(bloques)

def cifrar_cesar(mensaje, clave):
    mensaje_cifrado = ""
    for char in mensaje:
        if char.isalpha():
            desplazamiento = (ord(char) - ord('A') + clave) % 26
            mensaje_cifrado += chr(desplazamiento + ord('A'))
        else:
            mensaje_cifrado += char
    # Dividir en bloques de 5 letras
    return dividir_en_bloques(mensaje_cifrado)

def descifrar_cesar(mensaje, clave):
    # Eliminar espacios del mensaje cifrado
    mensaje = mensaje.replace(" ", "")
    mensaje_descifrado = ""
    for char in mensaje:
        if char.isalpha():
            desplazamiento = (ord(char) - ord('A') - clave) % 26
            mensaje_descifrado += chr(desplazamiento + ord('A'))
        else:
            mensaje_descifrado += char
    return mensaje_descifrado

while x!=1 and x!=2:
    try:
        x = int(input("Ingrese la opción que desea\n1. Cifrar\n2. Descifrar\n>>"))
    except ValueError:
        print("Opción inválida. Por favor, ingrese 1 o 2.")

while clave<=0 or any(not c.isdigit() for c in str(clave)):
    try:
        clave = int(input("Ingrese la clave de descifrado: "))
    except ValueError:
        print("Clave inválida. Por favor, ingrese un número entero positivo.")

if x==1:
    while any(not c.isupper() for c in mensaje):
        mensaje = input("Ingrese el mensaje a cifrar en mayusculas y sin espacios: ")
    mensaje_cifrado = cifrar_cesar(mensaje, clave)
    print("Mensaje cifrado:", mensaje_cifrado)

elif x==2:
    while any(not c.isupper() and c!=" " for c in mensaje):
        mensaje = input("Ingrese el mensaje a descifrar en mayusculas (puede incluir espacios): ")
    mensaje_descifrado = descifrar_cesar(mensaje, clave)
    print("Mensaje descifrado:", mensaje_descifrado)

y= input("Presione cualquier tecla para salir...")


