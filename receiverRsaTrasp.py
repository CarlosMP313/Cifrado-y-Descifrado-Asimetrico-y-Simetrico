import socket
import random
import math

# --- Funciones RSA ---
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
    return [e for e in range(3, phi_n, 2) if math.gcd(e, phi_n) == 1] + [65537]

def calcular_d(e, phi_n):
    return pow(e, -1, phi_n)

# --- Funciones de cifrado/descifrado por transposición ---
def descifrar_cr(texto, columnas):
    filas = math.ceil(len(texto) / columnas)
    vacíos = (columnas * filas) - len(texto)
    matriz = [''] * filas

    index = 0
    for col in range(columnas):
        for fila in range(filas):
            if fila == filas - 1 and col >= columnas - vacíos:
                continue
            matriz[fila] += texto[index]
            index += 1

    return ''.join(matriz)

# --- Configuración del servidor ---
HOST = '0.0.0.0'
PORT = 12345

# Generar llaves RSA
p, q = generar_primos()
n_b = p * q
phi_n_b = calcular_phi(p, q)
e_b = random.choice(obtener_posibles_e(phi_n_b))
d_b = calcular_d(e_b, phi_n_b)

print(f"Clave pública: (n_b={n_b}, e_b={e_b})")
print(f"Clave privada: (n_b={n_b}, d_b={d_b})")

# Iniciar el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print("[Servidor] Esperando conexión...")

    conn, addr = server.accept()
    with conn:
        print(f"[Servidor] Conectado con: {addr}")

        # Enviar la clave pública a A
        conn.sendall(f"{n_b},{e_b}".encode())
        print(f"[Servidor] Clave pública enviada: (n_b={n_b}, e_b={e_b})")

        while True:
            mensaje_cifrado = conn.recv(1024).decode()
            clave_cifrada = int(conn.recv(1024).decode())

            print(f"[Servidor] Mensaje cifrado recibido: {mensaje_cifrado}")
            print(f"[Servidor] Clave de transposición cifrada recibida: {clave_cifrada}")

            # Descifrar la clave de transposición
            columnas = pow(clave_cifrada, d_b, n_b)
            print(f"[Servidor] Clave de columnas descifrada: {columnas}")

            # Usar la clave para descifrar el mensaje
            mensaje_descifrado = descifrar_cr(mensaje_cifrado, columnas)
            print(f"[Servidor] Mensaje descifrado: {mensaje_descifrado}")

