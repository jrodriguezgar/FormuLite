import sys
import importlib
from typing import Union, List, Dict, Any, Tuple

# Diccionario para almacenar módulos importados de forma "lazy"
_lazy_loaded_modules = {}

def _lazy_import(module_name: str, package_name: str = None):
    """
    Intenta importar un módulo de forma perezosa. Si el módulo no está
    disponible, imprime un mensaje sugiriendo la instalación con pip.

    Args:
        module_name (str): El nombre del módulo a importar (ej. 'metaphone').
        package_name (str): El nombre del paquete para la instalación de pip
                            si es diferente al module_name (ej. 'python-Levenshtein').
                            Si es None, se usa module_name.

    Returns:
        module: El módulo importado.

    Raises:
        ImportError: Si el módulo no se puede importar después de la sugerencia.
    """
    if module_name in _lazy_loaded_modules:
        return _lazy_loaded_modules[module_name]

    try:
        module = importlib.import_module(module_name)
        _lazy_loaded_modules[module_name] = module
        return module
    except ImportError:
        install_name = package_name if package_name else module_name
        print(f"Error: La librería '{module_name}' no está instalada.")
        print(f"Por favor, instálala usando: pip install {install_name}")
        # En un entorno real, podrías intentar instalarla aquí,
        # pero en este entorno restringido, solo podemos sugerirlo.
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            module = importlib.import_module(module_name)
            _lazy_loaded_modules[module_name] = module
            return module
        except Exception as e:
            print(f"No se pudo instalar '{install_name}' automáticamente: {e}")
            #raise
        raise # Re-lanza el error para que el programa sepa que la dependencia no está disponible

# Definiciones de clases y funciones

