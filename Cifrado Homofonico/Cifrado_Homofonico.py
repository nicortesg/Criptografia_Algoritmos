import random

class CifradoHomofonico:
    def __init__(self):
        # Layout fijo de símbolos (0-99) asignados a cada letra del alfabeto inglés
        # Cada letra tiene diferentes cantidades de símbolos basados en su frecuencia típica
        self.layout = {
            'A': [0, 1, 2, 3, 4, 5, 6, 7],           # 8 símbolos (frecuencia alta)
            'B': [8, 9],                              # 2 símbolos (frecuencia baja)
            'C': [10, 11, 12],                        # 3 símbolos (frecuencia media-alta)
            'D': [13, 14, 15, 16],                    # 4 símbolos (frecuencia media-alta)
            'E': [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], # 12 símbolos (frecuencia muy alta)
            'F': [29, 30],                            # 2 símbolos (frecuencia baja)
            'G': [31, 32],                            # 2 símbolos (frecuencia baja)
            'H': [33, 34, 35, 36, 37, 38],           # 6 símbolos (frecuencia media-alta)
            'I': [39, 40, 41, 42, 43, 44, 45],       # 7 símbolos (frecuencia alta)
            'J': [46],                                # 1 símbolo (frecuencia muy baja)
            'K': [47],                                # 1 símbolo (frecuencia muy baja)
            'L': [48, 49, 50, 51],                    # 4 símbolos (frecuencia media)
            'M': [52, 53],                            # 2 símbolos (frecuencia baja)
            'N': [54, 55, 56, 57, 58, 59],           # 6 símbolos (frecuencia media-alta)
            'O': [60, 61, 62, 63, 64, 65, 66, 67],   # 8 símbolos (frecuencia alta)
            'P': [68, 69],                            # 2 símbolos (frecuencia baja)
            'Q': [70],                                # 1 símbolo (frecuencia muy baja)
            'R': [71, 72, 73, 74, 75, 76],           # 6 símbolos (frecuencia media-alta)
            'S': [77, 78, 79, 80, 81, 82],           # 6 símbolos (frecuencia media-alta)
            'T': [83, 84, 85, 86, 87, 88, 89, 90],   # 8 símbolos (frecuencia muy alta)
            'U': [91, 92, 93],                        # 3 símbolos (frecuencia media)
            'V': [94],                                # 1 símbolo (frecuencia muy baja)
            'W': [95],                                # 1 símbolo (frecuencia muy baja)
            'X': [96],                                # 1 símbolo (frecuencia muy baja)
            'Y': [97, 98],                            # 2 símbolos (frecuencia baja)
            'Z': [99]                                 # 1 símbolo (frecuencia muy baja)
        }
        
        # Crear el diccionario inverso para descifrado
        self.reverse_layout = {}
        for letra, simbolos in self.layout.items():
            for simbolo in simbolos:
                self.reverse_layout[simbolo] = letra
    
    def cifrar(self, mensaje):
        """
        Cifra un mensaje usando el algoritmo homofónico
        """
        mensaje = mensaje.upper().replace(' ', '').replace('\n', '')
        mensaje_cifrado = []
        
        for letra in mensaje:
            if letra in self.layout:
                # Seleccionar aleatoriamente uno de los símbolos asignados a la letra
                simbolos_disponibles = self.layout[letra]
                simbolo_elegido = random.choice(simbolos_disponibles)
                mensaje_cifrado.append(simbolo_elegido)
            else:
                # Si no es una letra del alfabeto inglés, mantener el carácter
                print(f"Advertencia: El carácter '{letra}' no está en el alfabeto inglés y será ignorado.")
        
        return mensaje_cifrado
    
    def descifrar(self, mensaje_cifrado):
        """
        Descifra un mensaje cifrado con el algoritmo homofónico
        """
        mensaje_descifrado = []
        
        for simbolo in mensaje_cifrado:
            if simbolo in self.reverse_layout:
                letra = self.reverse_layout[simbolo]
                mensaje_descifrado.append(letra)
            else:
                print(f"Advertencia: El símbolo '{simbolo}' no está en el layout de cifrado.")
        
        return ''.join(mensaje_descifrado)
    
    def mostrar_layout(self):
        """
        Muestra el layout de cifrado usado
        """
        print("\n=== LAYOUT DE CIFRADO HOMOFÓNICO ===")
        print("Letra -> Símbolos asignados")
        print("-" * 35)
        for letra in sorted(self.layout.keys()):
            simbolos = self.layout[letra]
            print(f"{letra:2} -> {simbolos}")
        print("-" * 35)
        print(f"Total de símbolos utilizados: {sum(len(simbolos) for simbolos in self.layout.values())}")
    
    def parsear_mensaje_cifrado(self, entrada):
        """
        Convierte una cadena de números separados por espacios o comas en una lista de enteros
        """
        try:
            # Remover caracteres no deseados y dividir por espacios o comas
            entrada = entrada.replace(',', ' ').replace('[', '').replace(']', '')
            numeros = [int(x) for x in entrada.split() if x.strip()]
            return numeros
        except ValueError:
            return None

def mostrar_menu():
    """
    Muestra el menú principal
    """
    print("\n" + "="*50)
    print("    CIFRADO HOMOFÓNICO (m=100, n=26)")
    print("="*50)
    print("1. Cifrar mensaje")
    print("2. Descifrar mensaje")
    print("3. Mostrar layout de cifrado")
    print("4. Salir")
    print("-" * 50)

def main():
    cipher = CifradoHomofonico()
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            print("\n--- CIFRAR MENSAJE ---")
            mensaje = input("Ingresa el mensaje a cifrar: ").strip()
            
            if not mensaje:
                print("Error: No se ingresó ningún mensaje.")
                continue
            
            mensaje_cifrado = cipher.cifrar(mensaje)
            print(f"\nMensaje original: {mensaje}")
            print(f"Mensaje cifrado: {mensaje_cifrado}")
            print(f"Cantidad de símbolos: {len(mensaje_cifrado)}")
            
        elif opcion == '2':
            print("\n--- DESCIFRAR MENSAJE ---")
            print("Ingresa los números del mensaje cifrado separados por espacios o comas:")
            print("Ejemplo: 17 34 52 8 21 o 17,34,52,8,21")
            entrada = input("Mensaje cifrado: ").strip()
            
            if not entrada:
                print("Error: No se ingresó ningún mensaje cifrado.")
                continue
            
            mensaje_cifrado = cipher.parsear_mensaje_cifrado(entrada)
            
            if mensaje_cifrado is None:
                print("Error: Formato inválido. Usa números separados por espacios o comas.")
                continue
            
            # Validar que todos los números estén en el rango válido (0-99)
            numeros_invalidos = [num for num in mensaje_cifrado if num < 0 or num > 99]
            if numeros_invalidos:
                print(f"Error: Los siguientes números están fuera del rango válido (0-99): {numeros_invalidos}")
                continue
            
            mensaje_descifrado = cipher.descifrar(mensaje_cifrado)
            print(f"\nMensaje cifrado: {mensaje_cifrado}")
            print(f"Mensaje descifrado: {mensaje_descifrado}")
            
        elif opcion == '3':
            cipher.mostrar_layout()
            
        elif opcion == '4':
            print("\n¡Gracias por usar el Cifrado Homofónico!")
            break
            
        else:
            print("\nError: Opción inválida. Por favor selecciona una opción del 1 al 4.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    print("Iniciando el programa de Cifrado Homofónico...")
    main()
