#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taller_DES.py

Script para convertir una imagen en una representación de bits, cifrarla con DES,
codificar el ciphertext en Base64, mostrarlo, decodificar, descifrar y reconstruir
la imagen original.

Características:
- Lee cualquier archivo de imagen (bytes)
- Convierte los bytes del archivo a una representación de bits (string o lista)
- Cifra con DES (CBC) usando una clave de 8 bytes (64 bits, 56 bits efectivos)
- Codifica el ciphertext (IV + ciphertext) en Base64 y lo imprime
- Decodifica desde Base64, descifra y guarda la imagen recuperada

Dependencias: pycryptodome, pillow
"""

import argparse
import base64
import os
import sys
from io import BytesIO

try:
    from Crypto.Cipher import DES
    from Crypto.Random import get_random_bytes
except Exception:
    print("Falta la librería 'pycryptodome'. Instálela con: pip install pycryptodome")
    raise

try:
    from PIL import Image
except Exception:
    print("Falta la librería 'Pillow'. Instálela con: pip install pillow")
    raise


BLOCK_SIZE = 8  # DES block size


def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len


def unpad(data: bytes) -> bytes:
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Padding inválido")
    return data[:-pad_len]


def bytes_to_bitstring(data: bytes) -> str:
    """Convierte bytes a una cadena de bits '010101...'"""
    return ''.join(f'{b:08b}' for b in data)


def bitstring_to_bytes(bits: str) -> bytes:
    """Convierte una cadena de bits (longitud múltiplo de 8) a bytes."""
    # rellenar con ceros si no es múltiplo de 8
    extra = (-len(bits)) % 8
    if extra:
        bits = bits + ('0' * extra)
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


def encrypt_des(plaintext: bytes, key: bytes) -> bytes:
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext))
    return iv + ct


def decrypt_des(iv_and_ct: bytes, key: bytes) -> bytes:
    iv = iv_and_ct[:BLOCK_SIZE]
    ct = iv_and_ct[BLOCK_SIZE:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    return unpad(pt_padded)


def process_image(path: str, key: bytes, do_show: bool = True) -> str:
    basename = os.path.basename(path)
    with open(path, 'rb') as f:
        data = f.read()

    # Convertir a representación de bits (string)
    bits = bytes_to_bitstring(data)
    print(f"Longitud original (bytes): {len(data)}")
    print(f"Longitud en bits: {len(bits)}")
    print(f"Primeros 128 bits (muestra): {bits[:128]}")

    # (Opcional) convertir la representación de bits de vuelta a bytes para encriptar.
    # Esto preserva la información original y demuestra la conversión solicitada.
    data_for_encrypt = bitstring_to_bytes(bits)

    # Cifrar con DES
    iv_ct = encrypt_des(data_for_encrypt, key)

    # Codificar en Base64
    b64 = base64.b64encode(iv_ct).decode('ascii')
    print('\n--- Texto Base64 (ciphertext) ---')
    print(b64)
    print('--- Fin Base64 ---\n')

    # Guardar Base64 en archivo
    with open(path + '.b64.txt', 'w', encoding='utf-8') as f:
        f.write(b64)

    # Decodificar Base64
    decoded = base64.b64decode(b64)

    # Descifrar
    recovered = decrypt_des(decoded, key)

    # Guardar la imagen recuperada
    recovered_path = os.path.join(os.path.dirname(path), f'recovered_{basename}')
    with open(recovered_path, 'wb') as f:
        f.write(recovered)

    print(f"Imagen recuperada guardada en: {recovered_path}")

    if do_show:
        try:
            img = Image.open(BytesIO(recovered))
            img.show()
        except Exception as e:
            print(f"No se pudo mostrar la imagen automáticamente: {e}")

    return recovered_path


def parse_args():
    parser = argparse.ArgumentParser(description='Cifrar/descifrar imágenes usando DES (ejercicio)')
    parser.add_argument('image', nargs='?', help='Ruta a la imagen. Si se omite se genera una imagen de prueba.')
    parser.add_argument('--key', help='Clave DES en hexadecimal (8 bytes / 16 hex chars). Si se omite se genera aleatoria.')
    parser.add_argument('--no-show', action='store_true', help='No abrir la imagen recuperada automáticamente')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.key:
        key = bytes.fromhex(args.key)
        if len(key) != 8:
            print('La clave DES debe ser de 8 bytes (16 hex).')
            sys.exit(1)
    else:
        key = get_random_bytes(8)
        print(f'Clave DES generada (hex): {key.hex()}')

    if not args.image:
        print('No se proporcionó imagen. Generando imagen de prueba (120x80).')
        img = Image.new('RGB', (120, 80), color=(100, 150, 200))
        for x in range(120):
            for y in range(80):
                if (x * y) % 17 == 0:
                    img.putpixel((x, y), (255, 255, 0))
        temp_path = os.path.join(os.getcwd(), 'test_des_image.jpg')
        img.save(temp_path, format='JPEG')
        image_path = temp_path
    else:
        image_path = args.image

    process_image(image_path, key, do_show=(not args.no_show))


if __name__ == '__main__':
    main()
