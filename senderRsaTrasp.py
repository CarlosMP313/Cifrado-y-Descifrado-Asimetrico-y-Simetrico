import socket
import math
from tkinter import Tk, Label, Entry, Button, Text, END

# --- Función de cifrado por transposición ---
def cifrar_rc(texto, columnas):
    matriz = [''] * columnas
    for i, char in enumerate(texto):
        matriz[i % columnas] += char
    return ''.join(matriz)

# --- Configuración del cliente ---
SERVER_IP = '127.0.0.1'  # Cambia por la IP del servidor si es necesario
PORT = 12345

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente - Enviar Mensajes")

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

        # Recibir la clave pública del servidor
        public_key = self.client.recv(1024).decode()
        self.n_b, self.e_b = map(int, public_key.split(','))
        self.log.insert(END, f"[Cliente] Clave pública recibida: (n_b={self.n_b}, e_b={self.e_b})\n")

    def send_message(self):
        mensaje = self.message_entry.get()
        if not mensaje:
            return  # No enviar mensajes vacíos

        # Definir el número de columnas como clave de transposición
        columnas = math.ceil(math.sqrt(len(mensaje)))

        print(f"[Cliente] Mensaje original: {mensaje}")
        print(f"[Cliente] Clave de transposición (columnas): {columnas}")

        # Cifrar el mensaje usando transposición r-c
        mensaje_cifrado = cifrar_rc(mensaje, columnas)
        print(f"[Cliente] Mensaje cifrado: {mensaje_cifrado}")

        # Cifrar la clave (cantidad de columnas) con RSA
        clave_cifrada = pow(columnas, self.e_b, self.n_b)
        print(f"[Cliente] Clave de transposición cifrada: {clave_cifrada}")

        # Enviar el mensaje y la clave cifrada al servidor
        self.client.sendall(mensaje_cifrado.encode())
        self.client.sendall(str(clave_cifrada).encode())

        self.log.insert(END, "[Cliente] Mensaje y clave cifrados enviados.\n")
        self.message_entry.delete(0, END)

# Iniciar la interfaz gráfica
root = Tk()
app = ClientApp(root)
root.mainloop()
