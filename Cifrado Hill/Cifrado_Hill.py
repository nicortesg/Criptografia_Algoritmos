print("Cifrado de Hill\nEscriba 1 para cifrar o 2 para decifrar: ")

def calculo_inversa(matriz):
    det = (matriz[0]*matriz[3]) - (matriz[1]*matriz[2])
    if det == 0:
        return None
    inv_det = 1/(det % 26)
    return [matriz[3] * inv_det % 26, -matriz[1] * inv_det % 26,
            -matriz[2] * inv_det % 26, matriz[0] * inv_det % 26]

mode = "0"
matriz = ["a","b","c","d"]
boolean = False
inversa = []
texto = ""
texto_cifrado = ""


while mode not in ("1","2"):
    mode = input(">> ")
    if mode not in ("1","2"):
        print("Entrada invalida, intente de nuevo")

while boolean == False:
    boolean = True
    print("Ejemplo de clave (Matriz 2x2):\n|a b|\n|c d|\n" \
    "Porfavor ingrese los los elementos de la clave en orden: a,b,c,d")
    for i in matriz:
        temp = input(">> ")
        if temp.isdigit() == False:
            boolean = False
            print("Entrada invalida, intente de nuevo")
            break
        else:
            matriz[matriz.index(i)] = int(temp)
    if boolean == True:
        inversa = calculo_inversa(matriz)
        if inversa == None:
            print("La matriz no es invertible, intente con otra clave")
            boolean = False

if mode == "1":
    while not texto.upper():
        print("Ingrese el texto a cifrar en mayusculas (sin espacios ni caracteres especiales): ")
        texto = input(">> ")
        if not texto.upper():
            print("Entrada invalida, intente de nuevo")
            continue
        else:
            if len(texto) % 2 != 0:
                texto += "X"
            for i in range(0, len(texto), 2):
                a = ord(texto[i]) - 65
                b = ord(texto[i + 1]) - 65
                c = (matriz[0] * a + matriz[2] * b) % 26
                d = (matriz[1] * a + matriz[3] * b) % 26
                texto_cifrado += chr(c + 65) + chr(d + 65)
            print("Texto cifrado:", texto_cifrado)

if mode == "2":
    while not texto.upper():
        print("Ingrese el texto a decifrar en mayusculas (sin espacios ni caracteres especiales): ")
        texto = input(">> ")
        if not texto.upper():
            print("Entrada invalida, intente de nuevo")
            continue
        else:
            if len(texto) % 2 != 0:
                texto += "X"
            for i in range(0, len(texto), 2):
                a = ord(texto[i]) - 65
                b = ord(texto[i + 1]) - 65
                c = (inversa[0] * a + inversa[2] * b) % 26
                d = (inversa[1] * a + inversa[3] * b) % 26
                texto_cifrado += chr(int(c) + 65) + chr(int(d) + 65)
            print("Texto decifrado:", texto_cifrado)

end=input("Presione una tecla para salir")







    
    

