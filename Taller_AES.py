#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taller_AES.py

Script para cifrar y descifrar imágenes usando AES (CBC) y mostrar/guardar
la representación en Base64 del mensaje cifrado.

Características:
- Acepta cualquier archivo de imagen (lee bytes del archivo)
- Cifra con AES en modo CBC usando una clave de 128/192/256 bits
- Codifica el ciphertext en Base64 y lo muestra en consola
- Decodifica desde Base64, descifra y reconstruye la imagen original
- Si se ejecuta sin argumentos, genera una imagen de prueba y la procesa

Dependencias: pycryptodome, pillow
"""

import argparse
import base64
import os
import sys
from io import BytesIO
import math

try:
	from Crypto.Cipher import AES
	from Crypto.Random import get_random_bytes
except Exception as e:
	print("Falta la librería 'pycryptodome'. Instálela con: pip install pycryptodome")
	raise

try:
	from PIL import Image
except Exception:
	print("Falta la librería 'Pillow'. Instálela con: pip install pillow")
	raise


BLOCK_SIZE = 16


def pad(data: bytes) -> bytes:
	"""PKCS7 padding"""
	pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
	return data + bytes([pad_len]) * pad_len


def unpad(data: bytes) -> bytes:
	if not data:
		return data
	pad_len = data[-1]
	if pad_len < 1 or pad_len > BLOCK_SIZE:
		raise ValueError("Padding inválido")
	return data[:-pad_len]


def encrypt_bytes(plaintext: bytes, key: bytes) -> bytes:
	iv = get_random_bytes(BLOCK_SIZE)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(pad(plaintext))
	return iv + ciphertext


def decrypt_bytes(iv_and_ciphertext: bytes, key: bytes) -> bytes:
	iv = iv_and_ciphertext[:BLOCK_SIZE]
	ciphertext = iv_and_ciphertext[BLOCK_SIZE:]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintext_padded = cipher.decrypt(ciphertext)
	return unpad(plaintext_padded)


def process_image_file(path: str, key_bytes: bytes, do_show: bool = True) -> str:
	"""Cifra, codifica en base64, decodifica, descifra y guarda la imagen recuperada.

	Devuelve la ruta del archivo recuperado.
	"""
	basename = os.path.basename(path)
	with open(path, "rb") as f:
		img_bytes = f.read()

	# Cifrar
	iv_cipher = encrypt_bytes(img_bytes, key_bytes)

	# Generar una representación visual del ciphertext y guardarla como JPEG
	try:
		enc_bytes = iv_cipher
		enc_len = len(enc_bytes)
		# Elegimos un ancho fijo para la imagen visual (256) para evitar imágenes excesivamente estrechas
		enc_width = 256
		enc_height = (enc_len + enc_width - 1) // enc_width
		pad_len = enc_width * enc_height - enc_len
		enc_padded = enc_bytes + (b"\x00" * pad_len)
		enc_img = Image.frombytes('L', (enc_width, enc_height), enc_padded)
		encrypted_path = os.path.join(os.path.dirname(path), f"encrypted_{basename}.jpg")
		# Guardar como JPEG
		enc_img.save(encrypted_path, format='JPEG')
		print(f"Encrypted image (visual) guardada en: {encrypted_path}")
	except Exception as e:
		print(f"No se pudo generar la imagen cifrada visual: {e}")

	# Base64
	b64 = base64.b64encode(iv_cipher)
	b64_text = b64.decode('ascii')

	print("--- Texto Base64 (puede ser muy largo) ---")
	print(b64_text)
	print("--- Fin Base64 ---")

	# También guardamos el base64 en un archivo por si es necesario
	b64_out = path + ".b64.txt"
	with open(b64_out, "w", encoding="utf-8") as f:
		f.write(b64_text)

	# Decodificar Base64 a bytes
	decoded = base64.b64decode(b64_text)

	# Descifrar
	recovered = decrypt_bytes(decoded, key_bytes)

	# Guardar imagen recuperada
	recovered_path = os.path.join(os.path.dirname(path), f"recovered_{basename}")
	with open(recovered_path, "wb") as f:
		f.write(recovered)

	print(f"Imagen recuperada guardada en: {recovered_path}")

	if do_show:
		try:
			img = Image.open(BytesIO(recovered))
			img.show()
		except Exception as e:
			print(f"No se pudo mostrar la imagen automáticamente: {e}")

	return recovered_path


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Cifrar y descifrar imágenes usando AES y Base64")
	parser.add_argument("image", nargs="?", help="Ruta al archivo de imagen. Si se omite, se usa una imagen de prueba generada.")
	parser.add_argument("--keysize", choices=["128", "192", "256"], default="128", help="Tamaño de clave AES en bits (128/192/256). Default=128")
	parser.add_argument("--key", help="Clave en hexadecimal (opcional). Si no se pasa, el script genera una aleatoria y la muestra.")
	parser.add_argument("--no-show", action="store_true", help="No abrir la imagen recuperada automáticamente")
	return parser.parse_args()


def main():
	args = parse_args()
	keysize_bits = int(args.keysize)
	key_len = keysize_bits // 8

	if args.key:
		# interpretar la clave como hex
		key_bytes = bytes.fromhex(args.key)
		if len(key_bytes) != key_len:
			print(f"La clave proporcionada no tiene la longitud correcta ({key_len} bytes).")
			sys.exit(1)
	else:
		key_bytes = get_random_bytes(key_len)
		print(f"Clave generada (hex) para AES-{keysize_bits}: {key_bytes.hex()}" )

	# Si no se proporcionó imagen, crear una pequeña imagen de prueba
	if not args.image:
		print("No se proporcionó imagen. Generando una imagen de prueba (100x100).")
		img = Image.new("RGB", (100, 100), color=(73, 109, 137))
		for x in range(100):
			for y in range(100):
				if (x + y) % 10 == 0:
					img.putpixel((x, y), (255, 255, 0))
		temp_path = os.path.join(os.getcwd(), "test_image.png")
		img.save(temp_path, format="PNG")
		image_path = temp_path
	else:
		image_path = args.image

	process_image_file(image_path, key_bytes, do_show=(not args.no_show))


if __name__ == "__main__":
	main()

