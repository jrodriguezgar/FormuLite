import math
from decimal import Decimal, ROUND_HALF_EVEN
from typing import List, Union, Any

def is_numeric_type(value: Any) -> bool:
    """Verifica si un valor es de tipo numérico.

    Problema/Necesidad del Usuario: Es común necesitar verificar si un valor es numérico
    antes de realizar operaciones matemáticas, especialmente cuando se reciben datos
    de distintas fuentes.

    Args:
        value (Any): El valor a verificar.

    Returns:
        bool: True si el valor es numérico (int, float, Decimal), False en caso contrario.

    Example:
        >>> is_numeric_type(42)
        True
        >>> is_numeric_type(3.14)
        True
        >>> is_numeric_type(Decimal('10.5'))
        True
        >>> is_numeric_type("123")  # Strings no son considerados numéricos
        False
        >>> is_numeric_type(None)
        False
        >>> is_numeric_type([1, 2, 3])
        False
    """
    return isinstance(value, (int, float, Decimal))


def is_prime(n: int) -> bool:
    """
    Verifica si un número es primo.

    Args:
        n (int): El número a verificar.

    Returns:
        bool: True si el número es primo, False en caso contrario.

    Example:
        >>> is_prime(7)
        True
        >>> is_prime(4)
        False
        >>> is_prime(2)
        True
        >>> is_prime(1)
        False
        >>> is_prime(0)
        False
        >>> is_prime(-7)
        False
    """
    if n < 2:
        return False
    
    # Verificamos solo hasta la raíz cuadrada del número
    # para optimizar el rendimiento
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_primes_up_to(limit: int) -> list[int]:
    """
    Genera una lista de números primos hasta un límite dado usando
    el algoritmo de la Criba de Eratóstenes.

    Args:
        limit (int): El límite superior hasta donde buscar números primos.

    Returns:
        list[int]: Lista de números primos encontrados.

    Raises:
        ValueError: Si el límite es menor que 2.

    Example:
        >>> get_primes_up_to(10)
        [2, 3, 5, 7]
        >>> get_primes_up_to(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
        >>> get_primes_up_to(1)
        ValueError: Limit must be at least 2
        >>> len(get_primes_up_to(100))
        25  # Hay 25 números primos menores que 100
    """
    if limit < 2:
        raise ValueError("Limit must be at least 2")

    # Inicializamos array de booleanos como True
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    # Implementación de la Criba de Eratóstenes
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            # Marcamos como no primos todos los múltiplos de i
            for j in range(i * i, limit + 1, i):
                sieve[j] = False

    # Creamos la lista de primos a partir del array de booleanos
    return [i for i in range(limit + 1) if sieve[i]]
def truncate_float(number: float) -> int:
    """
    Trunca un número flotante, eliminando la parte decimal.
    Similar a int(), pero semánticamente más claro para la operación de truncado.

    Args:
        number (float): El número flotante a truncar.

    Returns:
        int: El número entero resultante, con los decimales eliminados (truncado hacia cero).

    Example:
        >>> truncate_float(3.9)
        3
        >>> truncate_float(-3.9)
        -3
        >>> truncate_float(5.0)
        5
        >>> truncate_float(3.1)
        3
    """
    return math.trunc(number)


def round_to_n_decimals(number: float, decimals: int) -> float:
    """
    Redondea un número flotante a un número específico de decimales.

    Args:
        number (float): El número flotante a redondear.
        decimals (int): El número de posiciones decimales a las que redondear.

    Returns:
        float: El número redondeado.

    Example:
        >>> round_to_n_decimals(3.14159, 2)
        3.14
        >>> round_to_n_decimals(123.4567, 1)
        123.5
        >>> round_to_n_decimals(9.999, 2)
        10.0
    """
    return round(number, decimals)


def round_up(number: float) -> int:
    """
    Redondea un número flotante siempre hacia arriba al entero más cercano.

    Args:
        number (float): El número flotante a redondear hacia arriba.

    Returns:
        int: El entero más pequeño que es mayor o igual que 'number'.

    Example:
        >>> round_up(3.1)
        4
        >>> round_up(3.9)
        4
        >>> round_up(3.0)
        3
        >>> round_up(-3.1)
        -3
    """
    return math.ceil(number)


def round_down(number: float) -> int:
    """
    Redondea un número flotante siempre hacia abajo al entero más cercano.

    Args:
        number (float): El número flotante a redondear hacia abajo.

    Returns:
        int: El entero más grande que es menor o igual que 'number'.

    Example:
        >>> round_down(3.9)
        3
        >>> round_down(3.1)
        3
        >>> round_down(3.0)
        3
        >>> round_down(-3.9)
        -4
    """
    return math.floor(number)


