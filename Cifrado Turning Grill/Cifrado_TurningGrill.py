#!/usr/bin/env python3
"""
Turning Grille - CLI interactivo.

Parámetros (se piden por consola, en ese orden):
1) Tamaño N (entero) -> retícula NxN
2) Dirección de rotación -> 1 = sentido horario (clockwise), 0 = sentido antihorario (counterclockwise)
3) Modo -> 1 = cifrar, 0 = descifrar
4) Huecos -> lista de coordenadas (ej. "1,1 1,2 2,1 2,2"), se interpreta 1-based
5) Mensaje -> texto a (de)cifrar (para cifrar se mantiene sólo A-Z y se rellena con 'X' si hace falta;
   para descifrar ingresa el ciphertext cuyo tamaño debe ser múltiplo de N*N)

Ejemplo de uso al correr: seguirá pasos interactivos pidiendo cada dato.
"""

from typing import List, Tuple
import sys

def rotate_pos_clockwise(pos: Tuple[int,int], N: int) -> Tuple[int,int]:
    r, c = pos
    return (c, N - 1 - r)

def rotate_pos_counterclockwise(pos: Tuple[int,int], N: int) -> Tuple[int,int]:
    r, c = pos
    return (N - 1 - c, r)

def all_rotated_positions(initial_holes: List[Tuple[int,int]], N: int, rotation_dir: int) -> List[Tuple[int,int]]:
    rot = rotate_pos_clockwise if rotation_dir == 1 else rotate_pos_counterclockwise
    visited = []
    current = list(initial_holes)
    for _ in range(4):
        for p in current:
            visited.append(p)
        current = [rot(p, N) for p in current]
    return visited

def validate_grille(initial_holes: List[Tuple[int,int]], N: int, rotation_dir: int) -> Tuple[bool,str]:
    visited = all_rotated_positions(initial_holes, N, rotation_dir)
    if len(visited) != N*N:
        return False, f"Total visited positions through 4 rotations = {len(visited)} != {N*N}"
    if len(set(visited)) != N*N:
        s = set(visited)
        duplicates = [p for p in set(visited) if visited.count(p) > 1]
        all_cells = {(r,c) for r in range(N) for c in range(N)}
        missing = sorted(list(all_cells - s))
        msg = "Invalid grille: positions overlap across rotations."
        if duplicates:
            msg += f" Duplicates (examples): {duplicates[:10]}."
        if missing:
            msg += f" Missing cells (examples): {missing[:10]}."
        return False, msg
    return True, "OK"

def preprocess_plaintext(pt: str) -> str:
    return ''.join(ch for ch in pt.upper() if ch.isalpha())

def encrypt_turning_grille_single(N: int, rotation_dir: int, holes: List[Tuple[int,int]], plaintext_chunk: str, pad_char='X'):
    valid, msg = validate_grille(holes, N, rotation_dir)
    if not valid:
        raise ValueError("Grille invalid: " + msg)
    pt = preprocess_plaintext(plaintext_chunk)
    if len(pt) > N*N:
        raise ValueError(f"Plaintext chunk too long ({len(pt)}) for grid {N}x{N} (capacity {N*N}).")
    if len(pt) < N*N:
        pt = pt + pad_char * (N*N - len(pt))
    mat = [['' for _ in range(N)] for _ in range(N)]
    rot = rotate_pos_clockwise if rotation_dir == 1 else rotate_pos_counterclockwise
    current_holes = list(holes)
    idx = 0
    for rotation in range(4):
        sorted_holes = sorted(current_holes, key=lambda x: (x[0], x[1]))
        for (r,c) in sorted_holes:
            mat[r][c] = pt[idx]
            idx += 1
        current_holes = [rot(p, N) for p in current_holes]
    cipher_block = ''.join(mat[r][c] for r in range(N) for c in range(N))
    return cipher_block, mat

def decrypt_turning_grille_single(N: int, rotation_dir: int, holes: List[Tuple[int,int]], ciphertext_block: str):
    valid, msg = validate_grille(holes, N, rotation_dir)
    if not valid:
        raise ValueError("Grille invalid: " + msg)
    if len(ciphertext_block) != N*N:
        raise ValueError("Ciphertext length mismatch for block: expected " + str(N*N))
    mat = [['' for _ in range(N)] for _ in range(N)]
    it = iter(ciphertext_block)
    for r in range(N):
        for c in range(N):
            mat[r][c] = next(it)
    rot = rotate_pos_clockwise if rotation_dir == 1 else rotate_pos_counterclockwise
    current_holes = list(holes)
    out = []
    for rotation in range(4):
        sorted_holes = sorted(current_holes, key=lambda x: (x[0], x[1]))
        for (r,c) in sorted_holes:
            out.append(mat[r][c])
        current_holes = [rot(p, N) for p in current_holes]
    recovered = ''.join(out)
    return recovered, mat

