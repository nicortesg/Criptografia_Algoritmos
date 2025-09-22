#!/usr/bin/env python3
"""
Ejemplos:
    python Cifrado_Vigenere.py enc miClave 26 "Hola, mundo!"
    python Cifrado_Vigenere.py dec miClave 26 "Twnl, mprpw!"

"""
import sys
import argparse
import string

ALPHABET = string.ascii_uppercase


def sanitize_key(key: str) -> str:
    """Devuelve sólo las letras de la clave, en mayúsculas."""
    return ''.join(ch for ch in key if ch.isalpha()).upper()


def char_index(ch: str, t: int) -> int:
    """Devuelve el índice 0..t-1 del carácter alfabético `ch`, usando A.. como base y aplicando módulo t."""
    return (ord(ch.upper()) - ord('A')) % t


def index_to_char(idx: int, is_upper: bool) -> str:
    """Convierte un índice 0..t-1 de vuelta a carácter respetando mayúscula/minúscula.
    Nota: la función asume que la gestión del `t` se hace fuera (es decir, 0->'A', 1->'B', ...).
    """
    base = ord('A') if is_upper else ord('a')
    return chr(base + idx)


def encrypt_vigenere(key: str, t: int, plaintext: str) -> str:
    if not key:
        raise ValueError('La clave no puede estar vacía (después de quitar caracteres no alfabéticos).')

    key_idx = [char_index(k, t) for k in key]
    out = []
    j = 0  # posición en la clave (sólo avanza sobre letras del texto)

    for ch in plaintext:
        if ch.isalpha():
            k = key_idx[j % len(key_idx)]
            p = char_index(ch, t)
            c = (p + k) % t
            # Mapear c (0..t-1) a letra A..Z o a..z
            # Si t < 26, permitimos que c < t pero aún mapeamos con A.. (puede superponerse)
            is_upper = ch.isupper()
            # index_to_char espera 0..25 base A..Z; si t < 26 y c may exceed 25? c < t <=26 so safe.
            out_ch = index_to_char(c, is_upper)
            out.append(out_ch)
            j += 1
        else:
            out.append(ch)
    return ''.join(out)


def decrypt_vigenere(key: str, t: int, ciphertext: str) -> str:
    if not key:
        raise ValueError('La clave no puede estar vacía (después de quitar caracteres no alfabéticos).')

    key_idx = [char_index(k, t) for k in key]
    out = []
    j = 0

    for ch in ciphertext:
        if ch.isalpha():
            k = key_idx[j % len(key_idx)]
            c = char_index(ch, t)
            p = (c - k) % t
            is_upper = ch.isupper()
            out_ch = index_to_char(p, is_upper)
            out.append(out_ch)
            j += 1
        else:
            out.append(ch)
    return ''.join(out)


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Cifrado/Descifrado Vigenère (línea de comandos)')
    parser.add_argument('mode', choices=['enc', 'dec'], help="'enc' para cifrar, 'dec' para descifrar")
    parser.add_argument('key', help='Clave alfabética (se ignorarán caracteres no alfabéticos)')
    parser.add_argument('t', type=int, help='Parámetro entero t (típicamente 26)')
    parser.add_argument('text', help='Texto a cifrar/descifrar (proteger con comillas si contiene espacios)')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    key = sanitize_key(args.key)
    t = args.t
    text = args.text

    if t <= 0 or t > 26:
        print('Error: t debe ser un entero entre 1 y 26 (inclusive).')
        sys.exit(1)

    if not key:
        print('Error: la clave debe contener al menos una letra (A-Z).')
        sys.exit(1)

    try:
        if args.mode == 'enc':
            result = encrypt_vigenere(key, t, text)
        else:
            result = decrypt_vigenere(key, t, text)
    except Exception as e:
        print('Error durante el proceso:', e)
        sys.exit(1)

    print(result)


if __name__ == '__main__':
    main()
