def encriptar_otp(mensaje, clave):
    mensaje_encriptado = ""
    for i in range(len(mensaje)):
        if mensaje[i] == clave[i]:
            mensaje_encriptado += '0'
        else:
            mensaje_encriptado += '1'
    return mensaje_encriptado

print("Programa de encriptación/desencriptación OTP (One-Time Pad)")
x=""
y="x"
while len(x)!=len(y) or len(x)<8 or len(x)%8!=0 or not all(c in '01' for c in x) or not all(c in '01' for c in y):
    x=input("Ingrese el mensaje a encriptar/desencriptar en binario: ")
    y=input("Ingrese la clave (de igual longitud) en binario: ")
    if len(x)!=len(y):
        print("Error: La clave debe tener la misma longitud que el mensaje.")
    elif len(x)<8:
        print("Error: La longitud debe ser mínimo 8 caracteres.")
    elif len(x)%8!=0:
        print("Error: La longitud debe ser múltiplo de 8.")
    elif not all(c in '01' for c in x):
        print("Error: El mensaje debe contener solo ceros y unos.")
    elif not all(c in '01' for c in y):
        print("Error: La clave debe contener solo ceros y unos.")

print("Mensaje encriptado/desencriptado:", encriptar_otp(x,y))
input("Presiona Enter para salir...")
