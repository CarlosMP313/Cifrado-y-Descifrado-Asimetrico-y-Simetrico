import socket
import random
import math

# Funciones RSA
def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generar_primos():
    primos = [n for n in range(1, 1000) if es_primo(n)]
    p, q = random.sample(primos, 2)
    return p, q

def calcular_phi(p, q):
    return (p - 1) * (q - 1)

def obtener_posibles_e(phi_n):
    posibles_e = []
    for e in range(3, phi_n, 2):
        if math.gcd(e, phi_n) == 1:
            posibles_e.append(e)
    posibles_e.append(65537)
    return posibles_e

def calcular_d(e, phi_n):
    d = pow(e, -1, phi_n)
    return d

# Cifrado por transposición
def cifrar_transposicion(mensaje, clave):
    num_columnas = len(clave)
    num_filas = (len(mensaje) + num_columnas - 1) // num_columnas
    columnas = [''] * num_columnas

    for i in range(len(mensaje)):
        columnas[i % num_columnas] += mensaje[i]

    orden_columnas = sorted(range(num_columnas), key=lambda k: clave[k])
    mensaje_cifrado = ''.join(columnas[i] for i in orden_columnas)

    return mensaje_cifrado

def descifrar_transposicion(mensaje_cifrado, clave):
    num_columnas = len(clave)
    num_filas = (len(mensaje_cifrado) + num_columnas - 1) // num_columnas
    
    longitud_columnas = [num_filas] * num_columnas
    for i in range(len(mensaje_cifrado) % num_columnas):
        longitud_columnas[i] -= 1

    columnas = [''] * num_columnas
    indice = 0

    for i in sorted(range(num_columnas), key=lambda k: clave[k]):
        columnas[i] = mensaje_cifrado[indice:indice + longitud_columnas[i]]
        indice += longitud_columnas[i]

    mensaje_descifrado = ''
    for fila in range(num_filas):
        for columna in range(num_columnas):
            if fila < len(columnas[columna]):
                mensaje_descifrado += columnas[columna][fila]

    return mensaje_descifrado

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 12345

# Generar las llaves RSA para B
p, q = generar_primos()
n_b = p * q
phi_n_b = calcular_phi(p, q)
posibles_e_b = obtener_posibles_e(phi_n_b)
e_b = random.choice(posibles_e_b)
d_b = calcular_d(e_b, phi_n_b)

print(f"Clave pública de B (n_b, e_b): ({n_b}, {e_b})")
print(f"Clave privada de B (n_b, d_b): ({n_b}, {d_b})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print("[Servidor] Esperando conexión...")

    conn, addr = server.accept()
    with conn:
        print(f"[Servidor] Conectado con: {addr}")

        # Enviar la clave pública de B a A
        conn.sendall(f"{n_b},{e_b}".encode())
        print(f"[Servidor] Clave pública enviada: ({n_b}, {e_b})")

        while True:
            # Recibir mensaje cifrado
            mensaje_cifrado = conn.recv(1024).decode()
            if not mensaje_cifrado:
                break  # Salir si no hay más mensajes

            # Recibir la clave cifrada
            clave_cifrada = int(conn.recv(1024).decode())
            print(f"[Servidor] Mensaje cifrado recibido: {mensaje_cifrado}")
            print(f"[Servidor] Clave cifrada recibida: {clave_cifrada}")

            # Descifrar la clave de transposición con la clave privada de B
            clave_descifrada = pow(clave_cifrada, d_b, n_b)
            print(f"[Servidor] Clave de transposición descifrada: {clave_descifrada}")

            # Descifrar el mensaje con la clave de transposición
            mensaje_descifrado = descifrar_transposicion(mensaje_cifrado, str(clave_descifrada))
            print(f"[Servidor] Mensaje descifrado: {mensaje_descifrado}")
