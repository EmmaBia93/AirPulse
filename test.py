import bcrypt

# Contraseña en texto plano
password = "carpediem2110"

# Generar el hash
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Convertir el hash a una cadena legible para agregarlo al archivo .env
password_hash_str = password_hash.decode('utf-8')
print(password_hash_str)