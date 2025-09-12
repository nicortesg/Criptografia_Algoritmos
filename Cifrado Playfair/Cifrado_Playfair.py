import re
print("Programa de cifrado y decifrado Playfair")

x=0
men=""
ver=0
llave=[]
fila=""

#funciones
# 1) Construir la cuadrícula (5x5) y los mapeos letra -> (fila,col) y (fila,col) -> letra
def build_grid_from_input(llave_rows):
    grid = []
    for row in llave_rows:
        row_norm = row.replace('J','I')  # I/J comparten casilla
        grid.append(list(row_norm))
    # build maps
    letter_to_pos = {}
    pos_to_letter = {}
    for r in range(5):
        for c in range(5):
            ch = grid[r][c]
            pos_to_letter[(r,c)] = ch
            letter_to_pos[ch] = (r,c)
    # aseguramos que 'J' apunte a la misma posición que 'I' (por si el usuario consulta 'J')
    if 'I' in letter_to_pos:
        letter_to_pos['J'] = letter_to_pos['I']
    return grid, letter_to_pos, pos_to_letter

# 2) reemplazar J->I
def preprocess_text(text):
    s = ''.join(ch for ch in text.upper() if ch.isalpha())
    s = s.replace('J', 'I')
    return s

# 3) Formar bigramas según regla Playfair (insertar X entre iguales, pad final con X si hace falta)
def make_bigrams(plain):
    i = 0
    pairs = []
    while i < len(plain):
        a = plain[i]
        if i+1 == len(plain):
            # último carácter suelto -> emparejar con 'X'
            pairs.append(a + 'X')
            i += 1
        else:
            b = plain[i+1]
            if a == b:
                # letras iguales: insertar filler 'X' entre ellas
                pairs.append(a + 'X')
                i += 1  # avanzamos sólo una posición
            else:
                pairs.append(a + b)
                i += 2
    return pairs

# 4) Función de cifrado/descifrado de un par
def process_pair(pair, letter_to_pos, pos_to_letter, encrypt=True):
    """
    pair: string 2 chars (ej. 'HE')
    encrypt: True->cifrar, False->descifrar
    """
    a, b = pair[0], pair[1]
    ra, ca = letter_to_pos[a]
    rb, cb = letter_to_pos[b]

    if ra == rb:
        # misma fila
        if encrypt:
            ca2 = (ca + 1) % 5
            cb2 = (cb + 1) % 5
        else:
            ca2 = (ca - 1) % 5
            cb2 = (cb - 1) % 5
        return pos_to_letter[(ra, ca2)] + pos_to_letter[(rb, cb2)]
    elif ca == cb:
        # misma columna
        if encrypt:
            ra2 = (ra + 1) % 5
            rb2 = (rb + 1) % 5
        else:
            ra2 = (ra - 1) % 5
            rb2 = (rb - 1) % 5
        return pos_to_letter[(ra2, ca)] + pos_to_letter[(rb2, cb)]
    else:
        # rectángulo: intercambiar columnas
        return pos_to_letter[(ra, cb)] + pos_to_letter[(rb, ca)]

# 5) Eliminar rellenos 'X' añadidos durante el proceso de pairing al descifrar
def remove_fillers_from_decrypted(s):
    if len(s) % 2 != 0:
        # si por alguna razón no es par, lo devolvemos tal cual
        return s

    pairs = [s[i:i+2] for i in range(0, len(s), 2)]
    out = []
    for i in range(len(pairs)):
        a, b = pairs[i][0], pairs[i][1]
        if b == 'X' and i+1 < len(pairs) and pairs[i+1][0] == a:
            # el X fue relleno entre letras iguales: añadir solo la primera letra
            out.append(a)
        else:
            out.append(a + b)
    out_s = ''.join(out)
    # si terminó con 'X' suposición de padding final -> quitarlo
    if out_s.endswith('X'):
        out_s = out_s[:-1]
    return out_s

# 6) Funciones principales que cifran o descifran un texto (string)
def playfair_encrypt(plaintext, letter_to_pos, pos_to_letter):
    s = preprocess_text(plaintext)
    pairs = make_bigrams(s)
    cipher_pairs = [process_pair(p, letter_to_pos, pos_to_letter, encrypt=True) for p in pairs]
    cipher_text = ''.join(cipher_pairs)
    return cipher_text, cipher_pairs

def playfair_decrypt(ciphertext, letter_to_pos, pos_to_letter):
    s = preprocess_text(ciphertext)  # eliminar espacios y J->I si viniera
    # asumimos que el ciphertext viene ya en pares correctos;
    # si la longitud es impar, lo rellenamos con 'X' para evitar errores
    if len(s) % 2 != 0:
        s = s + 'X'
    pairs = [s[i:i+2] for i in range(0, len(s), 2)]
    plain_pairs = [process_pair(p, letter_to_pos, pos_to_letter, encrypt=False) for p in pairs]
    plain_text = ''.join(plain_pairs)
    # intentar limpiar rellenos
    cleaned = remove_fillers_from_decrypted(plain_text)
    return plain_text, cleaned, plain_pairs

#ingreso de la opción Encriptación(1) o desencriptación(2)
while x != 1 and x != 2:
    x = int(input("Seleccione la opción que desea:\n1) Cifrar un mensaje\n2)Decifrar un mensaje\n"))
    if x != 1 and x != 2:
        print("Opcion invalida")

#ingreso del mensaje en men, solo se aceptan letras mayusculas
men = input("Ingrese el mensaje a cifrar en mayusculas: ")
while ver == 0:
    if any(not c.isupper() for c in men):
        men = input("Mensaje invalido, solo puede ingresar letras mayusculas. Intente de nuevo: ")
    else:
        ver=1

#Ingreso de la llave (matriz 5x5), se almacena cada fila como un elemento de la lista llave
print("Ingrese la llave (matriz 5x5) fila por fila (Solo letras mayusculas sin espacios)")
for i in range(5):
    while len(fila) != 5 or ver==1:
        fila=input(f"Ingrese la fila {i+1}: ")
        if len(fila) != 5:
            print("Cada fila debe tener 5 letras únicamente")
        if any(not c.isupper() for c in fila):
            ver=1
            print("Solo puedes ingresar letras mayusculas sin espacios")
        else:
            ver=0
            
    llave.append(fila)
    fila=""

grid, letter_to_pos, pos_to_letter = build_grid_from_input(llave)
print("\nCuadrícula Playfair (I/J combinadas como I):")
for r in range(5):
    print(' '.join(grid[r]))
print()

#Encriptación
if x == 1:
    cipher_text, cipher_pairs = playfair_encrypt(men, letter_to_pos, pos_to_letter)
    # imprimimos agrupado por pares para mayor claridad
    grouped = ' '.join(cipher_pairs)
    print("Texto plano (preprocesado):", preprocess_text(men))
    print("Bigramas (usados para cifrar):", ' '.join(make_bigrams(preprocess_text(men))))
    print("Texto cifrado (por pares):", grouped)
    print("Texto cifrado (continuo):", cipher_text)

#Desencriptación
elif x == 2:
    plain_raw, plain_cleaned, plain_pairs = playfair_decrypt(men, letter_to_pos, pos_to_letter)
    print("Texto cifrado (preprocesado):", preprocess_text(men))
    print("Bigramas (cifradas):", ' '.join([men[i:i+2] for i in range(0, len(preprocess_text(men)), 2)]))
    print("Descifrado (raw, sin limpiar):", plain_raw)
    print("Descifrado (limpio, sin rellenos):", plain_cleaned)

x=input("Presione cualquier tecla para finalizar")
