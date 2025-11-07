# Taller_AES

Script en Python para cifrar y descifrar imágenes usando AES (CBC) y Base64.

Características principales:

- Cifra cualquier imagen (lee bytes del archivo) con AES en modo CBC.
- Soporta claves de 128, 192 y 256 bits.
- Codifica el ciphertext en Base64 y lo muestra en consola.
- Decodifica desde Base64 y reconstruye la imagen original.
- Si se ejecuta sin parámetros, genera una imagen de prueba y la procesa.

Requisitos
---------

Instalar las dependencias (recomendado crear un virtualenv):

```powershell
python -m pip install -r requirements.txt
```

Uso
---

1) Ejecutar con una imagen concreta:

```powershell
python .\Taller_AES.py C:\ruta\a\imagen.jpg --keysize 256
```

El script generará una clave aleatoria si no se indica `--key`. Para usar una
clave propia, pásala en hexadecimal con `--key <hex>`.

2) Ejecutar sin argumentos (genera y procesa una imagen de prueba):

```powershell
python .\Taller_AES.py
```

Salida
------

- El texto Base64 se imprime en consola y también se guarda en `imagen.ext.b64.txt`.
- La imagen recuperada se guarda como `recovered_<nombre>` en el mismo directorio.

Notas
-----

- En Windows PowerShell puede que la visualización automática (Image.show()) abra el visor por defecto.
- Si el Base64 es muy largo, ten cuidado al copiar/pegar en consolas con límites.
