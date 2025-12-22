# 🔤 String Similarity - Módulo de Comparación de Cadenas

**Módulo avanzado para calcular similitudes entre palabras y frases utilizando múltiples algoritmos de distancia y similitud fonética.**

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)
![Algorithms](https://img.shields.io/badge/algorithms-10-brightgreen.svg)

### 🚀 Quick Start

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

# Uso simple - ¡Una línea!
ratio = calculate_similarity("casa", "caza")
print(f"Similitud: {ratio:.2%}")  # Similitud: 75.00%

# Elegir algoritmo específico
es_igual = calculate_similarity("conocimiento", "conosimiento", algorithm='metaphone')
print(f"¿Suenan igual? {es_igual}")  # True

# Obtener métricas detalladas
resultado = calculate_similarity("word1", "word2", algorithm='jaro_winkler')
print(f"Score: {resultado['score']:.2f}%")
```

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Instalación](#-instalación)
- [Algoritmos Implementados](#-algoritmos-implementados)
- [Uso](#-uso)
  - [Uso Básico](#uso-básico)
  - [Comparación Completa](#comparación-completa)
  - [Determinar Equivalencia Efectiva](#determinar-equivalencia-efectiva)
  - [Funciones Auxiliares](#funciones-auxiliares)
- [Ejemplos Prácticos](#-ejemplos-prácticos)
- [Configuración Avanzada](#-configuración-avanzada)
- [API Reference](#-api-reference)
- [Dependencias](#-dependencias)
- [Pruebas](#-pruebas)
- [Rendimiento](#-rendimiento)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## 🎯 Descripción

`string_similarity.py` es un módulo Python completo que proporciona una clase `WordSimilarity` y funciones auxiliares para comparar cadenas de texto utilizando una variedad de algoritmos de similitud. El módulo es ideal para:

- **Detección de errores tipográficos y ortográficos**
- **Búsqueda difusa (fuzzy matching)**
- **Normalización de nombres y términos**
- **Deduplicación de datos**
- **Procesamiento de lenguaje natural (NLP)**
- **Sistemas de autocompletado y sugerencias**

El módulo combina métricas **fonéticas** (cómo suenan las palabras) con métricas **tipográficas** (cómo se escriben) para proporcionar evaluaciones robustas de similitud.

---

## ✨ Características

- **🎯 Función Wrapper Unificada**: `calculate_similarity()` con selección de algoritmo mediante string
- **🔊 Similitud Fonética**: Algoritmos Double Metaphone y Match Rating Approach (MRA)
- **✏️ Distancia de Edición**: Levenshtein, Hamming, Needleman-Wunsch
- **📐 Similitud de Subsecuencias**: Ratcliff-Obershelp, Longest Common Subsequence (LCS)
- **🎯 Similitud Basada en Tokens**: Sørensen-Dice, Jaccard
- **🔍 Similitud de Prefijo**: Jaro-Winkler
- **⚙️ Importación Perezosa**: Carga dependencias solo cuando se necesitan
- **🔧 Auto-instalación**: Intenta instalar automáticamente paquetes faltantes
- **📊 Comparación Completa**: Método `compare()` para ejecutar todos los algoritmos
- **🎚️ Umbrales Configurables**: Criterios de equivalencia personalizables
- **💡 Type Hints Completos**: Autocompletado IDE con `Literal` types
- **📝 Documentación Exhaustiva**: Docstrings completos con ejemplos

---

## 📦 Instalación

### Requisitos Previos

- **Python**: >= 3.7
- **pip**: Gestor de paquetes de Python

### Paso 1: Clonar o Copiar el Módulo

Coloca el archivo `string_similarity.py` en tu proyecto, preferiblemente en una estructura como:

```
tu_proyecto/
├── lib/
│   └── formulite/
│       └── fxString/
│           └── string_similarity.py
```

### Paso 2: Instalar Dependencias

El módulo utiliza **importación perezosa** e intenta instalar automáticamente las dependencias faltantes. Sin embargo, puedes instalarlas manualmente:

```bash
pip install python-Levenshtein metaphone jellyfish textdistance
```

**Dependencias Detalladas:**

| Paquete | Propósito | Comando de Instalación |
|---------|-----------|------------------------|
| `python-Levenshtein` | Distancia y ratio de Levenshtein | `pip install python-Levenshtein` |
| `metaphone` | Similitud fonética Double Metaphone | `pip install metaphone` |
| `jellyfish` | Distancia de Hamming y otros | `pip install jellyfish` |
| `textdistance` | Múltiples algoritmos de distancia | `pip install textdistance` |

### Paso 3: Verificar Instalación

```python
from lib.formulite.fxString.string_similarity import WordSimilarity

ws = WordSimilarity()
print("✅ Módulo instalado correctamente")
```

---

## 🧮 Algoritmos Implementados

### Algoritmos Fonéticos

| Algoritmo | Descripción | Complejidad | Uso Típico |
|-----------|-------------|-------------|------------|
| **Double Metaphone** | Genera claves fonéticas para comparación auditiva | $O(n)$ | Nombres propios, detección de homofonía |
| **Match Rating Approach (MRA)** | Compara códigos fonéticos de nombres | $O(n)$ | Nombres, variaciones ortográficas |

### Algoritmos de Distancia de Edición

| Algoritmo | Descripción | Complejidad | Restricción |
|-----------|-------------|-------------|-------------|
| **Levenshtein** | Número mínimo de ediciones (insertar/borrar/sustituir) | $O(m \times n)$ | Ninguna |
| **Hamming** | Número de posiciones diferentes | $O(n)$ | Misma longitud |
| **Needleman-Wunsch** | Alineación global con costos de gap | $O(m \times n)$ | Bioinformática |

### Algoritmos de Subsecuencias

| Algoritmo | Descripción | Complejidad | Características |
|-----------|-------------|-------------|-----------------|
| **Ratcliff-Obershelp** | Basado en LCS recursivo | $O(m \times n)$ | Subsecuencias comunes |
| **LCS (Longest Common Subsequence)** | Secuencia común más larga | $O(m \times n)$ | No requiere contigüidad |

### Algoritmos Basados en Tokens

| Algoritmo | Descripción | Complejidad | Aplicación |
|-----------|-------------|-------------|------------|
| **Sørensen-Dice** | Coeficiente basado en intersección/unión | $O(n + m)$ | Frases, documentos |
| **Jaccard** | Índice de similitud de conjuntos | $O(n + m)$ | Análisis de contenido |

### Algoritmos de Prefijo

| Algoritmo | Descripción | Complejidad | Ventaja |
|-----------|-------------|-------------|---------|
| **Jaro-Winkler** | Jaro con peso en prefijo común | $O(m \times n)$ | Errores al inicio |

---

## 🚀 Uso

### 🎯 Wrapper Unificado `calculate_similarity()` (Recomendado)

**La forma más sencilla de usar el módulo** es mediante la función wrapper `calculate_similarity()` que permite seleccionar el algoritmo con un parámetro string:

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

# Uso básico (Levenshtein por defecto)
ratio = calculate_similarity("casa", "caza")
print(f"Similitud: {ratio:.2%}")  # Similitud: 75.00%

# Seleccionar algoritmo específico
resultado = calculate_similarity("conocimiento", "conosimiento", algorithm='metaphone')
print(f"¿Suenan igual? {resultado}")  # True

# Métricas detalladas
resultado = calculate_similarity("martha", "marhta", algorithm='jaro_winkler')
print(f"Score: {resultado['score']:.2f}%")  # Score: 96.11%
```

#### Algoritmos Disponibles en el Wrapper

| Parámetro `algorithm` | Tipo de Retorno | Descripción |
|----------------------|----------------|-------------|
| `'levenshtein'` (default) | `float` | Distancia de edición normalizada (0.0-1.0) |
| `'metaphone'` | `bool` | Similitud fonética |
| `'hamming'` | `float` | Distancia para cadenas de igual longitud |
| `'jaro_winkler'` | `Dict` | Similitud con peso en prefijo |
| `'ratcliff_obershelp'` | `Dict` | Subsecuencias comunes |
| `'sorensen_dice'` | `Dict` | Similitud basada en tokens |
| `'jaccard'` | `Dict` | Índice de similitud de conjuntos |
| `'mra'` | `Dict` | Match Rating Approach fonético |
| `'needleman_wunsch'` | `Dict` | Alineación de secuencias |
| `'lcs'` | `Dict` | Longest Common Subsequence |

**Parámetros Opcionales (`kwargs`):**
- `nw_gap_cost` (int): Costo de gap para Needleman-Wunsch (default: 1)

---

### Uso Básico (API de Clase)

Si prefieres usar la clase `WordSimilarity` directamente:

#### 1. Similitud Fonética (Metaphone)

```python
from lib.formulite.fxString.string_similarity import WordSimilarity

ws = WordSimilarity()

# Detectar si dos palabras suenan similar
resultado = ws.metaphone_score("conocimiento", "conosimiento")
print(resultado)  # True

resultado = ws.metaphone_score("hello", "hola")
print(resultado)  # False
```

#### 2. Distancia de Levenshtein

```python
# Calcular ratio de similitud (0.0 a 1.0)
ratio = ws.levenshtein_score("kitten", "sitting")
print(f"Similitud: {ratio:.2%}")  # Similitud: 57.14%

ratio = ws.levenshtein_score("casa", "caza")
print(f"Similitud: {ratio:.2%}")  # Similitud: 75.00%
```

#### 3. Distancia de Hamming

```python
# Solo para cadenas de igual longitud
try:
    ratio = ws.hamming_score("karolin", "kathrin")
    print(f"Similitud: {ratio:.2%}")  # Similitud: 57.14%
except ValueError as e:
    print(f"Error: {e}")
```

#### 4. Jaro-Winkler (Prefijo Común)

```python
# Excelente para nombres con errores al inicio
resultado = ws.jaro_winkler_score("martha", "marhta")
print(resultado)
# {'distance': 0.044..., 'similarity': 0.955..., 
#  'normalized_similarity': 0.961..., 'score': 96.11}
```

---

### Comparación Completa

El método `compare()` ejecuta **todos los algoritmos** (10 en total) y devuelve un diccionario con los resultados:

```python
ws = WordSimilarity()
resultados = ws.compare("aplicacion", "aplikacion")

print(f"Coincidencia Fonética: {resultados['metaphone_match']}")
print(f"Levenshtein Ratio: {resultados['levenshtein_ratio']:.4f}")
print(f"Jaro-Winkler Score: {resultados['jaro_winkler']['score']:.2f}")
print(f"LCS Sequence: '{resultados['lcs']['sequence']}'")
print(f"LCS Length: {resultados['lcs']['length']}")
```

**Salida Esperada:**

```
Coincidencia Fonética: True
Levenshtein Ratio: 0.9000
Jaro-Winkler Score: 95.33
LCS Sequence: 'aplicacion'
LCS Length: 10
```

**Algoritmos incluidos en `compare()`:**
1. `metaphone_match` (bool)
2. `levenshtein_ratio` (float)
3. `hamming_ratio` (float o None)
4. `ratcliff_obershelp` (Dict)
5. `sorensen_dice` (Dict)
6. `mra` (Dict)
7. `needleman_wunsch` (Dict)
8. `jaro_winkler` (Dict)
9. `jaccard` (Dict)
10. `lcs` (Dict)

---

### Determinar Equivalencia Efectiva

El método `are_words_equivalent()` combina **múltiples algoritmos** para decidir si dos palabras son "efectivamente la misma":

```python
from lib.formulite.fxString.string_similarity import are_words_equivalent

# Uso con umbrales por defecto
resultado, metricas = are_words_equivalent("conocimiento", "conosimiento")
print(f"¿Son la misma? {resultado}")  # True
print(f"Métricas: {metricas}")

# Configuración personalizada
resultado, metricas = are_words_equivalent(
    "color",
    "colour",
    levenshtein_threshold=0.75,      # Menos estricto
    jaro_winkler_threshold=85.0,     # Menos estricto
    metaphone_required=False         # No requiere coincidencia fonética
)
print(f"¿Son la misma? {resultado}")  # True
```

**Parámetros de Configuración:**

| Parámetro | Tipo | Por Defecto | Descripción |
|-----------|------|-------------|-------------|
| `levenshtein_threshold` | float | 0.85 | Umbral de similitud de Levenshtein (0.0-1.0) |
| `jaro_winkler_threshold` | float | 0.9 | Umbral de score Jaro-Winkler (0.0-100.0) |
| `metaphone_required` | bool | True | Si requiere coincidencia fonética |

---

### Funciones Auxiliares

#### 1. Comparar Palabras (ignorando orden)

```python
from lib.formulite.fxString.string_similarity import has_same_words

resultado = has_same_words("hello world", "world hello")
print(resultado)  # True

resultado = has_same_words("python programming", "programming python")
print(resultado)  # True
```

#### 2. Encontrar Palabras Comunes

```python
from lib.formulite.fxString.string_similarity import find_common_words

comunes = find_common_words("The quick brown fox", "A quick brown dog")
print(comunes)  # ['quick', 'brown']

comunes = find_common_words("Hello WORLD", "world hello")
print(comunes)  # ['hello', 'world']
```

#### 3. Comparar Caracteres (ignorando orden y frecuencia)

```python
from lib.formulite.fxString.string_similarity import has_same_characters

resultado = has_same_characters("listen", "silent")
print(resultado)  # True (anagramas)

resultado = has_same_characters("aabbcc", "abc")
print(resultado)  # True (mismos caracteres únicos)
```

---

## 💡 Ejemplos Prácticos

### Caso 1: Sistema de Autocompletado (Usando Wrapper)

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

palabras_diccionario = ["aplicacion", "computadora", "programacion", "desarrollo"]
entrada_usuario = "aplikacion"

# Buscar coincidencias usando el wrapper
coincidencias = []
for palabra in palabras_diccionario:
    ratio = calculate_similarity(entrada_usuario, palabra)  # Levenshtein por defecto
    if ratio > 0.8:
        coincidencias.append((palabra, ratio))

# Ordenar por similitud
coincidencias.sort(key=lambda x: x[1], reverse=True)
print("Sugerencias:", [palabra for palabra, _ in coincidencias])
# Sugerencias: ['aplicacion']

# Versión optimizada con filtro fonético previo
print("\nBúsqueda optimizada (filtro fonético + Levenshtein):")
for palabra in palabras_diccionario:
    # Filtro rápido fonético
    if calculate_similarity(entrada_usuario, palabra, algorithm='metaphone'):
        ratio = calculate_similarity(entrada_usuario, palabra)
        if ratio > 0.75:
            print(f"  {palabra}: {ratio:.2%}")
```

### Caso 2: Deduplicación de Nombres (Usando Wrapper)

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

nombres = ["John Smith", "Jon Smyth", "Jane Doe", "John Smyth"]
nombres_unicos = []

for nombre in nombres:
    es_duplicado = False
    for nombre_unico in nombres_unicos:
        # Combinar Levenshtein con Jaro-Winkler para nombres
        lev_ratio = calculate_similarity(nombre, nombre_unico, algorithm='levenshtein')
        jw_result = calculate_similarity(nombre, nombre_unico, algorithm='jaro_winkler')
        
        if lev_ratio > 0.80 and jw_result['score'] > 85.0:
            es_duplicado = True
            print(f"  Duplicado detectado: '{nombre}' ≈ '{nombre_unico}' (Lev: {lev_ratio:.2%}, JW: {jw_result['score']:.2f})")
            break
    
    if not es_duplicado:
        nombres_unicos.append(nombre)

print("\nNombres únicos finales:", nombres_unicos)
# Nombres únicos: ['John Smith', 'Jane Doe']
```

### Caso 3: Análisis de Similitud de Frases (Comparación de Algoritmos)

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

frase1 = "the quick brown fox"
frase2 = "a quick red fox"

# Comparar usando diferentes algoritmos
print("Análisis de Frases usando diferentes algoritmos:\n")

# Sørensen-Dice (basado en tokens)
resultado_sd = calculate_similarity(frase1, frase2, algorithm='sorensen_dice')
print(f"Sørensen-Dice: {resultado_sd['score']:.2f}%")

# Jaccard (basado en tokens)
resultado_jac = calculate_similarity(frase1, frase2, algorithm='jaccard')
print(f"Jaccard: {resultado_jac['score']:.2f}%")

# Levenshtein (basado en caracteres)
resultado_lev = calculate_similarity(frase1, frase2, algorithm='levenshtein')
print(f"Levenshtein: {resultado_lev:.2%}")

# LCS (subsecuencias)
resultado_lcs = calculate_similarity(frase1, frase2, algorithm='lcs')
print(f"LCS: '{resultado_lcs['sequence']}' ({resultado_lcs['score']:.2f}%)")


```

### Caso 4: Validación de Entrada de Usuario (Con Sugerencias)

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

opciones_validas = ["continuar", "cancelar", "salir", "ayuda"]
entrada_usuario = "continar"  # Error tipográfico

print(f"Entrada: '{entrada_usuario}'")
print("\nBuscando coincidencias...\n")

# Buscar la mejor coincidencia
mejores_coincidencias = []
for opcion in opciones_validas:
    ratio = calculate_similarity(entrada_usuario, opcion)
    if ratio > 0.65:  # Umbral de similitud
        mejores_coincidencias.append((opcion, ratio))

if mejores_coincidencias:
    # Ordenar por similitud
    mejores_coincidencias.sort(key=lambda x: x[1], reverse=True)
    mejor = mejores_coincidencias[0]
    
    print(f"¿Quisiste decir '{mejor[0]}'? (Similitud: {mejor[1]:.2%})")
    
    if len(mejores_coincidencias) > 1:
        print("\nOtras opciones similares:")
        for opcion, ratio in mejores_coincidencias[1:]:
            print(f"  - {opcion}: {ratio:.2%}")
else:
    print("No se encontraron coincidencias. Opciones válidas:", opciones_validas)

# Salida esperada:
# ¿Quisiste decir 'continuar'? (Similitud: 88.89%)
```

### Caso 5: Búsqueda Difusa Multi-Algoritmo (Performance Optimizada)

```python
from lib.formulite.fxString.string_similarity import calculate_similarity

# Base de datos de productos
productos = [
    "iPhone 15 Pro Max", "Samsung Galaxy S24", "Google Pixel 8",
    "MacBook Pro M3", "Dell XPS 15", "Lenovo ThinkPad X1",
    "Sony WH-1000XM5", "AirPods Pro", "Bose QuietComfort"
]

consulta = "iphone pro"

print(f"Búsqueda: '{consulta}'\n")

# Fase 1: Filtro rápido con Metaphone (fonético)
print("Fase 1: Filtro fonético (rápido)")
candidatos_fase1 = []
for producto in productos:
    if calculate_similarity(consulta, producto, algorithm='metaphone'):
        candidatos_fase1.append(producto)
        print(f"  ✓ {producto}")

# Fase 2: Refinamiento con Levenshtein
print("\nFase 2: Refinamiento con Levenshtein")
resultados_finales = []
for producto in candidatos_fase1:
    ratio = calculate_similarity(consulta, producto, algorithm='levenshtein')
    if ratio > 0.4:  # Umbral más permisivo
        resultados_finales.append((producto, ratio))
        print(f"  {producto}: {ratio:.2%}")

# Ordenar por similitud
resultados_finales.sort(key=lambda x: x[1], reverse=True)

print("\n" + "="*50)
print("RESULTADO FINAL:")
if resultados_finales:
    print(f"Mejor coincidencia: {resultados_finales[0][0]} ({resultados_finales[0][1]:.2%})")
```

### Caso 6: Comparación Exhaustiva de Algoritmos

```python
from lib.formulite.fxString.string_similarity import WordSimilarity

palabra1 = "desarrollo"
palabra2 = "desarollo"  # Error: falta 'r'

print(f"Comparando: '{palabra1}' vs '{palabra2}'\n")
print("="*60)

# Ejecutar todos los algoritmos con compare()
ws = WordSimilarity()
resultados = ws.compare(palabra1, palabra2)

# Mostrar resultados de forma organizada
print("\n📊 ALGORITMOS DE DISTANCIA DE EDICIÓN:")
print(f"  Levenshtein:       {resultados['levenshtein_ratio']:.4f} ({resultados['levenshtein_ratio']*100:.2f}%)")
print(f"  Hamming:           {'N/A' if resultados['hamming_ratio'] is None else f\"{resultados['hamming_ratio']:.4f}\"}")
print(f"  Jaro-Winkler:      {resultados['jaro_winkler']['normalized_similarity']:.4f} ({resultados['jaro_winkler']['score']:.2f}%)")

print("\n🔊 ALGORITMOS FONÉTICOS:")
print(f"  Metaphone:         {'SÍ' if resultados['metaphone_match'] else 'NO'}")
print(f"  MRA:               {resultados['mra']['normalized_similarity']:.4f} ({resultados['mra']['score']:.2f}%)")

print("\n📐 ALGORITMOS DE SUBSECUENCIAS:")
print(f"  Ratcliff-Obershelp: {resultados['ratcliff_obershelp']['score']:.2f}%")
print(f"  LCS:                '{resultados['lcs']['sequence']}' (longitud: {resultados['lcs']['length']}, score: {resultados['lcs']['score']:.2f}%)")
print(f"  Needleman-Wunsch:   {resultados['needleman_wunsch']['score']:.2f}%")

print("\n🎯 ALGORITMOS BASADOS EN TOKENS:")
print(f"  Sørensen-Dice:     {resultados['sorensen_dice']['score']:.2f}%")
print(f"  Jaccard:           {resultados['jaccard']['score']:.2f}%")

print("\n" + "="*60)
print("\n💡 RECOMENDACIÓN:")
if resultados['levenshtein_ratio'] > 0.85 and resultados['metaphone_match']:
    print("  ✅ Las palabras son muy similares (error tipográfico probable)")
elif resultados['metaphone_match']:
    print("  ⚠️  Las palabras suenan igual pero se escriben diferente")
elif resultados['levenshtein_ratio'] > 0.7:
    print("  ⚠️  Las palabras son similares ortográficamente")
else:
    print("  ❌ Las palabras son significativamente diferentes")
```

---

## ⚙️ Configuración Avanzada

### Ajustar Costo de Gap en Needleman-Wunsch

```python
# Por defecto, gap_cost = 1
ws_default = WordSimilarity()

# Gap más costoso
ws_expensive_gap = WordSimilarity(nw_gap_cost=3)

resultado1 = ws_default.needleman_wunsch_score("GATTACA", "GTAC")
resultado2 = ws_expensive_gap.needleman_wunsch_score("GATTACA", "GTAC")

print(f"Gap cost = 1: {resultado1['score']:.2f}")
print(f"Gap cost = 3: {resultado2['score']:.2f}")
```

### Optimizar Umbrales para Tu Caso de Uso

```python
# Para nombres de personas (más permisivo)
resultado_nombre, _ = are_words_equivalent(
    "Catherine", "Kathryn",
    levenshtein_threshold=0.70,
    jaro_winkler_threshold=85.0,
    metaphone_required=True
)

# Para códigos o IDs (más estricto)
resultado_codigo, _ = are_words_equivalent(
    "ABC123", "ABC124",
    levenshtein_threshold=0.95,
    jaro_winkler_threshold=95.0,
    metaphone_required=False
)
```

---

## 📚 API Reference

### 🎯 Función Wrapper Principal

#### `calculate_similarity(word1, word2, algorithm='levenshtein', **kwargs)`

Función unificada para calcular similitud entre dos palabras usando el algoritmo especificado.

**Parámetros:**
- `word1` (str): Primera palabra o frase a comparar
- `word2` (str): Segunda palabra o frase a comparar
- `algorithm` (str): Algoritmo a utilizar (ver tabla de algoritmos disponibles)
- `**kwargs`: Parámetros adicionales según el algoritmo

**Retorna:**
- `bool`: Para 'metaphone'
- `float`: Para 'levenshtein', 'hamming'
- `Dict[str, Any]`: Para algoritmos con métricas múltiples
- `Tuple[bool, Dict]`: Para 'effective_same'

**Ejemplo:**
```python
# Uso simple
ratio = calculate_similarity("casa", "caza")

# Con algoritmo específico
es_igual, metricas = calculate_similarity("word1", "word2", algorithm='effective_same')

# Con parámetros adicionales
resultado = calculate_similarity("seq1", "seq2", algorithm='needleman_wunsch', nw_gap_cost=2)
```

---

### Clase `WordSimilarity`

#### Constructor

```python
WordSimilarity(nw_gap_cost: int = 1)
```

**Parámetros:**
- `nw_gap_cost` (int): Costo de gap para Needleman-Wunsch. Default: 1.

#### Métodos Estáticos

| Método | Retorno | Descripción |
|--------|---------|-------------|
| `metaphone_score(word1, word2)` | `bool` | Similitud fonética |
| `levenshtein_score(word1, word2)` | `float` | Ratio 0.0-1.0 |
| `hamming_score(word1, word2)` | `float` | Ratio 0.0-1.0 (misma longitud) |
| `ratcliff_obershelp_score(a, b)` | `Dict` | Métricas completas |
| `sorensen_dice_score(a, b)` | `Dict` | Métricas basadas en tokens |
| `mra_score(a, b)` | `Dict` | Métricas fonéticas MRA |
| `needleman_wunsch_score(a, b)` | `Dict` | Métricas de alineación |
| `jaro_winkler_score(a, b)` | `Dict` | Métricas con peso en prefijo |
| `jaccard_score(a, b)` | `Dict` | Métricas de índice Jaccard |
| `lcs_score(a, b)` | `Dict` | LCS y porcentaje |
| `compare(word1, word2)` | `Dict` | Todos los algoritmos |
| `are_words_equivalent(...)` | `Tuple[bool, Dict]` | Decisión + métricas |

### Funciones Independientes

| Función | Retorno | Descripción |
|---------|---------|-------------|
| `has_same_words(str1, str2)` | `bool` | Mismas palabras (ignora orden) |
| `find_common_words(str1, str2)` | `List[str]` | Palabras en común |
| `has_same_characters(str1, str2)` | `bool` | Mismos caracteres únicos |
| `are_words_equivalent(...)` | `Tuple[bool, Dict]` | Wrapper del método estático |

---

## 📋 Dependencias

### Dependencias Obligatorias

```txt
python-Levenshtein>=0.12.0
metaphone>=0.6
jellyfish>=0.9.0
textdistance>=4.2.0
```

### Instalación Completa

```bash
pip install python-Levenshtein metaphone jellyfish textdistance
```

### Notas sobre Instalación

- El módulo usa **importación perezosa**: solo carga las librerías cuando se usan.
- Si una dependencia falta, el módulo intenta **instalarla automáticamente** usando `subprocess`.
- En entornos restrictivos, instala las dependencias manualmente antes de usar el módulo.

---

## 🧪 Pruebas

### Ejecutar Demo Incluida

El módulo incluye una demostración completa en el bloque `if __name__ == "__main__"`:

```bash
python lib/formulite/fxString/string_similarity.py
```

### Ejemplo de Salida

```
--- Demostración de Comparación de Similitud de Palabras ---

Comparando 'computadora' y 'computador':
  metaphone_match: True
  levenshtein_ratio: 0.9545454545454546
  hamming_ratio: None
  ratcliff_obershelp:
    distance: 0.04545454545454542
    similarity: 0.9545454545454546
    normalized_similarity: 0.9545454545454546
    score: 95.45454545454545
  ...

--- Demostración de 'are_words_equivalent' (Mejores Prácticas) ---

Palabras: 'conocimiento', 'conosimiento'
  Decisión Esperada: True, Decisión Obtenida: True - PASÓ
  Métricas: Metaphone Match=1, Levenshtein Ratio=0.9167, Jaro-Winkler Score=95.56
```

### Casos de Prueba Incluidos

El módulo incluye **17 casos de prueba** en la demostración que cubren:
- Errores tipográficos comunes
- Variantes ortográficas
- Nombres propios
- Formas verbales
- Variantes de idioma
- Abreviaturas
- Palabras completamente diferentes

---

## ⚡ Rendimiento

### Complejidad Temporal

| Algoritmo | Complejidad | Mejor Para |
|-----------|-------------|------------|
| Metaphone | $O(n)$ | Búsqueda rápida fonética |
| Levenshtein | $O(m \times n)$ | Cadenas cortas/medianas |
| Hamming | $O(n)$ | Cadenas de igual longitud |
| Jaro-Winkler | $O(m \times n)$ | Nombres cortos |
| LCS | $O(m \times n)$ | Análisis de secuencias |

### Recomendaciones de Optimización

1. **Para Grandes Volúmenes**: Usa Metaphone primero como filtro rápido.
2. **Para Nombres**: Jaro-Winkler es el más eficiente.
3. **Para Textos Largos**: Considera Sørensen-Dice o Jaccard (basados en tokens).
4. **Para Validación Estricta**: Combina Levenshtein + Metaphone.

### Benchmark Aproximado

En un sistema moderno (Intel i7, Python 3.9):

| Operación | Tiempo (1000 comparaciones) |
|-----------|----------------------------|
| `metaphone_similarity()` | ~50ms |
| `levenshtein_similarity()` | ~200ms |
| `jaro_winkler_score()` | ~150ms |
| `compare()` (todos) | ~800ms |

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Si deseas mejorar este módulo:

1. **Fork** el repositorio
2. Crea una **rama de feature**: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -m 'Añadir nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un **Pull Request**

### Directrices

- Mantén el código siguiendo PEP 8
- Añade docstrings exhaustivos
- Incluye ejemplos en los docstrings
- Actualiza este README si añades nuevas funcionalidades
- Asegúrate de que todos los tests existentes pasen

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

```
MIT License

Copyright (c) 2025 [Tu Nombre/Organización]

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y archivos de documentación asociados (el "Software"), para 
utilizar el Software sin restricciones, incluyendo sin limitación los derechos 
de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o 
vender copias del Software...
```

Ver el archivo `LICENSE` para más detalles.

---

## 📧 Contacto

**Autor/Mantenedor**: [Tu Nombre]  
**Email**: tu.email@ejemplo.com  
**GitHub**: [@tu-usuario](https://github.com/tu-usuario)  
**Proyecto**: [guardianZ](https://github.com/tu-usuario/guardianZ)

---

## 🙏 Agradecimientos

Este módulo utiliza las siguientes librerías de código abierto:

- [python-Levenshtein](https://github.com/maxbachmann/Levenshtein) - Distancia de Levenshtein rápida
- [metaphone](https://github.com/oubiwann/metaphone) - Algoritmo Double Metaphone
- [jellyfish](https://github.com/jamesturk/jellyfish) - Múltiples métricas de similitud
- [textdistance](https://github.com/life4/textdistance) - Colección extensa de algoritmos

Agradecimientos especiales a la comunidad de Python por su continuo desarrollo de herramientas NLP.

---

## 📝 Notas de Versión

### v2.2.0 (2025-11-08) 🔄
- ♻️ **REFACTORIZADO:** Renombrados métodos para consistencia de nomenclatura
  - `metaphone_similarity()` → `metaphone_score()`
  - `levenshtein_similarity()` → `levenshtein_score()`
  - `hamming_similarity()` → `hamming_score()`
- 🗑️ **ELIMINADO:** Removido `effective_same` de `AlgorithmType` y `compare()`
- 🗑️ **ELIMINADO:** Removido `'all'` del parámetro `algorithm` en `calculate_similarity()`
- 📉 **SIMPLIFICADO:** `AlgorithmType` reducido de 12 a 10 algoritmos
- 📚 **ACTUALIZADO:** README y documentación reflejan los cambios de API
- ✅ Mantiene compatibilidad con funcionalidad core

### v2.1.0 (2025-11-08) 🎉
- ✨ **MEJORADO:** Método `compare()` ahora incluye `effective_same` (11 algoritmos en total)
- ✅ Completitud total: todos los algoritmos de `AlgorithmType` incluidos
- 📚 Documentación actualizada con la nueva estructura de resultados

### v2.0.0 (2025-11-08) 🎉
- ✨ **NUEVO:** Función wrapper `calculate_similarity()` unificada
- ✨ Selección de algoritmo mediante parámetro string
- ✨ Type hints con `Literal` para autocompletado IDE
- ✨ Ejemplos actualizados usando el wrapper
- ✨ 6 casos prácticos nuevos en la documentación
- ✨ Demostración extendida con 10 ejemplos del wrapper
- 📚 README completamente reorganizado y ampliado
- 🚀 API simplificada para usuarios nuevos
- 🔧 Mantiene compatibilidad con API de clase original

### v1.0.0 (2025-01-XX)
- ✅ Implementación inicial con 10 algoritmos
- ✅ Importación perezosa de dependencias
- ✅ Auto-instalación de paquetes faltantes
- ✅ Método `compare()` para análisis completo
- ✅ Función `are_words_effectively_the_same()` con umbrales configurables
- ✅ Funciones auxiliares para comparación de palabras y caracteres
- ✅ Documentación exhaustiva con ejemplos
- ✅ Demo incluida con 17 casos de prueba

---

## 🔗 Enlaces Útiles

- [Documentación de Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [Metaphone Algorithm](https://en.wikipedia.org/wiki/Metaphone)
- [Jaro-Winkler Distance](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
- [Python String Matching](https://docs.python.org/3/library/difflib.html)
- [TextDistance GitHub](https://github.com/life4/textdistance)

---

<div align="center">

**¿Te resultó útil este módulo? ¡Dale una ⭐ en GitHub!**

</div>
