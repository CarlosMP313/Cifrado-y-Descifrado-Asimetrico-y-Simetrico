import socket
from tkinter import Tk, Label, Entry, Button, Text, END
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

# Configuración del cliente
SERVER_IP = '127.0.0.1'  # Cambia por la IP del servidor
PORT = 12345

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente - Enviar Mensajes")

        # Interfaz gráfica
        Label(master, text="Mensaje:").pack()
        self.message_entry = Entry(master, width=50)
        self.message_entry.pack()

        self.send_button = Button(master, text="Enviar", command=self.send_message)
        self.send_button.pack()

        self.log = Text(master, height=15, width=80)
        self.log.pack()

        # Conectar al servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_IP, PORT))
        self.log.insert(END, "[Cliente] Conectado al servidor.\n")

        # Recibir la clave pública de B
        public_key = self.client.recv(1024).decode()
        n_b, e_b = map(int, public_key.split(','))
        self.log.insert(END, f"[Cliente] Clave pública recibida: (n_b={n_b}, e_b={e_b})\n")

        self.e_b = e_b
        self.n_b = n_b

    def send_message(self):
        mensaje = self.message_entry.get()
        if not mensaje:
            return  # No enviar mensajes vacíos

        # Cifrar el mensaje usando cifrado simétrico por transposición
        clave_transposicion = "31452"  # Clave de transposición
        mensaje_cifrado = cifrar_transposicion(mensaje, clave_transposicion)

        # Cifrar la clave de transposición usando la clave pública de B
        clave_cifrada = pow(int(clave_transposicion), self.e_b, self.n_b)

        # Enviar el mensaje cifrado y la clave cifrada a B
        self.client.sendall(mensaje_cifrado.encode())
        self.client.sendall(str(clave_cifrada).encode())

        print(f"[Cliente] Mensaje cifrado: {mensaje_cifrado}")
        print(f"[Cliente] Clave de transposición cifrada: {clave_cifrada}")
        self.log.insert(END, "[Cliente] Mensaje y clave cifrados enviados.\n")

        # Limpiar el campo de entrada
        self.message_entry.delete(0, END)

# Iniciar la interfaz gráfica
root = Tk()
app = ClientApp(root)
root.mainloop()
