import re

# Tu cadena original
cadena = "121PAPER HUMIT WC 1,55"

# Usamos una expresión regular para separar los números al principio
resultado = re.sub(r'^(\d+)', r'\1 ', cadena)

print(resultado)
