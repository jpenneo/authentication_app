import os

# Generar una clave secreta de 24 bytes
csrf_secret_key = os.urandom(24).hex()
print(csrf_secret_key)