def explicit_truncate(number: float) -> int:
    """
    Elimina la parte decimal de un número flotante sin redondear,
    truncando hacia cero, incluso para números negativos.

    Args:
        number (float): El número flotante a truncar.

    Returns:
        int: El número entero resultante.

    Example:
        >>> explicit_truncate(-4.8)
        -4
        >>> explicit_truncate(4.8)
        4
        >>> explicit_truncate(3.1)
        3
    """
    return math.trunc(number)


def add_with_exact_precision(num1: Union[float, str], num2: Union[float, str]) -> Decimal:
    """
    Suma dos números utilizando el tipo Decimal para evitar errores de precisión.

    Args:
        num1 (Union[float, str]): El primer número, puede ser un flotante o una cadena.
                                  Es recomendable usar cadenas para una precisión total en la entrada.
        num2 (Union[float, str]): El segundo número, puede ser un flotante o una cadena.

    Returns:
        Decimal: El resultado de la suma con precisión decimal exacta.

    Example:
        >>> # Ejemplo con float (demostrando la imprecisión inherente del float)
        >>> 0.1 + 0.2
        0.30000000000000004

        >>> # Ejemplo con Decimal para precisión exacta
        >>> add_with_exact_precision("0.1", "0.2")
        Decimal('0.3')
        >>> add_with_exact_precision(Decimal('0.1'), Decimal('0.2'))
        Decimal('0.3')
        >>> add_with_exact_precision(1.23, 4.56) # Aunque la entrada sea float, la operación interna es precisa
        Decimal('5.79')
    """
    return Decimal(str(num1)) + Decimal(str(num2)) # Convertir a str primero para evitar imprecisiones de float


def format_with_leading_zeros(number: int, width: int) -> str:
    """
    Formatea un número entero como cadena, rellenando con ceros a la izquierda hasta un ancho específico.

    Args:
        number (int): El número entero a formatear.
        width (int): El ancho total deseado de la cadena resultante.

    Returns:
        str: La cadena del número con ceros a la izquierda.

    Example:
        >>> format_with_leading_zeros(5, 3)
        '005'
        >>> format_with_leading_zeros(123, 5)
        '00123'
    """
    return format(number, f'0{width}')


def format_as_percentage(number: float, decimals: int = 2) -> str:
    """
    Formatea un número flotante como una cadena de porcentaje.

    Args:
        number (float): El número a formatear (ej. 0.1234).
        decimals (int): El número de posiciones decimales a mostrar en el porcentaje. Por defecto es 2.

    Returns:
        str: La cadena del porcentaje formateado (ej. "12.34%").

    Example:
        >>> format_as_percentage(0.1234)
        '12.34%'
        >>> format_as_percentage(0.5, 0)
        '50%'
        >>> format_as_percentage(0.005, 1)
        '0.5%'
    """
    return f"{number:.{decimals}%}"


def format_as_scientific_notation(number: float, decimals: int = 2) -> str:
    """
    Formatea un número flotante en notación científica.

    Args:
        number (float): El número a formatear.
        decimals (int): El número de posiciones decimales para la mantisa. Por defecto es 2.

    Returns:
        str: La cadena del número en notación científica (ej. "1.23e+06").

    Example:
        >>> format_as_scientific_notation(1230000)
        '1.23e+06'
        >>> format_as_scientific_notation(0.0000000000456, 1)
        '4.6e-11'
        >>> format_as_scientific_notation(1.0, 0)
        '1e+00'
    """
    return f"{number:.{decimals}e}"


