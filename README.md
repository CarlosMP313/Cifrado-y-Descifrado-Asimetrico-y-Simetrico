# Cifrado y Descifrado Asimétrico y Simétrico

Este proyecto implementa un sistema de cifrado y descifrado que utiliza técnicas de cifrado asimétrico (RSA) y simétrico (cifrado por transposición). El sistema permite que un cliente (A) se comunique de manera segura con un servidor (B), cifrando un mensaje y enviando una clave de cifrado.

## Estructura del Proyecto

El proyecto está compuesto por dos archivos principales:

1. **Servidor (B)**:
   - Genera un par de claves RSA (pública y privada).
   - Escucha las conexiones entrantes de los clientes.
   - Recibe un mensaje cifrado y una clave de transposición cifrada, que descifra usando su clave privada.
   - Descifra el mensaje utilizando la clave de transposición.

2. **Cliente (A)**:
   - Se conecta al servidor y recibe la clave pública de B.
   - Cifra un mensaje usando el método de transposición.
   - Cifra la clave de transposición usando la clave pública de B.
   - Envía tanto el mensaje cifrado como la clave cifrada al servidor.

## Funcionamiento del Código

1. **Generación de Claves RSA**:
   - El servidor genera un par de claves (pública y privada) utilizando números primos aleatorios.

2. **Cifrado Simétrico por Transposición**:
   - El cliente cifra el mensaje utilizando un algoritmo de transposición que reordena las letras del mensaje según una clave.

3. **Cifrado de la Clave de Transposición**:
   - El cliente cifra la clave utilizada para el cifrado simétrico con la clave pública del servidor.

4. **Comunicación**:
   - El cliente envía el mensaje cifrado y la clave cifrada al servidor.
   - El servidor descifra la clave y luego el mensaje.

## Requisitos

- Python 3.x
- Bibliotecas estándar de Python

## Ejecución

1. **Ejecutar el Servidor**:
   ```bash
   python servidor.py
   ```
2. **Ejecutar el Cliente**:
   ```bash
   python cliente.py
   ```

   ## Ejemplo de Uso

- El servidor se inicia y genera sus claves RSA.
- El cliente se conecta al servidor y envía un mensaje cifrado junto con la clave de transposición cifrada.
- El servidor recibe y descifra ambos, mostrando el mensaje original.

## Notas

- Asegúrate de que el servidor esté en ejecución antes de iniciar el cliente.
- Puedes modificar el mensaje y la clave de transposición según tus necesidades.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, por favor envía un pull request o abre un issue para discutir los cambios que deseas realizar.

Asegúrate de sustituir `servidor.py` y `cliente.py` con los nombres reales de tus archivos si son diferentes.


   