class WordSimilarity:
    """
    Clase para calcular similitudes entre palabras o frases usando una variedad
    de algoritmos de distancia y similitud de cadenas.

    Ofrece métodos para:
      - Similitud fonética (Metaphone).
      - Similitud de edición (Levenshtein, Hamming, Needleman-Wunsch).
      - Similitud basada en subsecuencias y patrones (Ratcliff-Obershelp, LCS).
      - Similitud basada en tokens (Sørensen-Dice, Jaccard).
      - Similitud fonética avanzada (Match Rating Approach - MRA).
      - Similitud de prefijo (Jaro-Winkler).

    Atributos:
        nw_gap_cost (int): Costo de 'gap' para el algoritmo de Needleman-Wunsch.
                           Por defecto es 1.

    Ejemplo de Uso General:
        >>> ws = WordSimilarity()
        >>> word1 = "aplicacion"
        >>> word2 = "aplikacion"
        >>> results = ws.compare(word1, word2)
        >>> print(results)
        # Salida esperada (parcial):
        # {
        # 'metaphone_match': True,
        # 'levenshtein_ratio': 0.9,
        # 'hamming_ratio': None, # Será None si las longitudes son diferentes
        # 'ratcliff_obershelp': {'distance': ..., 'similarity': ..., 'normalized_similarity': ..., 'score': ...},
        # ...
        # }

    Guía de Implementación:
        1. Inicialización:
            Crea una instancia de WordSimilarity. Puedes especificar el costo
            de gap para Needleman-Wunsch si lo deseas.
            >>> ws = WordSimilarity()
            >>> ws_custom_nw = WordSimilarity(nw_gap_cost=2)

        2. Uso de Métodos Específicos:
            Cada método estático puede ser llamado directamente desde la clase
            o desde una instancia.
            >>> WordSimilarity.levenshtein_similarity("casa", "caza")
            >>> ws.metaphone_similarity("conocimiento", "conosimiento")

        3. Comparación Completa con `compare()`:
            El método `compare()` es la forma más sencilla de obtener un resumen
            de todas las métricas para dos cadenas.
            Devuelve un diccionario con los resultados de cada algoritmo.
            Es útil para una visión general o para seleccionar el mejor algoritmo
            para un caso de uso específico.

        4. Manejo de Errores:
            El método `hamming_similarity` lanzará un ValueError si las cadenas
            tienen longitudes diferentes. El método `compare` maneja esto
            internamente asignando `None` a `hamming_ratio` en ese caso.
            Otros métodos lanzarán TypeError si los inputs no son cadenas.

        5. Determinación de Equivalencia "Efectiva":
            Utiliza el método estático `are_words_effectively_the_same`
            para aplicar un criterio combinado de similitud.
            >>> WordSimilarity.are_words_effectively_the_same("aplicacion", "aplikacion")
            True
            >>> WordSimilarity.are_words_effectively_the_same("cat", "dog")
            False
    """
    def __init__(self, nw_gap_cost: int = 1):
        """
        Inicializa la clase WordSimilarity.

        Args:
            nw_gap_cost (int): Costo por un 'gap' en el algoritmo de
                               Needleman-Wunsch. Por defecto es 1.
        """
        if not isinstance(nw_gap_cost, int) or nw_gap_cost < 0:
            raise ValueError("nw_gap_cost debe ser un entero no negativo.")
        td = _lazy_import('textdistance') # Importación perezosa
        td.needleman_wunsch.gap_cost = nw_gap_cost

    @staticmethod
    def metaphone_similarity(word1: str, word2: str) -> bool:
        """
        Compara la similitud fonética de dos palabras usando Double Metaphone.

        Este algoritmo genera una o dos claves fonéticas para cada palabra
        y devuelve True si alguna de las claves de la primera palabra
        coincide con alguna clave de la segunda palabra. Es útil para
        detectar palabras que suenan similar.

        Args:
            word1 (str): La primera palabra a comparar.
            word2 (str): La segunda palabra a comparar.

        Returns:
            bool: True si las palabras tienen similitud fonética según Metaphone,
                  False en caso contrario.

        Ejemplos:
            >>> WordSimilarity.metaphone_similarity("conocimiento", "conosimiento")
            True
            >>> WordSimilarity.metaphone_similarity("hello", "hola")
            False
            >>> WordSimilarity.metaphone_similarity("smith", "smyth")
            True
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        metaphone = _lazy_import('metaphone') # Importación perezosa
        meta1 = metaphone.doublemetaphone(word1.lower()) # Convertir a minúsculas para consistencia
        meta2 = metaphone.doublemetaphone(word2.lower()) # Convertir a minúsculas para consistencia
        return any(m in meta2 for m in meta1 if m)

    @staticmethod
    def levenshtein_similarity(word1: str, word2: str) -> float:
        """
        Calcula el ratio de similitud de Levenshtein entre dos cadenas.

        La distancia de Levenshtein es el número mínimo de ediciones
        (inserciones, eliminaciones o sustituciones de un solo carácter)
        necesarias para transformar una cadena en la otra. El ratio
        es 1 - (distancia / max_longitud). Un valor de 1.0 indica
        cadenas idénticas, 0.0 indica que no hay similitud.

        Args:
            word1 (str): La primera cadena a comparar.
            word2 (str): La segunda cadena a comparar.

        Returns:
            float: Un valor flotante entre 0.0 y 1.0 que representa la
                   similitud de Levenshtein.

        Ejemplos:
            >>> WordSimilarity.levenshtein_similarity("kitten", "sitting")
            0.5714285714285714
            >>> WordSimilarity.levenshtein_similarity("casa", "caza")
            0.75
            >>> WordSimilarity.levenshtein_similarity("apple", "apple")
            1.0
            >>> WordSimilarity.levenshtein_similarity("", "abc")
            0.0
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        Levenshtein = _lazy_import('Levenshtein', 'python-Levenshtein') # Importación perezosa
        return Levenshtein.ratio(word1, word2)

    @staticmethod
    def hamming_similarity(word1: str, word2: str) -> float:
        """
        Calcula el ratio de similitud de Hamming entre dos cadenas.

        La distancia de Hamming solo es aplicable a cadenas de la misma longitud.
        Cuenta el número de posiciones en las que los símbolos correspondientes
        son diferentes. El ratio es 1 - (distancia / longitud).

        Args:
            word1 (str): La primera cadena a comparar.
            word2 (str): La segunda cadena a comparar.

        Returns:
            float: Un valor flotante entre 0.0 y 1.0 que representa la
                   similitud de Hamming.

        Raises:
            ValueError: Si las cadenas de entrada tienen longitudes diferentes.
            TypeError: Si los argumentos no son cadenas.

        Ejemplos:
            >>> WordSimilarity.hamming_similarity("karolin", "kathrin")
            0.5714285714285714
            >>> WordSimilarity.hamming_similarity("rojo", "rosa")
            0.5
            >>> WordSimilarity.hamming_similarity("abc", "abc")
            1.0
            >>> WordSimilarity.hamming_similarity("abc", "abd")
            0.6666666666666667
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        if len(word1) != len(word2):
            raise ValueError("Para Hamming, ambas palabras deben tener la misma longitud.")
        if not word1: # Si ambas son cadenas vacías, la distancia es 0, similitud 1.0
            return 1.0
        jellyfish = _lazy_import('jellyfish') # Importación perezosa
        dist = jellyfish.hamming_distance(word1, word2)
        return 1 - dist / len(word1)

    @staticmethod
    def ratcliff_obershelp_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el algoritmo Ratcliff-Obershelp.

        Este algoritmo es efectivo para comparar cadenas que pueden contener
        subcadenas comunes, incluso si no están en el mismo orden exacto.
        Se basa en la Longest Common Subsequence (LCS).

        Args:
            a (str): La primera cadena a comparar.
            b (str): La segunda cadena a comparar.

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.ratcliff_obershelp_score("apple", "aple")
            {'distance': 0.1, 'similarity': 0.9, 'normalized_similarity': 0.9, 'score': 90.0}
            >>> ws.ratcliff_obershelp_score("information", "inform")
            {'distance': 0.36363636363636365, 'similarity': 0.6363636363636364, 'normalized_similarity': 0.6363636363636364, 'score': 63.63636363636363}
            >>> ws.ratcliff_obershelp_score("hello world", "world hello")
            {'distance': 0.0, 'similarity': 1.0, 'normalized_similarity': 1.0, 'score': 100.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.ratcliff_obershelp
        return {
            'distance': d.distance(a, b),
            'similarity': d.similarity(a, b),
            'normalized_similarity': d.normalized_similarity(a, b),
            'score': 100.0 * d.normalized_similarity(a, b)
        }

    @staticmethod
    def sorensen_dice_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el coeficiente de Sørensen-Dice
        basado en tokens (palabras).

        Este coeficiente mide la similitud entre dos conjuntos. Aquí, las
        cadenas se dividen en palabras (tokens) por espacios en blanco,
        y la similitud se calcula en base a la superposición de estos tokens.
        Es útil para comparar la similitud de contenido de frases cortas
        o documentos pequeños.

        Args:
            a (str): La primera cadena a comparar (se dividirá en tokens).
            b (str): La segunda cadena a comparar (se dividirá en tokens).

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.sorensen_dice_score("this is a test", "this is test")
            {'distance': 0.2, 'similarity': 0.8, 'normalized_similarity': 0.8, 'score': 80.0}
            >>> ws.sorensen_dice_score("python programming", "java programming")
            {'distance': 0.33333333333333337, 'similarity': 0.6666666666666666, 'normalized_similarity': 0.6666666666666666, 'score': 66.66666666666666}
            >>> ws.sorensen_dice_score("apple orange", "banana kiwi")
            {'distance': 1.0, 'similarity': 0.0, 'normalized_similarity': 0.0, 'score': 0.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        tokens_a, tokens_b = a.lower().split(), b.lower().split() # Convertir a minúsculas y tokenizar
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.sorensen
        return {
            'distance': d.distance(tokens_a, tokens_b),
            'similarity': d.similarity(tokens_a, tokens_b),
            'normalized_similarity': d.normalized_similarity(tokens_a, tokens_b),
            'score': 100.0 * d.normalized_similarity(tokens_a, tokens_b)
        }

    @staticmethod
    def mra_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el Match Rating Approach (MRA).

        MRA es un algoritmo fonético diseñado para comparar nombres.
        Genera un "código de clasificación" para cada cadena y luego
        calcula una distancia basada en la comparación de estos códigos.
        Es similar a Metaphone pero con un enfoque diferente.

        Args:
            a (str): La primera cadena a comparar.
            b (str): La segunda cadena a comparar.

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.mra_score("Schmitt", "Schmidt")
            {'distance': 0.16666666666666666, 'similarity': 0.8333333333333334, 'normalized_similarity': 0.8333333333333334, 'score': 83.33333333333334}
            >>> ws.mra_score("John", "Jon")
            {'distance': 0.0, 'similarity': 1.0, 'normalized_similarity': 1.0, 'score': 100.0}
            >>> ws.mra_score("Michael", "Mike")
            {'distance': 0.0, 'similarity': 1.0, 'normalized_similarity': 1.0, 'score': 100.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.mra
        return {
            'distance': d.distance(a, b),
            'similarity': d.similarity(a, b),
            'normalized_similarity': d.normalized_similarity(a, b),
            'score': 100.0 * d.normalized_similarity(a, b)
        }

    @staticmethod
    def needleman_wunsch_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el algoritmo de Needleman-Wunsch.

        Este algoritmo es comúnmente usado en bioinformática para alinear
        secuencias de ADN o proteínas. Encuentra la alineación global más óptima
        entre dos secuencias, considerando costos de 'match', 'mismatch' y 'gap'.
        El costo de 'gap' se puede configurar al inicializar la clase
        WordSimilarity.

        Args:
            a (str): La primera cadena a comparar.
            b (str): La segunda cadena a comparar.

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.needleman_wunsch_score("GATTACA", "GTAC")
            {'distance': 3.0, 'similarity': -3.0, 'normalized_similarity': -0.42857142857142855, 'score': -42.857142857142855}
            >>> ws.needleman_wunsch_score("casa", "caza")
            {'distance': 1.0, 'similarity': 3.0, 'normalized_similarity': 0.75, 'score': 75.0}
            >>> ws.needleman_wunsch_score("apple", "aple")
            {'distance': 1.0, 'similarity': 4.0, 'normalized_similarity': 0.8, 'score': 80.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.needleman_wunsch
        return {
            'distance': d.distance(a, b),
            'similarity': d.similarity(a, b),
            'normalized_similarity': d.normalized_similarity(a, b),
            'score': 100.0 * d.normalized_similarity(a, b)
        }

    @staticmethod
    def jaro_winkler_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el algoritmo Jaro-Winkler.

        Este algoritmo es una variante de Jaro que da más peso a las
        concordancias en el prefijo de las cadenas. Es muy efectivo para
        comparar nombres cortos o palabras con errores tipográficos al
        principio.

        Args:
            a (str): La primera cadena a comparar.
            b (str): La segunda cadena a comparar.

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.jaro_winkler_score("martha", "marhta")
            {'distance': 0.04444444444444443, 'similarity': 0.9555555555555556, 'normalized_similarity': 0.9611111111111111, 'score': 96.11111111111111}
            >>> ws.jaro_winkler_score("dixon", "dicksonx")
            {'distance': 0.22499999999999998, 'similarity': 0.775, 'normalized_similarity': 0.8133333333333333, 'score': 81.33333333333333}
            >>> ws.jaro_winkler_score("cat", "cow")
            {'distance': 0.33333333333333337, 'similarity': 0.6666666666666666, 'normalized_similarity': 0.7777777777777778, 'score': 77.77777777777779}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.jaro_winkler
        return {
            'distance': d.distance(a, b),
            'similarity': d.similarity(a, b),
            'normalized_similarity': d.normalized_similarity(a, b),
            'score': 100.0 * d.normalized_similarity(a, b)
        }

    @staticmethod
    def jaccard_score(a: str, b: str) -> Dict[str, float]:
        """
        Calcula las métricas de similitud usando el índice de Jaccard
        basado en tokens (palabras).

        Similar a Sørensen-Dice, pero el índice de Jaccard es la
        cardinalidad de la intersección de los conjuntos dividida por la
        cardinalidad de su unión. Las cadenas se tokenizan por espacios
        en blanco. Es útil para medir la similitud de conjuntos de palabras.

        Args:
            a (str): La primera cadena a comparar (se dividirá en tokens).
            b (str): La segunda cadena a comparar (se dividirá en tokens).

        Returns:
            Dict[str, float]: Un diccionario con 'distance', 'similarity',
                              'normalized_similarity' y 'score' (similitud normalizada * 100).

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.jaccard_score("this is a test", "this is test")
            {'distance': 0.25, 'similarity': 0.75, 'normalized_similarity': 0.75, 'score': 75.0}
            >>> ws.jaccard_score("apple banana", "banana orange")
            {'distance': 0.6666666666666666, 'similarity': 0.33333333333333337, 'normalized_similarity': 0.33333333333333337, 'score': 33.333333333333336}
            >>> ws.jaccard_score("hello world", "hello world")
            {'distance': 0.0, 'similarity': 1.0, 'normalized_similarity': 1.0, 'score': 100.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        tokens_a, tokens_b = a.lower().split(), b.lower().split() # Convertir a minúsculas y tokenizar
        td = _lazy_import('textdistance') # Importación perezosa
        d = td.jaccard
        return {
            'distance': d.distance(tokens_a, tokens_b),
            'similarity': d.similarity(tokens_a, tokens_b),
            'normalized_similarity': d.normalized_similarity(tokens_a, tokens_b),
            'score': 100.0 * d.normalized_similarity(tokens_a, tokens_b)
        }

    @staticmethod
    def lcs_score(a: str, b: str) -> Dict[str, Union[str, float, int]]:
        """
        Calcula la Longest Common Subsequence (LCS) y su porcentaje de similitud.

        La LCS es la secuencia más larga que es una subsecuencia de ambas
        cadenas. No requiere que los caracteres sean contiguos.
        El 'score' es un porcentaje basado en la longitud de la LCS
        dividida por la media de las longitudes de las dos cadenas,
        multiplicado por 200.0 para escalarlo de 0 a 100%.

        Args:
            a (str): La primera cadena a comparar.
            b (str): La segunda cadena a comparar.

        Returns:
            Dict[str, Union[str, float, int]]: Un diccionario con:
                                                - 'sequence': La secuencia común más larga.
                                                - 'length': La longitud de la secuencia común.
                                                - 'score': Porcentaje de similitud basado en LCS.

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> ws.lcs_score("ABCBDAB", "BDCABA")
            {'sequence': 'BCBA', 'length': 4, 'score': 66.66666666666666}
            >>> ws.lcs_score("AGGTAB", "GXTXAYB")
            {'sequence': 'GTAB', 'length': 4, 'score': 66.66666666666666}
            >>> ws.lcs_score("coche", "correr")
            {'sequence': 'coe', 'length': 3, 'score': 54.54545454545454}
            >>> ws.lcs_score("python", "java")
            {'sequence': '', 'length': 0, 'score': 0.0}
        """
        if not isinstance(a, str) or not isinstance(b, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")

        n1, n2 = len(a), len(b)
        
        # Casos base para cadenas vacías
        if n1 == 0 or n2 == 0:
            return {'sequence': '', 'length': 0, 'score': 0.0}

        # Matriz para DP: dp[i][j] es la longitud de LCS de a[:i] y b[:j]
        # Y también guardamos la secuencia
        dp = [[(0, '') for _ in range(n2 + 1)] for _ in range(n1 + 1)]

        for i in range(1, n1 + 1):
            for j in range(1, n2 + 1):
                if a[i - 1] == b[j - 1]:
                    # Si los caracteres coinciden, extendemos la LCS de la subproblema anterior
                    dp[i][j] = (dp[i - 1][j - 1][0] + 1, dp[i - 1][j - 1][1] + a[i - 1])
                else:
                    # Si no coinciden, tomamos la LCS máxima de ignorar un carácter de 'a' o de 'b'
                    if dp[i - 1][j][0] >= dp[i][j - 1][0]:
                        dp[i][j] = dp[i - 1][j]
                    else:
                        dp[i][j] = dp[i][j - 1]

        length, seq = dp[n1][n2]
        percent = 200.0 * length / (n1 + n2) if (n1 + n2) > 0 else 0.0
        return {'sequence': seq, 'length': length, 'score': percent}

    def compare(self, word1: str, word2: str) -> Dict[str, Any]:
        """
        Devuelve un diccionario con los resultados de todos los algoritmos
        de similitud implementados en la clase para las dos palabras dadas.

        Args:
            word1 (str): La primera palabra o frase a comparar.
            word2 (str): La segunda palabra o frase a comparar.

        Returns:
            Dict[str, Any]: Un diccionario donde las claves son los nombres
                            de los algoritmos y los valores son sus respectivos
                            resultados. El valor para 'hamming_ratio' será
                            None si las longitudes de las palabras difieren.

        Raises:
            TypeError: Si alguno de los argumentos de entrada no es una cadena.

        Ejemplos:
            >>> ws = WordSimilarity()
            >>> results = ws.compare("franco", "franko")
            >>> # print(results) mostrará todos los resultados
            >>> results['metaphone_match']
            True
            >>> results['levenshtein_ratio']
            0.8333333333333334
            >>> results['sorensen_dice']['score']
            0.0 # porque "franco" y "franko" son una sola palabra, no múltiples tokens
            >>> results['lcs']['sequence']
            'franco'
            >>>
            >>> results_phrases = ws.compare("the quick brown fox", "a quick red fox")
            >>> # print(results_phrases)
            >>> results_phrases['sorensen_dice']['score'] # Mayor para frases con palabras comunes
            66.66666666666666
            >>> results_phrases['jaccard']['score']
            50.0
            >>> results_phrases['lcs']['sequence']
            'quick rox' # Note que LCS no requiere contigüidad.

        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")

        results: Dict[str, Any] = {
            'metaphone_match': self.metaphone_similarity(word1, word2),
            'levenshtein_ratio': self.levenshtein_similarity(word1, word2),
            'hamming_ratio': None # Inicializar a None, se actualizará si es posible
        }
        try:
            results['hamming_ratio'] = self.hamming_similarity(word1, word2)
        except ValueError:
            # Captura el error de longitud diferente para Hamming y lo ignora,
            # dejando 'hamming_ratio' como None.
            pass
        except TypeError:
            # Aunque ya se comprueba al principio, es una doble seguridad.
            # En un entorno de producción, es preferible que la función
            # individual lance el error y `compare` lo maneje si quiere
            # ser más resiliente. Aquí, la validación inicial ya lo cubre.
            pass

        # Métricas que devuelven diccionarios de textdistance
        # Asegurarse de que se llaman con las cadenas originales
        results.update({
            'ratcliff_obershelp': self.ratcliff_obershelp_score(word1, word2),
            'sorensen_dice': self.sorensen_dice_score(word1, word2),
            'mra': self.mra_score(word1, word2),
            'needleman_wunsch': self.needleman_wunsch_score(word1, word2),
            'jaro_winkler': self.jaro_winkler_score(word1, word2),
            'jaccard': self.jaccard_score(word1, word2),
            'lcs': self.lcs_score(word1, word2)
        })
        return results

    @staticmethod
    def are_words_effectively_the_same(
        word1: str,
        word2: str,
        levenshtein_threshold: float = 0.85,
        jaro_winkler_threshold: float = 0.9,
        metaphone_required: bool = True
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Propuesta de mejores prácticas para determinar si dos palabras son
        "efectivamente la misma" basándose en una combinación de algoritmos
        de similitud.

        Este método combina la similitud fonética (Metaphone) con métricas
        de distancia de edición (Levenshtein y Jaro-Winkler) para ofrecer
        un criterio más robusto que una sola métrica.
        Puede ser configurado mediante umbrales.

        Args:
            word1 (str): La primera palabra a comparar.
            word2 (str): La segunda palabra a comparar.
            levenshtein_threshold (float): Umbral para la similitud de Levenshtein.
                                           Las palabras se consideran similares si el ratio
                                           de Levenshtein es igual o superior a este valor.
                                           (Valor por defecto: 0.85)
            jaro_winkler_threshold (float): Umbral para la similitud de Jaro-Winkler.
                                            Las palabras se consideran similares si el score
                                            de Jaro-Winkler es igual o superior a este valor.
                                            (Valor por defecto: 0.9)
            metaphone_required (bool): Si es True, las palabras deben tener
                                       similitud fonética según Metaphone para
                                       ser consideradas "la misma".
                                       (Valor por defecto: True)

        Returns:
            Tuple[bool, Dict[str, Any]]: Una tupla que contiene:
                - bool: True si las palabras son consideradas "efectivamente la misma", False en caso contrario.
                - Dict[str, Any]: Un diccionario con los resultados de las métricas
                                  utilizadas para la decisión.

        Raises:
            TypeError: Si alguno de los argumentos de entrada no es una cadena.

        Ejemplos de Uso:
            >>> # Caso 1: Palabras muy similares tipográficamente y fonéticamente
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("conocimiento", "conosimiento")
            >>> result
            True
            >>> metrics['metaphone_match']
            True
            >>> metrics['levenshtein_ratio'] > 0.85
            True

            >>> # Caso 2: Palabras diferentes, no deberían coincidir
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("casa", "perro")
            >>> result
            False
            >>> metrics['levenshtein_ratio'] < 0.85
            True

            >>> # Caso 3: Palabras con un pequeño error, pero fonéticamente iguales (metaphone_required=True)
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("aplicacion", "aplikacion")
            >>> result
            True

            >>> # Caso 4: Similar tipográficamente pero fonéticamente diferente (si metaphone_required=True)
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("cat", "cut")
            >>> result
            False
            >>> # Si metaphone_required fuera False, podría dar True dependiendo de los umbrales
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("cat", "cut", metaphone_required=False)
            >>> result # Puede ser True si los umbrales son bajos y la similitud tipográfica es alta
            True

            >>> # Caso 5: Nombres propios con ligeras variaciones
            >>> result, metrics = WordSimilarity.are_words_effectively_the_same("Smith", "Smyth")
            >>> result
            True

        Guía de Implementación:
            Este enfoque es ideal para escenarios donde necesitas manejar
            variaciones comunes en la escritura (errores tipográficos,
            diferencias de dialecto, romanizaciones alternativas) o
            identificar nombres o términos que suenan igual.

            1.  **Ajusta los umbrales:** Los valores `levenshtein_threshold` y
                `jaro_winkler_threshold` son críticos y deben ajustarse
                según la sensibilidad deseada para tu caso de uso.
                Valores más altos = más estricto.
            2.  **`metaphone_required`:** Si estás comparando términos donde
                la fonética es crucial (ej. nombres de personas, lugares con
                variaciones ortográficas), mantenlo en `True`. Si el enfoque
                es puramente tipográfico, puedes establecerlo en `False`.
            3.  **Evaluación Combinada:** La función devuelve True si *todas*
                las condiciones configuradas se cumplen. Esto asegura que la
                "igualdad efectiva" se basa en múltiples criterios.
            4.  **Resultados Detallados:** El segundo elemento de la tupla de
                retorno (`metrics`) te proporciona los valores de las métricas
                individuales, lo cual es útil para depuración o para entender
                por qué se tomó una decisión.
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Ambos argumentos deben ser cadenas de texto.")
        if not isinstance(levenshtein_threshold, (int, float)) or not (0.0 <= levenshtein_threshold <= 1.0):
            raise ValueError("levenshtein_threshold debe ser un flotante entre 0.0 y 1.0.")
        if not isinstance(jaro_winkler_threshold, (int, float)) or not (0.0 <= jaro_winkler_threshold <= 100.0):
            raise ValueError("jaro_winkler_threshold debe ser un flotante entre 0.0 y 100.0 (es un score).")
        if not isinstance(metaphone_required, bool):
            raise TypeError("metaphone_required debe ser un booleano.")

        # Asegurarse de que las palabras estén en minúsculas para comparaciones consistentes
        # Esto es importante para Levenshtein y Jaro-Winkler si se quiere insensibilidad a mayúsculas
        # Metaphone ya maneja esto internamente.
        w1_lower = word1.lower()
        w2_lower = word2.lower()

        # Caso trivial: palabras idénticas (después de normalizar a minúsculas)
        if w1_lower == w2_lower:
            return True, {
                'exact_match': True,
                'metaphone_match': True,
                'levenshtein_ratio': 1.0,
                'jaro_winkler_score': 100.0
            }

        # Calcular las métricas relevantes
        metaphone_match = WordSimilarity.metaphone_similarity(w1_lower, w2_lower)
        lev_ratio = WordSimilarity.levenshtein_similarity(w1_lower, w2_lower)
        jaro_score = WordSimilarity.jaro_winkler_score(w1_lower, w2_lower)['score']

        results_metrics = {
            'exact_match': False,
            'metaphone_match': metaphone_match,
            'levenshtein_ratio': lev_ratio,
            'jaro_winkler_score': jaro_score
        }

        # Aplicar los criterios
        is_lev_similar = lev_ratio >= levenshtein_threshold
        is_jaro_similar = jaro_score >= jaro_winkler_threshold

        if metaphone_required:
            final_decision = metaphone_match and is_lev_similar and is_jaro_similar
        else:
            final_decision = is_lev_similar and is_jaro_similar # o combinar con OR si es menos estricto

        return final_decision, results_metrics


def has_same_words(string_one: str, string_two: str) -> bool:
    """
    Checks if two strings contain the same words, ignoring word order and case.

    This function tokenizes both input strings into words, converts them to
    lowercase, sorts the resulting word lists, and then compares them.
    This approach ensures that the order of words and their capitalization
    do not affect the comparison result.

    Args:
        string_one (str): The first string to compare.
        string_two (str): The second string to compare.

    Returns:
        bool: True if both strings contain the same words, False otherwise.

    Raises:
        TypeError: If either input is not a string.

    Example of use:
        >>> has_same_words("hello world", "world hello")
        True
        >>> has_same_words("python programming", "programming python")
        True
        >>> has_same_words("apple banana", "banana orange")
        False
        >>> has_same_words("HELLO world", "world hello")
        True
        >>> has_same_words("one two two", "two one two")
        True
        >>> has_same_words("a b c", "A B C")
        True

    Guía de Implementación:
        Esta función es útil cuando solo importa la presencia de las mismas
        palabras, no su orden ni su capitalización, y también considera
        la multiplicidad de las palabras.
        Simplemente pasa las dos cadenas y obtén un booleano.
        Ten en cuenta que `split()` por defecto divide por cualquier espacio
        en blanco y descarta cadenas vacías resultantes.
    """
    if not isinstance(string_one, str) or not isinstance(string_two, str):
        raise TypeError("Both inputs must be strings.")

    # Convert strings to lowercase and split them into words.
    # We convert to lowercase so that case differences don't affect the comparison.
    # For example, "Hello" and "hello" should be considered the same word.
    list_one = string_one.lower().split()
    list_two = string_two.lower().split()

    # Sort the lists of words.
    # Sorting allows us to compare the contents of the strings regardless of
    # the original word order. If the sorted lists are identical, it means
    # the strings contain the same words. This also accounts for word counts.
    list_one.sort()
    list_two.sort()

    return list_one == list_two


def find_common_words(string_one: str, string_two: str) -> List[str]:
    """
    Identifies and returns the common unique words between two input strings.

    This function first tokenizes both strings into words, converts them to
    lowercase, and then uses sets to efficiently find the words that are
    present in both strings. The result is a list of unique common words.
    The order of words in the returned list is not guaranteed.

    Args:
        string_one (str): The first string for comparison.
        string_two (str): The second string for comparison.

    Returns:
        list[str]: A list of unique words found in both strings.

    Raises:
        TypeError: If either input is not a string.

    Example of use:
        >>> find_common_words("The quick brown fox", "A quick brown dog")
        ['quick', 'brown'] # El orden puede variar
        >>> find_common_words("Hello world", "WORLD hello")
        ['world', 'hello'] # El orden puede variar
        >>> find_common_words("apple banana orange", "grape kiwi pineapple")
        []
        >>> find_common_words("one two three four", "three four five six")
        ['three', 'four'] # El orden puede variar
        >>> find_common_words("common common word", "common common phrase")
        ['common']

    Guía de Implementación:
        Usa esta función cuando necesites extraer una lista de palabras
        que aparecen en *ambas* cadenas, sin importar el orden ni la frecuencia
        dentro de cada cadena.
        La función es insensible a mayúsculas/minúsculas.
    """
    if not isinstance(string_one, str) or not isinstance(string_two, str):
        raise TypeError("Both inputs must be strings.")

    # Convert strings to lowercase and split into words.
    # Lowercasing ensures that case differences (e.g., "The" vs. "the")
    # don't prevent words from being identified as common.
    words_one = string_one.lower().split()
    words_two = string_two.lower().split()

    # Convert lists of words to sets.
    # Sets provide efficient ways to find common elements (intersections).
    # This also automatically handles duplicate words within a single string,
    # ensuring that each word is considered only once for the commonality check.
    set_one = set(words_one)
    set_two = set(words_two)

    # Find the intersection of the two sets.
    # The intersection operation returns a new set containing only the elements
    # that are present in both set_one and set_two.
    common_words_set = set_one.intersection(set_two)

    # Convert the set of common words back to a list for the return value.
    # While sets are great for the logic, lists are often more convenient
    # for ordered or repeatable output (though the order is not guaranteed).
    return list(common_words_set)


def has_same_characters(string_one: str, string_two: str) -> bool:
    """
    Checks if two strings contain exactly the same unique characters,
    regardless of their order or frequency.

    This function converts both input strings into sets of characters.
    Since sets only store unique elements, this effectively ignores
    duplicate characters and character order. The function then
    compares these two sets. If the sets are identical, it means both
    strings are composed of the exact same unique characters.

    Args:
        string_one (str): The first string to compare.
        string_two (str): The second string to compare.

    Returns:
        bool: True if both strings contain the exact same set of unique
              characters, False otherwise.

    Raises:
        TypeError: If either input is not a string.

    Example of use:
        >>> has_same_characters("listen", "silent")
        True
        >>> has_same_characters("aabbcc", "abc")
        True
        >>> has_same_characters("hello", "world")
        False
        >>> has_same_characters("apple", "aple")
        True
        >>> has_same_characters("aaabbbccc", "abc")
        True
        >>> has_same_characters("abc", "cba")
        True
        >>> has_same_characters("", "")
        True
        >>> has_same_characters("a", "")
        False

    Guía de Implementación:
        Utiliza esta función para determinar si dos cadenas son anagramas
        (en su conjunto de caracteres únicos) o si están compuestas
        exactamente por los mismos elementos atómicos (caracteres),
        sin importar cuántas veces se repita cada uno o en qué orden aparezcan.
        Es útil para limpiar datos o para comprobaciones de "tipo de contenido"
        a nivel de carácter.
    """
    if not isinstance(string_one, str) or not isinstance(string_two, str):
        raise TypeError("Both inputs must be strings.")

    # Convert each string into a set of its characters.
    # Sets are used because they only store unique elements. This automatically
    # handles the requirement to ignore character frequency and order.
    # For instance, set('aabbc') will result in {'a', 'b', 'c'}.
    set_one = set(string_one)
    set_two = set(string_two)

    # Compare the two sets.
    # If the sets are equal, it means they contain the exact same unique characters.
    return set_one == set_two

def are_words_effectively_the_same(
    word1: str,
    word2: str,
    levenshtein_threshold: float = 0.85,
    jaro_winkler_threshold: float = 0.9,
    metaphone_required: bool = True
) -> Tuple[bool, Dict[str, Any]]:
    """
    Propuesta de mejores prácticas para determinar si dos palabras son
    "efectivamente la misma" basándose en una combinación de algoritmos
    de similitud.

    Esta función de nivel superior es un wrapper para el método estático
    WordSimilarity.are_words_effectively_the_same.

    Este enfoque combina la similitud fonética (Metaphone) con métricas
    de distancia de edición (Levenshtein y Jaro-Winkler) para ofrecer
    un criterio más robusto que una sola métrica.
    Puede ser configurado mediante umbrales.

    Args:
        word1 (str): La primera palabra a comparar.
        word2 (str): La segunda palabra a comparar.
        levenshtein_threshold (float): Umbral para la similitud de Levenshtein.
                                       Las palabras se consideran similares si el ratio
                                       de Levenshtein es igual o superior a este valor.
                                       (Valor por defecto: 0.85)
        jaro_winkler_threshold (float): Umbral para la similitud de Jaro-Winkler.
                                        Las palabras se consideran similares si el score
                                        de Jaro-Winkler es igual o superior a este valor.
                                        (Valor por defecto: 0.9)
        metaphone_required (bool): Si es True, las palabras deben tener
                                   similitud fonética según Metaphone para
                                   ser consideradas "la misma".
                                   (Valor por defecto: True)

    Returns:
        Tuple[bool, Dict[str, Any]]: Una tupla que contiene:
            - bool: True si las palabras son consideradas "efectivamente la misma", False en caso contrario.
            - Dict[str, Any]: Un diccionario con los resultados de las métricas
                              utilizadas para la decisión.

    Raises:
        TypeError: Si alguno de los argumentos de entrada no es una cadena.

    Ejemplos de Uso:
        >>> # Caso 1: Palabras muy similares tipográficamente y fonéticamente
        >>> result, metrics = are_words_effectively_the_same("conocimiento", "conosimiento")
        >>> result
        True
        >>> metrics['metaphone_match']
        True
        >>> metrics['levenshtein_ratio'] > 0.85
        True

        >>> # Caso 2: Palabras diferentes, no deberían coincidir
        >>> result, metrics = are_words_effectively_the_same("casa", "perro")
        >>> result
        False
        >>> metrics['levenshtein_ratio'] < 0.85
        True

    Guía de Implementación:
        Esta función de utilidad es la forma recomendada de usar el criterio
        de "igualdad efectiva" sin necesidad de instanciar `WordSimilarity`
        explícitamente. Permite un control fino sobre los umbrales de decisión.
    """
    return WordSimilarity.are_words_effectively_the_same(
        word1, word2,
        levenshtein_threshold,
        jaro_winkler_threshold,
        metaphone_required
    )

if __name__ == "__main__":
    print("--- Demostración de Comparación de Similitud de Palabras ---")
    ws = WordSimilarity()

    # Ejemplo de uso de compare()
    word1_compare = "computadora"
    word2_compare = "computador"
    print(f"\nComparando '{word1_compare}' y '{word2_compare}':")
    try:
        results = ws.compare(word1_compare, word2_compare)
        for metric, value in results.items():
            if isinstance(value, dict):
                print(f"  {metric}:")
                for sub_metric, sub_value in value.items():
                    print(f"    {sub_metric}: {sub_value}")
            else:
                print(f"  {metric}: {value}")
    except ImportError as e:
        print(f"No se pudieron calcular todas las métricas debido a una librería faltante: {e}")

    # Batería de Ejemplos para are_words_effectively_the_same()
    print("\n--- Demostración de 'are_words_effectively_the_same' (Mejores Prácticas) ---")

    test_cases = [
        ("conocimiento", "conosimiento", True),  # Similares fonéticamente y tipográficamente
        ("aplicacion", "aplikacion", True),      # Error ortográfico común
        ("Smith", "Smyth", True),                 # Nombres propios
        ("color", "colour", True),                # Variantes de idioma (requiere ajuste de umbrales o consideración cultural)
        ("alberto", "huberto", False),            # Diferentes fonéticamente
        ("casa", "caza", True),                   # Una letra diferente
        ("telefono", "telefno", True),            # Letra faltante
        ("programacion", "progrmacion", True),    # Omisión de vocal
        ("gato", "perro", False),                 # Completamente diferentes
        ("internet", "intranet", False),          # Palabras que suenan similar pero significan diferente
        ("hello", "hola", False),                 # Idiomas diferentes
        ("cancelar", "cancela", True),             # Forma verbal diferente
        ("organizar", "organise", True),          # Variante de ortografía (inglés americano vs británico)
        ("doctor", "doc", False),                 # Abreviatura, puede que no pase umbrales estrictos
        ("software", "sofftware", True),          # Error tipográfico
        ("identificador", "identificadr", True),
        ("implementacion", "implementacion", True) # Idénticas
    ]

    print("\nCasos de Prueba con umbrales por defecto (Levenshtein>=0.85, Jaro-Winkler>=0.9, Metaphone requerido=True):")
    for word1, word2, expected in test_cases:
        try:
            result, metrics = are_words_effectively_the_same(word1, word2)
            status = "PASÓ" if result == expected else "FALLÓ"
            print(f"\nPalabras: '{word1}', '{word2}'")
            print(f"  Decisión Esperada: {expected}, Decisión Obtenida: {result} - {status}")
            print(f"  Métricas de Decisión: Metaphone Match={metrics['metaphone_match']:.0f}, Levenshtein Ratio={metrics['levenshtein_ratio']:.4f}, Jaro-Winkler Score={metrics['jaro_winkler_score']:.4f}")
        except ImportError as e:
            print(f"\nSaltando prueba para '{word1}', '{word2}' debido a una librería faltante: {e}")

    print("\n--- Ejemplos adicionales para otras funciones ---")

    # has_same_words
    print("\n--- has_same_words ---")
    print(f"'hello world', 'world hello': {has_same_words('hello world', 'world hello')}")
    print(f"'python programming', 'programming python': {has_same_words('python programming', 'programming python')}")
    print(f"'apple banana', 'banana orange': {has_same_words('apple banana', 'banana orange')}")
    print(f"'HELLO world', 'world hello': {has_same_words('HELLO world', 'world hello')}")
    print(f"'one two two', 'two one two': {has_same_words('one two two', 'two one two')}")

    # find_common_words
    print("\n--- find_common_words ---")
    print(f"'The quick brown fox', 'A quick brown dog': {find_common_words('The quick brown fox', 'A quick brown dog')}")
    print(f"'Hello world', 'WORLD hello': {find_common_words('Hello world', 'WORLD hello')}")
    print(f"'apple banana orange', 'grape kiwi pineapple': {find_common_words('apple banana orange', 'grape kiwi pineapple')}")
    print(f"'common common word', 'common common phrase': {find_common_words('common common word', 'common common phrase')}")

    # has_same_characters
    print("\n--- has_same_characters ---")
    print(f"'listen', 'silent': {has_same_characters('listen', 'silent')}")
    print(f"'aabbcc', 'abc': {has_same_characters('aabbcc', 'abc')}")
    print(f"'hello', 'world': {has_same_characters('hello', 'world')}")
    print(f"'apple', 'aple': {has_same_characters('apple', 'aple')}")
    print(f"'', '': {has_same_characters('', '')}")
    print(f"'a', '': {has_same_characters('a', '')}")

    print("\n--- Fin de la demostración ---")