def encrypt_turning_grille(N, rotation_dir, holes, plaintext, pad_char='X'):
    pt = preprocess_plaintext(plaintext)
    blocks = [pt[i:i+N*N] for i in range(0, len(pt), N*N)]
    ciphertext_blocks = []
    mats = []
    for b in blocks:
        cb, mat = encrypt_turning_grille_single(N, rotation_dir, holes, b, pad_char=pad_char)
        ciphertext_blocks.append(cb)
        mats.append(mat)
    return ''.join(ciphertext_blocks), ciphertext_blocks, mats

def decrypt_turning_grille(N, rotation_dir, holes, ciphertext):
    ct = ''.join(ciphertext.split())
    if len(ct) % (N*N) != 0:
        raise ValueError("Ciphertext total length must be multiple of N*N")
    blocks = [ct[i:i+N*N] for i in range(0, len(ct), N*N)]
    recovered_blocks = []
    mats = []
    for b in blocks:
        rec, mat = decrypt_turning_grille_single(N, rotation_dir, holes, b)
        recovered_blocks.append(rec)
        mats.append(mat)
    return ''.join(recovered_blocks), recovered_blocks, mats

def parse_holes_input(s: str, N: int, one_based=True):
    tokens = [t.strip() for t in s.replace(';',' ').split() if t.strip()]
    holes = []
    for tok in tokens:
        if ',' in tok:
            a,b = tok.split(',')
        elif '.' in tok:
            a,b = tok.split('.')
        else:
            raise ValueError("Invalid token for hole coordinates: " + tok)
        r = int(a); c = int(b)
        if one_based:
            r -= 1; c -= 1
        if not (0 <= r < N and 0 <= c < N):
            raise ValueError(f"Hole coordinate out of range: {(r,c)} for grid {N}.")
        holes.append((r,c))
    return holes

def read_input_console():
    try:
        N = int(input("1) Tamaño N de la retícula (entero, por ejemplo 4 para 4x4): ").strip())
        if N <= 0:
            print("N debe ser positivo."); sys.exit(1)
        rotation_dir = int(input("2) Dirección de rotación (1=horario, 0=antihorario): ").strip())
        if rotation_dir not in (0,1):
            print("Dirección debe ser 0 o 1."); sys.exit(1)
        mode = int(input("3) Modo (1=cifrar, 0=descifrar): ").strip())
        if mode not in (0,1):
            print("Modo debe ser 0 o 1."); sys.exit(1)
        holes_raw = input("4) Huecos (lista de coordenadas 1-based, ejemplo '1,1 1,2 2,1 2,2'): ").strip()
        holes = parse_holes_input(holes_raw, N, one_based=True)
        message = input("5) Mensaje a (de)cifrar: ").rstrip('\n')
        return N, rotation_dir, mode, holes, message
    except Exception as e:
        print("Entrada inválida:", e)
        sys.exit(1)

def pretty_print_matrix(mat):
    for row in mat:
        print(' '.join(row))
    print()

def main():
    N, rotation_dir, mode, holes, message = read_input_console()
    valid, msg = validate_grille(holes, N, rotation_dir)
    if not valid:
        print("La grille no es válida:", msg)
        print("Corrige la distribución de huecos y vuelve a intentar.")
        return
    print("Grille validada OK.")
    if mode == 1:
        # encrypt (support multi-block)
        cipher, blocks, mats = encrypt_turning_grille(N, rotation_dir, holes, message)
        print("\nCiphertext (concatenado):", cipher)
        print("Ciphertext (por bloques de tamaño NxN):", ' '.join(blocks))
        for i, m in enumerate(mats):
            print(f"\nBloque {i+1} - matriz rellenada tras cifrar:")
            pretty_print_matrix(m)
    else:
        # decrypt
        try:
            recovered, blocks, mats = decrypt_turning_grille(N, rotation_dir, holes, message)
        except Exception as e:
            print("Error en descifrado:", e)
            return
        print("\nRecovered concatenado (sin espacios):", recovered)
        print("Recovered por bloques (cada bloque es lectura por rotaciones):", ' '.join(blocks))
        for i, m in enumerate(mats):
            print(f"\nBloque {i+1} - matriz (ciphertext cargado fila por fila):")
            pretty_print_matrix(m)

if __name__ == "__main__":
    main()