def force_float_division(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    """
    Realiza una división asegurando que el resultado sea siempre un flotante,
    incluso si ambos operandos son enteros.

    Args:
        numerator (Union[int, float]): El numerador.
        denominator (Union[int, float]): El denominador.

    Returns:
        float: El resultado de la división como un número de punto flotante.

    Raises:
        ZeroDivisionError: Si el denominador es cero.

    Example:
        >>> force_float_division(5, 2)
        2.5
        >>> force_float_division(10, 3)
        3.3333333333333335
        >>> force_float_division(7.0, 2)
        3.5
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return float(numerator) / denominator # Asegura que el numerador sea float para la división


def manual_round_and_cast(number: float) -> int:
    """
    Realiza un redondeo manual al entero más cercano y luego castea a int.
    Este método puede usarse como alternativa a round() si se desea evitar
    el comportamiento de 'redondeo al par más cercano' (round half to even) de Python 3.

    Args:
        number (float): El número flotante a redondear y castear.

    Returns:
        int: El entero resultante del redondeo manual.

    Example:
        >>> manual_round_and_cast(3.6)
        4
        >>> manual_round_and_cast(3.2)
        3
        >>> manual_round_and_cast(3.5) # Este redondea siempre hacia arriba para .5
        4
        >>> manual_round_and_cast(2.5) # Este redondea siempre hacia arriba para .5, resultando en 3
        3
        >>> manual_round_and_cast(-3.6)
        -4
        >>> manual_round_and_cast(-3.5) # Este redondea hacia el entero más lejano de cero
        -4
    """
    # Para redondeo al más cercano (hacia arriba para .5 positivo, hacia abajo para .5 negativo)
    # Una forma común para 'round half up' para positivos y 'round half down' para negativos:
    if number >= 0:
        return int(number + 0.5)
    else:
        return int(number - 0.5)


def manual_round_up_to_int(number: float) -> int:
    """
    Redondea un número flotante al entero más cercano, siempre hacia arriba.
    Funciona para positivos y negativos.

    Args:
        number (float): El número flotante a redondear.

    Returns:
        int: El entero resultante, redondeado siempre hacia arriba.

    Example:
        >>> manual_round_up_to_int(3.1)
        4
        >>> manual_round_up_to_int(3.9)
        4
        >>> manual_round_up_to_int(3.0)
        3
        >>> manual_round_up_to_int(-3.1)
        -3 # Redondea de -3.1 a -3 (es más grande o igual a -3.1)
        >>> manual_round_up_to_int(-3.9)
        -3
    """
    # Para flotantes, añadir un valor muy pequeño para asegurar el "paso" si es casi un entero,
    # y luego truncar.
    # Alternativamente, usar math.ceil() que es más directo.
    # Pero si se quiere evitar math, esta es una aproximación:
    if number == int(number): # Si ya es un entero (ej. 3.0)
        return int(number)
    if number > 0:
        return int(number + 0.9999999999999999) # Añade un épsilon para asegurar el redondeo
    else: # Si es negativo, redondea hacia 0 (ej. -3.1 a -3)
        return int(number) if number == int(number) else int(number + 0.9999999999999999) # Equivale a ceil para negativos también


def manual_round_down_to_int(number: float) -> int:
    """
    Redondea un número flotante al entero más cercano, siempre hacia abajo.
    Funciona para positivos y negativos.

    Args:
        number (float): El número flotante a redondear.

    Returns:
        int: El entero resultante, redondeado siempre hacia abajo.

    Example:
        >>> manual_round_down_to_int(3.9)
        3
        >>> manual_round_down_to_int(3.1)
        3
        >>> manual_round_down_to_int(3.0)
        3
        >>> manual_round_down_to_int(-3.1)
        -4 # Redondea de -3.1 a -4 (es más pequeño o igual a -3.1)
        >>> manual_round_down_to_int(-3.9)
        -4
    """
    # Para flotantes, simplemente truncar la parte decimal.
    # Alternativamente, usar math.floor() que es más directo.
    # Pero si se quiere evitar math, esta es la forma:
    if number >= 0:
        return int(number) # Trunca directamente para positivos
    else: # Para negativos, int() trunca hacia cero. Necesitamos floor-like.
        return int(number - 0.0000000000000001) # Sustrae un épsilon para asegurar el redondeo abajo


def round_half_even(number: Union[float, str, Decimal], target_precision: str = "1") -> Decimal:
    """
    Realiza el redondeo bancario (ROUND_HALF_EVEN) de un número a una precisión específica.

    Problema/Necesidad del Usuario: En cálculos financieros o científicos, es vital evitar el
    sesgo acumulativo que puede surgir del redondeo tradicional (donde X.5 siempre se redondea hacia arriba).
    El redondeo bancario (ROUND_HALF_EVEN) mitiga este problema al redondear 0.5 al número par más cercano.

    Objetivos del Producto: Proporcionar una función precisa y fiable para aplicar el
    redondeo bancario, crucial para la integridad de datos en aplicaciones financieras
    y estadísticas.

    Descripción: Esta función toma un número (puede ser float, str o Decimal) y lo redondea
    utilizando la política ROUND_HALF_EVEN. Esto significa que si el dígito a redondear es 5,
    el número se redondeará al número par más cercano. Por ejemplo, 2.5 se redondea a 2,
    mientras que 3.5 se redondea a 4. Si el dígito a redondear no es 5, se comporta como
    el redondeo normal (hacia arriba si es 5 o más, hacia abajo si es menos de 5).
    La precisión objetivo ('target_precision') define a qué lugar decimal se redondea.
    Por ejemplo, "1" para redondear a un entero, "0.1" para un decimal, "0.01" para dos decimales, etc.

    Args:
        number (Union[float, str, Decimal]): El número a redondear. Es recomendable pasarlo como
                                             cadena (str) o ya como un objeto Decimal para evitar
                                             imprecisiones de los floats binarios.
        target_precision (str): Una cadena que representa la precisión deseada.
                                Ejemplo: "1" para redondear a un entero, "0.1" para un decimal,
                                "0.01" para dos decimales, etc. Por defecto es "1" (redondeo a entero).

    Returns:
        Decimal: El número redondeado con la precisión especificada y la política ROUND_HALF_EVEN.

    Raises:
        TypeError: Si 'number' o 'target_precision' no son de tipos válidos.
        decimal.InvalidOperation: Si 'target_precision' no es una cadena que representa un número válido.

    Example:
        >>> # Redondeo al entero más cercano
        >>> round_half_even(Decimal("2.5")) # 2.5 -> 2 (el 2 es par)
        Decimal('2')
        >>> round_half_even(Decimal("3.5")) # 3.5 -> 4 (el 4 es par)
        Decimal('4')
        >>> round_half_even(2.6) # 2.6 -> 3 (se redondea normalmente si no es .5)
        Decimal('3')
        >>> round_half_even(2.4) # 2.4 -> 2 (se redondea normalmente si no es .5)
        Decimal('2')

        >>> # Redondeo a un decimal
        >>> round_half_even(Decimal("2.25"), "0.1") # 2.25 -> 2.2 (el 2 es par)
        Decimal('2.2')
        >>> round_half_even(Decimal("2.35"), "0.1") # 2.35 -> 2.4 (el 4 es par)
        Decimal('2.4')

        >>> # Usando strings para mayor precisión en la entrada
        >>> round_half_even("2.5")
        Decimal('2')
        >>> round_half_even("3.5")
        Decimal('4')
        >>> round_half_even("1.235", "0.01") # Redondea 1.235 a dos decimales. 3 es impar, por lo que 1.23 -> 1.24
        Decimal('1.24')
        >>> round_half_even("1.245", "0.01") # Redondea 1.245 a dos decimales. 4 es par, por lo que 1.24 -> 1.24
        Decimal('1.24')
    """
    if not isinstance(target_precision, str):
        raise TypeError("'target_precision' must be a string (e.g., '1', '0.1', '0.01').")

    # Es crucial convertir el número de entrada a Decimal.
    # Si es float, es mejor pasarlo a str primero para evitar imprecisiones de float.
    if isinstance(number, float):
        number_decimal = Decimal(str(number))
    elif isinstance(number, (str, Decimal)):
        number_decimal = Decimal(number)
    else:
        raise TypeError("'number' must be a float, str, or Decimal object.")

    # Convertir la precisión objetivo a un objeto Decimal para el método quantize
    try:
        quantization_precision = Decimal(target_precision)
    except Exception as e:
        raise decimal.InvalidOperation(f"Invalid 'target_precision' string: {target_precision}. Error: {e}")

    # Realizar el redondeo usando quantize con la política ROUND_HALF_EVEN
    return number_decimal.quantize(quantization_precision, rounding=ROUND_HALF_EVEN)


def round_to_nearest_multiple(number: Union[int, float], base: Union[int, float]) -> Union[int, float]:
    """
    Redondea un número al múltiplo más cercano de una base dada.

    Problema/Necesidad del Usuario: Es necesario ajustar un valor numérico a un incremento
    predefinido (una "base"), como redondear un tiempo a la media hora más cercana o una
    cantidad a múltiplos de 10.

    Objetivos del Producto: Proporcionar una función concisa para alinear valores numéricos
    con un conjunto discreto de múltiplos, mejorando la usabilidad y la coherencia de los datos.

    Descripción: La función toma un `number` (entero o flotante) y una `base` (entero o flotante).
    Primero, divide el `number` por la `base`, luego redondea el resultado al entero más cercano
    utilizando la función `round()` de Python (que usa redondeo "al par más cercano" para .5).
    Finalmente, multiplica este entero redondeado por la `base` para obtener el múltiplo deseado.

    Args:
        number (Union[int, float]): El número a redondear.
        base (Union[int, float]): La base o el múltiplo al que se desea redondear.

    Returns:
        Union[int, float]: El número redondeado al múltiplo más cercano de la base.
                           El tipo de retorno será int si la base es int y el resultado es entero;
                           de lo contrario, será float.

    Raises:
        ValueError: Si 'base' es cero, ya que la división por cero no está permitida.

    Example:
        >>> # Redondear 7 al múltiplo más cercano de 5
        >>> round_to_nearest_multiple(7, 5)
        5

        >>> # Redondear 8 al múltiplo más cercano de 5
        >>> round_to_nearest_multiple(8, 5)
        10

        >>> # Redondear tiempo a la media hora más cercana
        >>> round_to_nearest_multiple(10.25, 0.5) # 10.25 horas -> 10.5 horas (10:30)
        10.5

        >>> # Redondear 23 al múltiplo más cercano de 10
        >>> round_to_nearest_multiple(23, 10)
        20

        >>> # Redondear 25 al múltiplo más cercano de 10 (round half to even: 2.5 -> 2)
        >>> round_to_nearest_multiple(25, 10)
        20

        >>> # Redondear 35 al múltiplo más cercano de 10 (round half to even: 3.5 -> 4)
        >>> round_to_nearest_multiple(35, 10)
        40

        >>> # Base cero (levantará ValueError)
        >>> try:
        >>>     round_to_nearest_multiple(10, 0)
        >>> except ValueError as e:
        >>>     print(f"Error: {e}")
        # Salida esperada: Error: The 'base' for rounding cannot be zero.
    """
    if base == 0:
        raise ValueError("The 'base' for rounding cannot be zero.")

    # Divide el número por la base, redondea el resultado al entero más cercano,
    # y luego multiplica por la base.
    # El round() de Python 3 sigue la regla de "round half to even" (redondeo bancario).
    return round(number / base) * base


def normalize_to_0_1_range(x: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> float:
    """
    Normaliza un número para escalarlo a un rango entre 0 y 1.

    Args:
        x (Union[int, float]): El valor numérico a normalizar.
        min_val (Union[int, float]): El valor mínimo esperado en el rango original.
        max_val (Union[int, float]): El valor máximo esperado en el rango original.

    Returns:
        float: El valor normalizado entre 0 y 1. Si min_val == max_val, devuelve 0.0.

    Raises:
        ValueError: Si 'min_val' es mayor que 'max_val'.

    Example:
        >>> normalize_to_0_1_range(50, 0, 100)
        0.5
        >>> normalize_to_0_1_range(10, 0, 100)
        0.1
        >>> normalize_to_0_1_range(100, 0, 100)
        1.0
        >>> normalize_to_0_1_range(0, 0, 100)
        0.0
        >>> normalize_to_0_1_range(75, 50, 100)
        0.5
        >>> normalize_to_0_1_range(5, 5, 5) # min_val == max_val
        0.0
    """
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val.")
    
    if max_val == min_val:
        return 0.0 # Evitar división por cero si el rango es un solo punto.
                   # En muchos contextos de ML, si el rango es 0, el valor normalizado es 0.

    return (x - min_val) / (max_val - min_val)


def scale_to_new_range(x: Union[int, float], min_x: Union[int, float], max_x: Union[int, float], new_min: Union[int, float], new_max: Union[int, float]) -> float:
    """
    Escala un número de un rango original a un nuevo rango.

    Args:
        x (Union[int, float]): El valor numérico a escalar.
        min_x (Union[int, float]): El valor mínimo del rango original.
        max_x (Union[int, float]): El valor máximo del rango original.
        new_min (Union[int, float]): El valor mínimo del nuevo rango.
        new_max (Union[int, float]): El valor máximo del nuevo rango.

    Returns:
        float: El valor escalado en el nuevo rango. Si max_x == min_x, devuelve new_min.

    Raises:
        ValueError: Si 'min_x' es mayor que 'max_x'.

    Example:
        >>> # Escalar 50 de 0-100 a 0-10
        >>> scale_to_new_range(50, 0, 100, 0, 10)
        5.0
        >>> # Escalar 120 de 0-200 a 0-1
        >>> scale_to_new_range(120, 0, 200, 0, 1)
        0.6
        >>> # Escalar 50 de 0-100 a 100-200
        >>> scale_to_new_range(50, 0, 100, 100, 200)
        150.0
        >>> # Escalar 5 de 5-5 a 0-10 (rango original de un solo punto)
        >>> scale_to_new_range(5, 5, 5, 0, 10)
        0.0
    """
    if min_x > max_x:
        raise ValueError("min_x cannot be greater than max_x.")
    
    if max_x == min_x:
        return float(new_min) # Si el rango original es un solo punto, el valor escalado es el new_min.

    # Fórmula de escalado lineal
    normalized_x = (x - min_x) / (max_x - min_x)
    new_val = new_min + normalized_x * (new_max - new_min)
    return float(new_val)


def clip_number(x: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """
    Fuerza que un número esté dentro de un rango específico [min_val, max_val].
    Si el número es menor que min_val, devuelve min_val.
    Si el número es mayor que max_val, devuelve max_val.
    Si el número está dentro del rango, devuelve el número original.

    Args:
        x (Union[int, float]): El número a "recortar" (clip).
        min_val (Union[int, float]): El valor mínimo permitido.
        max_val (Union[int, float]): El valor máximo permitido.

    Returns:
        Union[int, float]: El número ajustado al rango.

    Raises:
        ValueError: Si 'min_val' es mayor que 'max_val'.

    Example:
        >>> clip_number(10, 0, 100)
        10
        >>> clip_number(-5, 0, 100)
        0
        >>> clip_number(150, 0, 100)
        100
        >>> clip_number(50.5, 0.0, 100.0)
        50.5
        >>> clip_number(5, 10, 20) # Min es 10, valor es 5 -> devuelve 10
        10
    """
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val.")

    return max(min(x, max_val), min_val)


def reduce_to_modulo_range(x: Union[int, float], base: Union[int, float]) -> Union[int, float]:
    """
    Convierte un valor a un rango cíclico utilizando la operación de módulo.
    El resultado estará en el rango [0, base) para números positivos,
    o en el rango (-base, 0] para números negativos (si x es negativo).

    Args:
        x (Union[int, float]): El valor numérico a reducir.
        base (Union[int, float]): La base del ciclo (el tamaño del rango).
                                   Debe ser un número positivo.

    Returns:
        Union[int, float]: El valor reducido al rango cíclico.

    Raises:
        ValueError: Si 'base' es cero o negativo.

    Example:
        >>> # Ejemplo con reloj (horas en un día)
        >>> reduce_to_modulo_range(25, 24)
        1 # 25 horas es la 1 AM del día siguiente

        >>> # Ejemplo con ángulos (360 grados)
        >>> reduce_to_modulo_range(370, 360)
        10 # 370 grados es equivalente a 10 grados

        >>> # Ejemplo con valores negativos
        >>> reduce_to_modulo_range(-5, 10)
        5 # -5 es 5 unidades antes de 0 en un ciclo de 10

        >>> reduce_to_modulo_range(-25, 24)
        23 # -25 horas es la 23 PM del día anterior

        >>> # Base cero (levantará ValueError)
        >>> try:
        >>>     reduce_to_modulo_range(10, 0)
        >>> except ValueError as e:
        >>>     print(f"Error: {e}")
        # Salida esperada: Error: The 'base' must be a positive number.
    """
    if base <= 0:
        raise ValueError("The 'base' must be a positive number.")
    
    # La operación de módulo (%) en Python maneja correctamente los números negativos,
    # asegurando que el resultado tenga el mismo signo que el divisor (base).
    return x % base


def quantize_number(x: Union[int, float], step: Union[int, float]) -> Union[int, float]:
    """
    Cuantiza un número, forzándolo a tomar solo ciertos valores discretos (múltiplos del 'step').
    Esto es útil para simplificar valores o ajustarlos a una granularidad específica.

    Args:
        x (Union[int, float]): El número a cuantizar.
        step (Union[int, float]): El tamaño del incremento o el "paso" para la cuantización.
                                  Debe ser un número positivo.

    Returns:
        Union[int, float]: El número cuantizado al múltiplo más cercano del 'step'.
                           El tipo de retorno será int si el step es int y el resultado es entero;
                           de lo contrario, será float.

    Raises:
        ValueError: Si 'step' es cero o negativo.

    Example:
        >>> # Cuantizar a múltiplos de 0.25
        >>> quantize_number(1.23, 0.25)
        1.25
        >>> quantize_number(1.10, 0.25)
        1.0
        >>> quantize_number(1.12, 0.25)
        1.0
        >>> quantize_number(1.13, 0.25)
        1.25

        >>> # Cuantizar a múltiplos de 10
        >>> quantize_number(23, 10)
        20
        >>> quantize_number(27, 10)
        30
        >>> quantize_number(25, 10) # Redondeo al par más cercano (round half to even: 2.5 -> 2)
        20

        >>> # Step cero (levantará ValueError)
        >>> try:
        >>>     quantize_number(10, 0)
        >>> except ValueError as e:
        >>>     print(f"Error: {e}")
        # Salida esperada: Error: The 'step' for quantization cannot be zero or negative.
    """
    if step <= 0:
        raise ValueError("The 'step' for quantization cannot be zero or negative.")

    # Divide por el paso, redondea al entero más cercano y multiplica por el paso.
    # Se usa round() que en Python 3 usa la regla de redondeo "round half to even".
    return round(x / step) * step


def add_bool_to_int(boolean_value: bool, int_value: int) -> int:
    """
    Suma un valor booleano a un entero.

    En Python, True se evalúa como 1 y False como 0 en contextos numéricos.
    Esto permite usar booleanos directamente en operaciones aritméticas,
    lo cual es especialmente útil para crear contadores condicionales.

    Args:
        boolean_value (bool): El valor booleano (True o False).
        int_value (int): El número entero al que se sumará el booleano.

    Returns:
        int: El resultado de la suma.

    Raises:
        TypeError: Si 'boolean_value' no es un booleano o 'int_value' no es un entero.

    Example:
        >>> add_bool_to_int(True, 2)
        3
        >>> add_bool_to_int(False, 5)
        5
        >>> add_bool_to_int(True, 0)
        1
        >>> add_bool_to_int(False, -3)
        -3
        >>> # Uso en un contexto de conteo (no es parte de la función, solo demostración)
        >>> counter = 0
        >>> is_active = True
        >>> has_permission = False
        >>> counter += is_active  # counter se convierte en 1
        >>> counter += has_permission # counter sigue siendo 1
        >>> counter
        1
    """
    if not isinstance(boolean_value, bool):
        raise TypeError("'boolean_value' must be a boolean.")
    if not isinstance(int_value, int):
        raise TypeError("'int_value' must be an integer.")

    # Python convierte automáticamente boolean_value a 1 o 0
    return boolean_value + int_value


def safe_sum_with_none(num1: Union[int, float, None], num2: Union[int, float, None]) -> Union[int, float]:
    """
    Realiza una suma de dos números, manejando de forma segura los valores None.

    Problema/Necesidad del Usuario: La suma directa con None en Python resulta en un TypeError.
    Es necesario un mecanismo para procesar números que pueden ser None, tratándolos como 0
    o validando su existencia antes de la operación.

    Objetivos del Producto: Proporcionar una función robusta para sumar números,
    que sea tolerante a la presencia de None, evitando errores y mejorando la fiabilidad del código.

    Descripción: Esta función toma dos argumentos, `num1` y `num2`, que pueden ser enteros,
    flotantes o None. Antes de realizar la suma, cada argumento se verifica. Si es None,
    se sustituye por 0. Esto asegura que la operación aritmética siempre se realice entre números.

    Args:
        num1 (Union[int, float, None]): El primer número (o None).
        num2 (Union[int, float, None]): El segundo número (o None).

    Returns:
        Union[int, float]: El resultado de la suma. El tipo de retorno dependerá de
                           los tipos de los números involucrados (int si ambos son int,
                           float si al menos uno es float).

    Raises:
        TypeError: Si alguno de los valores, después de la sustitución de None, no es un número.
                   (Aunque la función está diseñada para evitar esto si la entrada esperada es int/float/None).

    Example:
        >>> safe_sum_with_none(3, 5)
        8
        >>> safe_sum_with_none(3, None)
        3
        >>> safe_sum_with_none(None, 5)
        5
        >>> safe_sum_with_none(None, None)
        0
        >>> safe_sum_with_none(3.5, None)
        3.5
        >>> safe_sum_with_none(10, -3)
        7

        >>> # Ejemplo de lo que ocurriría sin la función (causaría TypeError)
        >>> # try:
        >>> #     print(3 + None)
        >>> # except TypeError as e:
        >>> #     print(f"Error esperado: {e}")
        # Salida esperada: Error esperado: unsupported operand type(s) for +: 'int' and 'NoneType'

        >>> # Un caso donde la función aún podría fallar (si la entrada no es None, int, o float)
        >>> # try:
        >>> #     safe_sum_with_none("abc", 5)
        >>> # except TypeError as e:
        >>> #     print(f"Error esperado: {e}")
        # Salida esperada: Error esperado: unsupported operand type(s) for +: 'str' and 'int'
    """
    # Reemplazar None con 0 para la suma
    val1 = num1 if num1 is not None else 0
    val2 = num2 if num2 is not None else 0

    # Ahora que sabemos que val1 y val2 son números (o 0), podemos sumarlos.
    # Python manejará automáticamente la promoción de tipos (int + float = float).
    return val1 + val2


def count_true_with_sum(boolean_list: List[bool]) -> int:
    """
    Cuenta el número de valores True en una lista de booleanos utilizando la función sum().

    Problema/Necesidad del Usuario: Contar eficientemente cuántas condiciones se cumplen
    o cuántos ítems en una colección satisfacen un criterio.

    Objetivos del Producto: Proporcionar una forma idiomática y concisa de contar
    condiciones verdaderas, aprovechando la naturaleza numérica de los booleanos en Python.

    Descripción: Esta función toma una lista de valores booleanos. Internamente, Python
    trata True como 1 y False como 0. La función sum() simplemente suma estos valores
    (1s y 0s), resultando en un conteo directo de cuántos True hay en la lista.

    Args:
        boolean_list (List[bool]): Una lista que contiene valores True o False.

    Returns:
        int: El número total de valores True en la lista.

    Raises:
        TypeError: Si 'boolean_list' no es una lista o contiene elementos que no son booleanos.

    Example:
        >>> count_true_with_sum([True, False, True, True])
        3
        >>> count_true_with_sum([False, False, False])
        0
        >>> count_true_with_sum([])
        0
        >>> count_true_with_sum([True, False])
        1

        >>> # Ejemplo con un generador (más eficiente para grandes datasets)
        >>> # Esto no es parte de la función, sino una demostración de uso.
        >>> numbers = [1, 2, 3, 4, 5, 6]
        >>> count_even = sum(1 for n in numbers if n % 2 == 0) # Generador de 1s para True
        >>> print(f"Números pares: {count_even}")
        # Salida esperada: Números pares: 3

        >>> # Otro ejemplo más directo usando el booleano directamente:
        >>> count_even_direct = sum(n % 2 == 0 for n in numbers)
        >>> print(f"Números pares (directo): {count_even_direct}")
        # Salida esperada: Números pares (directo): 3
    """
    if not isinstance(boolean_list, list):
        raise TypeError("'boolean_list' must be a list.")
    
    # Validar que todos los elementos sean booleanos para una función tipada
    for item in boolean_list:
        if not isinstance(item, bool):
            raise TypeError("All elements in 'boolean_list' must be booleans.")

    # Python trata True como 1 y False como 0 en sum()
    return sum(boolean_list)


def true_division(numerator: Union[int, float], denominator: Union[int, float]) -> float:
    """
    Realiza una división "verdadera" (flotante), siempre devolviendo un número de punto flotante.

    Args:
        numerator (Union[int, float]): El dividendo.
        denominator (Union[int, float]): El divisor.

    Returns:
        float: El resultado de la división como un flotante.

    Raises:
        ZeroDivisionError: Si el divisor es cero.

    Example:
        >>> true_division(5, 2)
        2.5
        >>> true_division(10, 4)
        2.5
        >>> true_division(6, 2) # Aunque el resultado es entero, se devuelve como float
        3.0
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return numerator / denominator


def floor_division(numerator: Union[int, float], denominator: Union[int, float]) -> Union[int, float]:
    """
    Realiza una división entera (división de piso), truncando el resultado hacia abajo.

    Args:
        numerator (Union[int, float]): El dividendo.
        denominator (Union[int, float]): El divisor.

    Returns:
        Union[int, float]: La parte entera del cociente. El tipo será int si ambos operandos
                           eran int, o float si al menos uno era float.

    Raises:
        ZeroDivisionError: Si el divisor es cero.

    Example:
        >>> floor_division(5, 2)
        2
        >>> floor_division(10, 4)
        2
        >>> floor_division(7, 3)
        2
        >>> floor_division(-5, 2) # -2.5 truncado hacia abajo es -3
        -3
        >>> floor_division(5.0, 2) # Si un operando es float, el resultado es float
        2.0
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return numerator // denominator


def safe_division_for_context(
    numerator: Union[int, float],
    denominator: Union[int, float],
    return_float: bool = True
) -> Union[int, float]:
    """
    Realiza una división seleccionando el operador adecuado según la necesidad del contexto.

    Args:
        numerator (Union[int, float]): El dividendo.
        denominator (Union[int, float]): El divisor.
        return_float (bool): Si es True, realiza división flotante (`/`).
                             Si es False, realiza división entera (`//`).
                             Por defecto es True.

    Returns:
        Union[int, float]: El resultado de la división, ya sea un float o un int/float truncado.

    Raises:
        ZeroDivisionError: Si el divisor es cero.

    Example:
        >>> safe_division_for_context(5, 2, return_float=True)
        2.5
        >>> safe_division_for_context(5, 2, return_float=False)
        2
        >>> safe_division_for_context(10, 3, return_float=True)
        3.3333333333333335
        >>> safe_division_for_context(10, 3, return_float=False)
        3
        >>> safe_division_for_context(7.0, 2, return_float=False) # Float operand -> float result
        3.0
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")

    if return_float:
        return numerator / denominator
    else:
        return numerator // denominator
    

def compare_floats_with_tolerance(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 1e-5) -> bool:
    """
    Compara dos números de punto flotante (floats) para determinar si son 
    "cercanos" entre sí, utilizando tolerancias relativas y absolutas.

    Esta función es ideal para comparar floats en sistemas donde la precisión
    inherente de los cálculos de punto flotante puede llevar a pequeñas
    diferencias que no deberían considerarse significativas.

    Args:
        a (float): El primer número de punto flotante a comparar.
        b (float): El segundo número de punto flotante a comparar.
        rel_tol (float): La tolerancia relativa. Representa la máxima
                         diferencia permitida entre 'a' y 'b', relativa al
                         mayor de sus valores absolutos. Por defecto, es 1e-9.
                         Útil para números grandes.
        abs_tol (float): La tolerancia absoluta. Representa la máxima
                         diferencia fija permitida entre 'a' y 'b',
                         independientemente de su magnitud. Por defecto, es 1e-5.
                         Útil para números cercanos a cero.

    Returns:
        bool: True si 'a' y 'b' se consideran cercanos según las tolerancias,
              False en caso contrario.

    Ejemplo de uso:
    >>> compare_floats_with_tolerance(0.1 + 0.2, 0.3)
    True
    >>> compare_floats_with_tolerance(1000000.0, 1000000.0000001, rel_tol=1e-9)
    True
    >>> compare_floats_with_tolerance(0.0000001, 0.0000002, abs_tol=1e-6)
    True
    """
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


