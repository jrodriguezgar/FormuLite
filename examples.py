# Para desarrollar más funcionalidades, puedes:

# Añadir más funciones matemáticas como:

# COUNT_IF() para contar elementos que cumplen una condición
# PRODUCT() para multiplicar números
# POWER() para potencias
# Añadir más funciones de texto como:

# TRIM() para eliminar espacios en blanco
# PROPER() para capitalizar palabras
# REPLACE() para reemplazar texto
# Añadir más funciones de búsqueda como:

# MATCH() para encontrar la posición de un valor
# INDEX() para obtener valores por índice


# Ejemplos de funciones matemáticas
numbers = [1, 2, 3, 4, 5]
sum_greater_than_3 = pending_math.sum_if(numbers, ">3")  # Resultado: 9 (4 + 5)
promedio = pending_math.average(numbers)  # Resultado: 3.0

# Ejemplos de funciones de texto
texto = pending_text.concat("Hola", " ", "Mundo")  # Resultado: "Hola Mundo"
primeras_letras = pending_text.left("Python", 2)  # Resultado: "Py"
ultimas_letras = pending_text.right("Python", 2)  # Resultado: "on"

# Ejemplos de funciones de búsqueda
tabla = [
    ["Nombre", "Edad", "Ciudad"],
    ["Ana", 25, "Madrid"],
    ["Juan", 30, "Barcelona"]
]
edad_ana = pending_lookup.vlookup("Ana", tabla, 2)  # Resultado: 25
ciudad_juan = pending_lookup.vlookup("Juan", tabla, 3)  # Resultado: "Barcelona"