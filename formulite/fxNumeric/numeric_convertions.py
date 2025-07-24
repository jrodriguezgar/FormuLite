import json
from decimal import Decimal, getcontext
import locale
from typing import Any, Union, Optional

# JavaScript's safe integer limit
JS_MAX_SAFE_INTEGER = 2**53 - 1
JS_MIN_SAFE_INTEGER = -(2**53 - 1)

from datetime import datetime, timezone

def float_to_int_truncated(number: float) -> int:
    """
    Convierte un número flotante a un entero, truncando los decimales (hacia cero).

    Args:
        number (float): El número flotante a convertir.

    Returns:
        int: El número entero resultante, sin la parte decimal.

    Example:
        >>> float_to_int_truncated(3.9)
        3
        >>> float_to_int_truncated(-3.9)
        -3
        >>> float_to_int_truncated(5.0)
        5
    """
    return int(number)


def int_to_float(number: int) -> float:
    """
    Convierte un número entero a un número de punto flotante.

    Args:
        number (int): El número entero a convertir.

    Returns:
        float: El número decimal resultante.

    Example:
        >>> int_to_float(5)
        5.0
        >>> int_to_float(-10)
        -10.0
    """
    return float(number)


def number_to_complex(number: Union[int, float]) -> complex:
    """
    Convierte un número entero o flotante a un número complejo con parte imaginaria cero.

    Args:
        number (Union[int, float]): El número a convertir.

    Returns:
        complex: El número complejo resultante.

    Example:
        >>> number_to_complex(4.2)
        (4.2+0j)
        >>> number_to_complex(7)
        (7+0j)
    """
    return complex(number)


def number_to_bool(number: Union[int, float]) -> bool:
    """
    Convierte un número entero o flotante a un valor booleano.
    0 o 0.0 se convierten en False; cualquier otro número se convierte en True.

    Args:
        number (Union[int, float]): El número a convertir.

    Returns:
        bool: El valor booleano resultante.

    Example:
        >>> number_to_bool(0)
        False
        >>> number_to_bool(3.5)
        True
        >>> number_to_bool(-1)
        True
        >>> number_to_bool(0.0)
        False
    """
    return bool(number)


def bool_to_int(value: bool) -> int:
    """
    Convierte un valor booleano a un entero.
    True se convierte en 1; False se convierte en 0.

    Args:
        value (bool): El valor booleano a convertir.

    Returns:
        int: El entero resultante.

    Example:
        >>> bool_to_int(True)
        1
        >>> bool_to_int(False)
        0
    """
    return int(value)


def bool_to_float(value: bool) -> float:
    """
    Convierte un valor booleano a un número de punto flotante.
    True se convierte en 1.0; False se convierte en 0.0.

    Args:
        value (bool): El valor booleano a convertir.

    Returns:
        float: El número decimal resultante.

    Example:
        >>> bool_to_float(True)
        1.0
        >>> bool_to_float(False)
        0.0
    """
    return float(value)


def number_to_string(number: Union[int, float]) -> str:
    """
    Convierte un número entero o flotante a su representación de cadena.

    Args:
        number (Union[int, float]): El número a convertir.

    Returns:
        str: La cadena de texto resultante.

    Example:
        >>> number_to_string(3.14)
        '3.14'
        >>> number_to_string(100)
        '100'
        >>> number_to_string(-0.5)
        '-0.5'
    """
    return str(number)


def round_float_to_int(number: float) -> int:
    """
    Redondea un número flotante al entero más cercano.

    Args:
        number (float): El número flotante a redondear.

    Returns:
        int: El entero más cercano al número dado.
             Si el número está exactamente a mitad de camino entre dos enteros (ej. X.5),
             Python 3.x redondea al entero par más cercano (redondeo "al par más cercano" o "bancario").

    Example:
        >>> round_float_to_int(3.6)
        4
        >>> round_float_to_int(3.2)
        3
        >>> round_float_to_int(3.5) # Redondea al par más cercano (3 es impar, 4 es par)
        4
        >>> round_float_to_int(2.5) # Redondea al par más cercano (2 es par)
        2
        >>> round_float_to_int(-3.6)
        -4
        >>> round_float_to_int(-3.5) # Redondea al par más cercano (-4 es par)
        -4
    """
    return round(number)



def hex_to_int(hex_string: str) -> int:
    """
    Convierte una cadena hexadecimal a un número entero.

    Args:
        hex_string (str): La cadena hexadecimal (puede tener prefijo '0x').

    Returns:
        int: El número entero decimal.

    Example:
        >>> hex_to_int("0xff")
        255
        >>> hex_to_int("FF")
        255
        >>> hex_to_int("a")
        10
    """
    return int(hex_string, 16)


def bin_to_int(bin_string: str) -> int:
    """
    Convierte una cadena binaria a un número entero.

    Args:
        bin_string (str): La cadena binaria (puede tener prefijo '0b').

    Returns:
        int: El número entero decimal.

    Example:
        >>> bin_to_int("0b1010")
        10
        >>> bin_to_int("111")
        7
    """
    return int(bin_string, 2)


def octal_to_int(octal_string: str) -> int:
    """
    Convierte una cadena octal a un número entero.

    Args:
        octal_string (str): La cadena octal (puede tener prefijo '0o').

    Returns:
        int: El número entero decimal.

    Example:
        >>> octal_to_int("0o17")
        15
        >>> octal_to_int("77")
        63
    """
    return int(octal_string, 8)

def int_to_binary_clean(number: int) -> str:
    """
    Convierte un número entero a su representación binaria como cadena, sin el prefijo '0b'.

    Args:
        number (int): El número entero a convertir.

    Returns:
        str: La cadena binaria.

    Example:
        >>> int_to_binary_clean(10)
        '1010'
        >>> int_to_binary_clean(5)
        '101'
    """
    return format(number, 'b')


def int_to_hex_clean(number: int) -> str:
    """
    Convierte un número entero a su representación hexadecimal como cadena, sin el prefijo '0x'.

    Args:
        number (int): El número entero a convertir.

    Returns:
        str: La cadena hexadecimal (en minúsculas).

    Example:
        >>> int_to_hex_clean(255)
        'ff'
        >>> int_to_hex_clean(10)
        'a'
    """
    return format(number, 'x')


def int_to_binary_with_prefix(number: int) -> str:
    """
    Convierte un número entero a su representación binaria como cadena, incluyendo el prefijo '0b'.

    Args:
        number (int): El número entero a convertir.

    Returns:
        str: La cadena binaria con prefijo.

    Example:
        >>> int_to_binary_with_prefix(255)
        '0b11111111'
        >>> int_to_binary_with_prefix(10)
        '0b1010'
    """
    return format(number, '#b')


def int_to_hex_with_prefix(number: int) -> str:
    """
    Convierte un número entero a su representación hexadecimal como cadena, incluyendo el prefijo '0x'.

    Args:
        number (int): El número entero a convertir.

    Returns:
        str: La cadena hexadecimal con prefijo (en minúsculas).

    Example:
        >>> int_to_hex_with_prefix(255)
        '0xff'
        >>> int_to_hex_with_prefix(10)
        '0xa'
    """
    return format(number, '#x')


def int_to_octal_with_prefix(number: int) -> str:
    """
    Convierte un número entero a su representación octal como cadena, incluyendo el prefijo '0o'.

    Args:
        number (int): El número entero a convertir.

    Returns:
        str: La cadena octal con prefijo.

    Example:
        >>> int_to_octal_with_prefix(255)
        '0o377'
        >>> int_to_octal_with_prefix(15)
        '0o17'
    """
    return format(number, '#o')


def datetime_to_unix_timestamp(dt: datetime) -> float:
    """
    Convierte un objeto datetime a su correspondiente timestamp numérico UNIX (flotante).
    El timestamp representa los segundos transcurridos desde el Epoch (1 de enero de 1970, 00:00:00 UTC).

    Args:
        dt (datetime): El objeto datetime a convertir.

    Returns:
        float: El timestamp UNIX como un número flotante.

    Raises:
        TypeError: Si 'dt' no es un objeto datetime.

    Example:
        >>> from datetime import datetime, timezone
        >>> # Usando una fecha y hora específica (asegurando que sea UTC o aware)
        >>> dt_utc = datetime(2025, 6, 11, 10, 27, 5, 0, tzinfo=timezone.utc)
        >>> datetime_to_unix_timestamp(dt_utc)
        1718092025.0

        >>> # Usando la fecha y hora actual (se recomienda UTC para timestamps)
        >>> import time
        >>> current_dt_utc = datetime.now(timezone.utc)
        >>> current_timestamp = datetime_to_unix_timestamp(current_dt_utc)
        >>> # Comparar con time.time() para verificar (time.time() devuelve float de segundos desde epoch)
        >>> # abs(current_timestamp - time.time()) < 1.0 # Debería ser True
    """
    if not isinstance(dt, datetime):
        raise TypeError("'dt' must be a datetime object.")
    
    # El método .timestamp() maneja correctamente las zonas horarias si el datetime es "aware".
    # Si es "naive" (sin tzinfo), se asume que está en la hora local del sistema.
    return dt.timestamp()


def unix_timestamp_to_datetime(timestamp: Union[int, float], tz_info: Optional[str] = None) -> datetime:
    """
    Convierte un timestamp numérico UNIX (segundos desde el Epoch) a un objeto datetime.

    Args:
        timestamp (Union[int, float]): El timestamp UNIX.
        tz_info (Optional[str]): Un string IANA timezone (ej. 'America/New_York', 'Europe/Madrid').
                                 Si se proporciona, el datetime resultante será "aware" (con zona horaria).
                                 Si es None, el datetime será "naive" (sin zona horaria, asumiendo local).

    Returns:
        datetime: El objeto datetime resultante.

    Raises:
        TypeError: Si 'timestamp' no es un int o float, o si 'tz_info' no es un string.
        zoneinfo.ZoneInfoNotFoundError: Si el string 'tz_info' no corresponde a una zona horaria válida.

    Example:
        >>> from datetime import datetime
        >>> # Convertir un timestamp a un datetime UTC
        >>> unix_timestamp_to_datetime(1718092025.0, tz_info='UTC')
        datetime.datetime(2025, 6, 11, 10, 27, 5, tzinfo=datetime.timezone.utc)

        >>> # Convertir a un datetime en la zona horaria de Madrid
        >>> madrid_dt = unix_timestamp_to_datetime(1718092025.0, tz_info='Europe/Madrid')
        >>> madrid_dt # Note the +02:00 offset for CEST
        datetime.datetime(2025, 6, 11, 12, 27, 5, tzinfo=zoneinfo.ZoneInfo(key='Europe/Madrid'))

        >>> # Convertir a un datetime naive (local time)
        >>> unix_timestamp_to_datetime(1718092025.0)
        datetime.datetime(2025, 6, 11, 12, 27, 5) # Output assumes local timezone is CEST+2 for this example
    """
    if not isinstance(timestamp, (int, float)):
        raise TypeError("'timestamp' must be an int or float.")
    
    target_tz = None
    if tz_info:
        try:
            import zoneinfo # Requires Python 3.9+
            target_tz = zoneinfo.ZoneInfo(tz_info)
        except ImportError:
            # Fallback for Python < 3.9 or if zoneinfo is not available
            print("Warning: 'zoneinfo' module not found. Timezone awareness might be limited.")
            from datetime import timedelta, tzinfo
            if tz_info.upper() == 'UTC':
                target_tz = timezone.utc
            else:
                # Basic timezone handling if zoneinfo not available (e.g., fixed offset)
                # This is a simplification; full TZ handling needs zoneinfo/pytz
                raise NotImplementedError("Specific timezone conversion without 'zoneinfo' is not fully implemented. Please install 'zoneinfo' or use Python 3.9+ for full timezone support.")
        except zoneinfo.ZoneInfoNotFoundError:
            raise ValueError(f"Invalid or unknown timezone: '{tz_info}'.")

    if target_tz:
        # fromtimestamp with tz argument available in Python 3.3+
        return datetime.fromtimestamp(timestamp, tz=target_tz)
    else:
        # If no tz_info, return a naive datetime from local timestamp
        return datetime.fromtimestamp(timestamp)


def to_js_safe_integer(number: Union[int, float]) -> Union[int, str]:
    """
    Convierte un número a un entero seguro para JavaScript.

    Si el número está dentro del rango seguro de enteros de JavaScript (-(2^53-1) a 2^53-1),
    se devuelve como un int de Python. Si excede este rango, se devuelve como una cadena
    para evitar la pérdida de precisión en JavaScript, lo que requerirá que JavaScript lo maneje
    como un BigInt u otra representación de número grande.

    Args:
        number (Union[int, float]): El número entero o flotante a convertir.
                                    Si es flotante, se truncará a entero antes de la comprobación.

    Returns:
        Union[int, str]: El número como un int si está dentro del rango seguro de JS,
                         o como una cadena si excede ese rango.

    Raises:
        TypeError: Si 'number' no es un int o float.

    Example:
        >>> to_js_safe_integer(100)
        100
        >>> to_js_safe_integer(9007199254740991) # JS_MAX_SAFE_INTEGER
        9007199254740991
        >>> to_js_safe_integer(9007199254740992) # JS_MAX_SAFE_INTEGER + 1
        '9007199254740992'
        >>> to_js_safe_integer(-9007199254740991) # JS_MIN_SAFE_INTEGER
        -9007199254740991
        >>> to_js_safe_integer(-9007199254740992) # JS_MIN_SAFE_INTEGER - 1
        '-9007199254740992'
        >>> to_js_safe_integer(3.14) # Flotantes se truncan a enteros
        3
        >>> to_js_safe_integer(9007199254740991.99)
        9007199254740991
    """
    if not isinstance(number, (int, float)):
        raise TypeError("'number' must be an int or float.")
    
    # Truncar flotantes a enteros para la comprobación
    num_int = int(number)

    if JS_MIN_SAFE_INTEGER <= num_int <= JS_MAX_SAFE_INTEGER:
        return num_int
    else:
        return str(num_int)


def convert_string_to_float_with_locale(number_string: str, target_locale: Optional[str] = None) -> float:
    """
    Convierte una cadena numérica a un flotante, interpretando los separadores decimales
    y de miles según una configuración regional (locale) específica.

    Problema/Necesidad del Usuario: Manejar la entrada de números desde diferentes regiones
    del mundo, donde el separador decimal y de miles puede variar (ej. ',' vs '.').

    Objetivos del Producto: Proporcionar una conversión robusta de cadenas numéricas
    a flotantes que respete los formatos regionales, evitando errores y facilitando
    la internacionalización de aplicaciones.

    Descripción: Esta función utiliza el módulo `locale` de Python. Opcionalmente,
    permite establecer un `target_locale` específico para la conversión. Si se
    proporciona `target_locale`, la función guarda el locale actual del sistema,
    establece temporalmente el nuevo locale, realiza la conversión con `locale.atof()`,
    y luego restaura el locale original. Si no se proporciona `target_locale`,
    la conversión se realiza con el locale actualmente configurado en el sistema.

    Args:
        number_string (str): La cadena que representa el número a convertir.
        target_locale (Optional[str]): El string del locale a usar para la conversión
                                       (ej. 'es_ES', 'de_DE', 'en_US'). Si es None,
                                       usa el locale actual del sistema.

    Returns:
        float: El número de punto flotante resultante.

    Raises:
        TypeError: Si 'number_string' no es una cadena.
        ValueError: Si la cadena no puede ser interpretada como un número válido
                    dentro del locale especificado, o si el locale no es válido.

    Example:
        >>> # Configuración para un locale que usa coma como decimal (ej. español de España)
        >>> convert_string_to_float_with_locale("1.234,56", 'es_ES')
        1234.56
        >>> convert_string_to_float_with_locale("123,45", 'es_ES')
        123.45

        >>> # Configuración para un locale que usa punto como decimal (ej. inglés de EE.UU.)
        >>> convert_string_to_float_with_locale("1,234.56", 'en_US')
        1234.56
        >>> convert_string_to_float_with_locale("123.45", 'en_US')
        123.45

        >>> # Usando el locale actual del sistema (puede variar según la configuración de tu OS)
        >>> # Para esta demostración, simularemos un locale 'es_ES' si no está configurado.
        >>> current_locale = locale.getlocale(locale.LC_NUMERIC) # Obtener el locale actual para LC_NUMERIC
        >>> try:
        >>>     # Intentar configurar a es_ES para el ejemplo si no está ya
        >>>     locale.setlocale(locale.LC_ALL, 'es_ES')
        >>>     print(f"Usando locale: {locale.getlocale(locale.LC_NUMERIC)}")
        >>>     print(f"'{1.234,56}' con locale actual (es_ES): {convert_string_to_float_with_locale('1.234,56')}")
        >>> finally:
        >>>     locale.setlocale(locale.LC_ALL, current_locale) # Restaurar el locale original

        >>> # Cadena no numérica (levantará ValueError)
        >>> try:
        >>>     convert_string_to_float_with_locale("abc", 'es_ES')
        >>> except ValueError as e:
        >>>     print(f"Error: {e}")
        # Salida esperada: Error: could not convert string to float: 'abc'
    """
    if not isinstance(number_string, str):
        raise TypeError("'number_string' must be a string.")

    original_locale = None
    try:
        # Guarda el locale actual para restaurarlo después
        original_locale = locale.getlocale(locale.LC_ALL)
        
        if target_locale:
            # Establece el locale temporalmente
            # locale.setlocale puede lanzar un locale.Error si el locale no es válido o no está instalado
            locale.setlocale(locale.LC_ALL, target_locale)
        else:
            # Asegúrate de que el locale numérico esté configurado, si no, usa el predeterminado del sistema
            locale.setlocale(locale.LC_ALL, '') # '' usa el locale predeterminado del usuario/sistema

        # Realiza la conversión usando locale.atof()
        return locale.atof(number_string)
    except locale.Error as e:
        raise ValueError(f"Could not set locale '{target_locale}'. Error: {e}. Check if the locale is installed on your system.")
    except ValueError as e:
        # Re-lanzar ValueError si la cadena no es un número válido en el locale especificado
        raise ValueError(f"Could not convert string '{number_string}' to float using locale '{target_locale or 'current'}'. Error: {e}")
    finally:
        # Asegura que el locale original siempre se restaure
        if original_locale:
            locale.setlocale(locale.LC_ALL, original_locale)


def safe_convert_number(value: Any, default_value: Union[int, float] = 0, target_type: type = float) -> Union[int, float]:
    """
    Convierte un valor de entrada a un tipo numérico (float o int) de forma segura,
    utilizando un patrón try-except para manejar errores y proporcionar un valor de fallback.

    Problema/Necesidad del Usuario: La entrada de datos de usuario o fuentes externas
    a menudo contiene valores que no se pueden convertir directamente a números,
    causando errores en el programa. Se necesita una manera de manejar estos casos
    graciosamente, proporcionando un valor por defecto.

    Objetivos del Producto: Ofrecer una función flexible y robusta para la conversión de tipos
    numéricos, que prevenga caídas del programa y mejore la resiliencia al procesar datos inciertos.

    Descripción: Esta función intenta convertir el `value` de entrada al `target_type` especificado
    (por defecto float). Si la conversión es exitosa, devuelve el valor convertido.
    Si la conversión falla (por ejemplo, si el valor es una cadena no numérica, None,
    o una cadena vacía), la función captura la excepción y devuelve el `default_value` proporcionado.
    Se puede especificar si el valor de fallback debe ser int o float, y también el tipo
    al que se intenta convertir (int o float).

    Args:
        value (Any): El valor de entrada a intentar convertir (puede ser str, int, float, None, etc.).
        default_value (Union[int, float]): El valor a devolver si la conversión falla.
                                          Por defecto es 0.
        target_type (type): El tipo numérico al que se desea convertir (int o float).
                            Por defecto es float.

    Returns:
        Union[int, float]: El valor convertido o el `default_value` si la conversión falla.

    Raises:
        ValueError: Si 'target_type' no es ni 'int' ni 'float'.

    Example:
        >>> # Conversión a float
        >>> safe_convert_number("3.14")
        3.14
        >>> safe_convert_number("10")
        10.0
        >>> safe_convert_number("abc")
        0.0
        >>> safe_convert_number("")
        0.0
        >>> safe_convert_number(None)
        0.0
        >>> safe_convert_number("hello", default_value=-1.0)
        -1.0

        >>> # Conversión a int
        >>> safe_convert_number("5", target_type=int)
        5
        >>> safe_convert_number("7.8", target_type=int)
        7
        >>> safe_convert_number("not_a_num", default_value=99, target_type=int)
        99
        >>> safe_convert_number(None, default_value=1, target_type=int)
        1
        >>> safe_convert_number(True, target_type=int) # Booleanos funcionan
        1
    """
    if target_type not in [int, float]:
        raise ValueError("target_type must be 'int' or 'float'.")

    try:
        # Intentar convertir el valor al tipo deseado
        return target_type(value)
    except (ValueError, TypeError):
        # Si la conversión falla, devolver el valor por defecto
        return default_value


def ieee754_hex_representation(numero: float) -> str:
    """
    Devuelve la representación hexadecimal de un número de punto flotante
    según el estándar IEEE 754.

    Este método muestra el valor IEEE real (binario subyacente) de un float,
    lo cual puede ser útil para depuración o para entender cómo se almacenan
    los números de punto flotante.

    Args:
        numero (float): El número de punto flotante del que se desea obtener
                        la representación hexadecimal.

    Returns:
        str: Una cadena que representa el valor IEEE 754 hexadecimal del número.
             El formato es '0x<mantisa>p<exponente>'.

    Ejemplo de uso:
    >>> ieee754_hex_representation(3.14)
    '0x1.91eb851eb851fp+1'
    >>> ieee754_hex_representation(0.5)
    '0x1.0p-1'
    >>> ieee754_hex_representation(1.0)
    '0x1.0p+0'
    >>> ieee754_hex_representation(-1.0)
    '-0x1.0p+0'
    >>> ieee754_hex_representation(float('inf'))
    'inf'
    >>> ieee754_hex_representation(float('-inf'))
    '-inf'
    >>> ieee754_hex_representation(float('nan'))
    'nan'
    """
    return numero.hex()


def int_a_bytes(numero_entero: int, num_bytes: int, byteorder: str = 'big') -> bytes:
    """
    Convierte un número entero a una secuencia de bytes.

    Útil para la transmisión de datos binarios, protocolos de comunicación
    o almacenamiento de datos en formatos binarios.

    Args:
        numero_entero (int): El número entero a convertir.
        num_bytes (int): El número de bytes deseado para la representación.
                         Debe ser suficiente para contener el entero.
        byteorder (str): El orden de los bytes ('big' para network byte order,
                         'little' para el orden inverso). Por defecto, 'big'.

    Returns:
        bytes: La representación en bytes del número entero.

    Raises:
        OverflowError: Si el entero es demasiado grande para el número de bytes especificado.

    Ejemplo de uso:
    >>> int_a_bytes(123, 2, byteorder='big')
    b'\x00{'
    >>> int_a_bytes(256, 2, byteorder='little')
    b'\x00\x01'
    >>> int_a_bytes(65535, 2, byteorder='big') # Max value for 2 bytes unsigned
    b'\xff\xff'
    """
    return numero_entero.to_bytes(num_bytes, byteorder=byteorder)


def bytes_a_int(secuencia_bytes: bytes, byteorder: str = 'big') -> int:
    """
    Convierte una secuencia de bytes a un número entero.

    Útil para decodificar datos recibidos a través de un protocolo binario
    o leer valores numéricos de archivos binarios.

    Args:
        secuencia_bytes (bytes): La secuencia de bytes a convertir.
        byteorder (str): El orden de los bytes ('big' para network byte order,
                         'little' para el orden inverso). Por defecto, 'big'.

    Returns:
        int: El número entero representado por la secuencia de bytes.

    Ejemplo de uso:
    >>> bytes_a_int(b'\x00{', 'big')
    123
    >>> bytes_a_int(b'\x00\x01', 'little')
    256
    >>> bytes_a_int(b'\xff\xff', 'big')
    65535
    """
    return int.from_bytes(secuencia_bytes, byteorder=byteorder)


def float_a_json_safe(numero_float: float) -> str:
    """
    Convierte un número de punto flotante a una representación segura para JSON.

    Los estándares JSON no admiten directamente valores como NaN (Not a Number)
    o Infinity. Esta función los convierte a su representación de cadena
    correspondiente ('NaN', 'Infinity', '-Infinity') antes de la serialización JSON,
    mientras que los números regulares se manejan como floats JSON estándar.

    Args:
        numero_float (float): El número de punto flotante de entrada.

    Returns:
        str: La representación del número como una cadena JSON válida.

    Ejemplo de uso:
    >>> float_a_json_safe(3.14)
    '3.14'
    >>> float_a_json_safe(float('nan'))
    '"NaN"'
    >>> float_a_json_safe(float('inf'))
    '"Infinity"'
    >>> float_a_json_safe(float('-inf'))
    '"-Infinity"'
    """
    if math.isnan(numero_float):
        # Convertir NaN a la cadena "NaN"
        return json.dumps(str(numero_float))
    elif math.isinf(numero_float):
        # Convertir Infinity a la cadena "Infinity" o "-Infinity"
        return json.dumps(str(numero_float))
    else:
        # Para números normales, dejar que json.dumps los maneje directamente
        # o convertirlos a Decimal primero para mayor precisión si se desea
        return json.dumps(numero_float)


def convert_bytes_to(unit: str, value: Union[int, float, str]) -> float:
    """Converts a byte value to a specified target unit.

    This function takes a byte value and converts it into a more readable
    unit (e.g., KB, MB, GB, KiB, MiB, GiB). It supports both SI (powers of 1000)
    and IEC (powers of 1024) units.

    Args:
        unit: The target unit for conversion (e.g., 'KB', 'MB', 'GB', 'TB',
              'PB' for SI units, or 'KiB', 'MiB', 'GiB', 'TiB', 'PiB' for IEC units).
        value: The byte value to convert. Can be an int, float, or a string
               that can be converted to a number.

    Returns:
        The converted value as a float.

    Raises:
        TypeError: If 'value' cannot be converted to a numeric type.
        ValueError: If 'unit' is not a recognized conversion unit.

    Example of use:
        >>> convert_bytes_to('KB', 1024)
        1.024
        >>> convert_bytes_to('GiB', 1073741824) # 1 GiB
        1.0
        >>> convert_bytes_to('GB', 1000000000) # 1 GB
        1.0
        >>> convert_bytes_to('MB', 5242880) # 5 MiB
        5.24288
        >>> convert_bytes_to('MiB', 5242880) # 5 MiB
        5.0
        >>> convert_bytes_to('TB', 2_000_000_000_000)
        2.0
        >>> convert_bytes_to('KiB', "2048")
        2.0
    """
    # Why: Attempt to convert the input value to a float.
    # This makes the function robust to string inputs that represent numbers.
    try:
        numeric_value = float(value)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Value '{value}' cannot be converted to a numeric type. Original error: {e}")

    # Why: Define conversion constants directly within the function scope.
    # While they could be global constants, keeping them here ensures all conversion
    # logic is self-contained.
    KIBI = 1024**1
    MEBI = 1024**2
    GIBI = 1024**3
    TEBI = 1024**4
    PEBI = 1024**5

    KILO = 1000**1
    MEGA = 1000**2
    GIGA = 1000**3
    TERA = 1000**4
    PETA = 1000**5

    # Why: Standardize the unit string for case-insensitive comparison.
    normalized_unit = unit.strip().upper()

    # Why: Use a dictionary for cleaner mapping of units to their respective divisors.
    # This avoids long if/elif chains and is easily extensible.
    conversion_factors = {
        'KB': KILO, 'MB': MEGA, 'GB': GIGA, 'TB': TERA, 'PB': PETA,
        'KIB': KIBI, 'MIB': MEBI, 'GIB': GIBI, 'TIB': TEBI, 'PIB': PIBI
    }

    # Why: Retrieve the appropriate divisor. If the unit is not found, raise a ValueError.
    divisor = conversion_factors.get(normalized_unit)
    if divisor is None:
        raise ValueError(
            f"Unsupported unit: '{unit}'. "
            f"Supported units are: {', '.join(conversion_factors.keys())}"
        )

    # Why: Perform the actual division to convert bytes to the target unit.
    return numeric_value / divisor


def number_to_hexadecimal(number_input: Union[int, float]) -> str:
    """
    Returns a string representing the hexadecimal value of a number.

    This function converts an integer or float to its hexadecimal string representation.
    For integers, it uses Python's built-in `hex()` function, which prefixes the
    output with '0x'. For floats, it first converts the float to an integer
    (by truncating its decimal part) before converting to hexadecimal.

    Args:
        number_input (Union[int, float]): The number to convert.

    Returns:
        str: A string representing the hexadecimal value, prefixed with '0x'.

    Raises:
        TypeError: If the input is not an integer or a float.
        ValueError: If the input number is too large to be converted to an integer
                    for hexadecimal representation (relevant for very large floats).

    Example of use:
        >>> number_to_hexadecimal(255)
        '0xff'
        >>> number_to_hexadecimal(10)
        '0xa'
        >>> number_to_hexadecimal(0)
        '0x0'
        >>> number_to_hexadecimal(25.75)
        '0x19'
        >>> number_to_hexadecimal(-10)
        '-0xa'
    """
    if not isinstance(number_input, (int, float)):
        raise TypeError("Input must be an integer or a float.")

    # Convert float to integer by truncating, as hexadecimal is typically for integers.
    # We maintain the sign before conversion and apply it back if needed.
    if isinstance(number_input, float):
        # We need to handle the sign before casting to int, as int() truncates towards zero.
        if number_input < 0:
            integer_part = int(abs(number_input))
            hex_value = hex(integer_part)
            return f"-{hex_value}"
        else:
            integer_part = int(number_input)
            return hex(integer_part)
    else: # It's an integer
        return hex(number_input)
    

def number_to_octal(number_input: Union[int, float]) -> str:
    """
    Returns a string representing the octal value of a number.

    This function converts an integer or float to its octal string representation.
    For integers, it uses Python's built-in `oct()` function, which prefixes the
    output with '0o'. For floats, it first converts the float to an integer
    (by truncating its decimal part) before converting to octal.

    Args:
        number_input (Union[int, float]): The number to convert.

    Returns:
        str: A string representing the octal value, prefixed with '0o'.

    Raises:
        TypeError: If the input is not an integer or a float.
        ValueError: If the input number is too large to be converted to an integer
                    for octal representation (relevant for very large floats).

    Example of use:
        >>> number_to_octal(8)
        '0o10'
        >>> number_to_octal(15)
        '0o17'
        >>> number_to_octal(0)
        '0o0'
        >>> number_to_octal(10.99)
        '0o12'
        >>> number_to_octal(-7)
        '-0o7'
    """
    if not isinstance(number_input, (int, float)):
        raise TypeError("Input must be an integer or a float.")

    # Convert float to integer by truncating, as octal is typically for integers.
    # We maintain the sign before conversion and apply it back if needed.
    if isinstance(number_input, float):
        # We need to handle the sign before casting to int, as int() truncates towards zero.
        if number_input < 0:
            integer_part = int(abs(number_input))
            octal_value = oct(integer_part)
            return f"-{octal_value}"
        else:
            integer_part = int(number_input)
            return oct(integer_part)
    else: # It's an integer
        return oct(number_input)
    

import math
from typing import Union

def power(base: Union[int, float], exponent: Union[int, float]) -> float:
    """
    Calculates the value of a base raised to a specified exponent (base^exponent).

    This function handles both positive and negative bases and exponents,
    returning a float. It uses the standard exponentiation operator `**`.

    Args:
        base (Union[int, float]): The base number.
        exponent (Union[int, float]): The exponent to which the base is raised.

    Returns:
        float: The result of base raised to the power of exponent.

    Raises:
        TypeError: If base or exponent are not numeric.
        ValueError: If a negative base is raised to a non-integer exponent
                    (which results in a complex number, not handled here),
                    or if 0 is raised to a negative or zero exponent.

    Example of use:
        >>> power(2, 3)
        8.0
        >>> power(9, 0.5) # Square root
        3.0
        >>> power(-2, 3)
        -8.0
        >>> power(10, -2)
        0.01
    """
    if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
        raise TypeError("Both base and exponent must be numeric values (int or float).")

    # Handle specific edge cases for 0 as base
    if base == 0:
        if exponent == 0:
            # 0^0 is typically defined as 1 in mathematics contexts (e.g., binomial theorem),
            # but Python's ** operator handles it correctly as 1.0.
            return 1.0
        elif exponent < 0:
            raise ValueError("0 cannot be raised to a negative power (results in division by zero).")
        else: # exponent > 0
            return 0.0

    # For negative base and non-integer exponent, the result is complex.
    # This function is designed for real-valued results.
    if base < 0 and exponent != int(exponent):
        raise ValueError("Cannot raise a negative base to a non-integer exponent; result is complex.")

    return float(base ** exponent)

def square_root(x: Union[int, float]) -> float:
    """
    Calculates the square root of a non-negative number.

    The square root function finds a number that, when multiplied by itself,
    equals the input number.

    Args:
        x (Union[int, float]): The number for which to calculate the square root. Must be non-negative.

    Returns:
        float: The square root of x.

    Raises:
        TypeError: If x is not numeric.
        ValueError: If x is negative.

    Example of use:
        >>> square_root(9)
        3.0
        >>> square_root(25.0)
        5.0
        >>> square_root(0)
        0.0
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Input 'x' must be a numeric value (int or float).")
    if x < 0:
        raise ValueError("Cannot calculate the square root of a negative number (results in a complex number).")

    return math.sqrt(x)

def cube_root(x: Union[int, float]) -> float:
    """
    Calculates the cube root of a number.

    The cube root function finds a number that, when multiplied by itself
    three times, equals the input number. It works for both positive and negative
    real numbers.

    Args:
        x (Union[int, float]): The number for which to calculate the cube root.

    Returns:
        float: The cube root of x.

    Raises:
        TypeError: If x is not numeric.

    Example of use:
        >>> cube_root(8)
        2.0
        >>> cube_root(27)
        3.0
        >>> cube_root(-8)
        -2.0
        >>> cube_root(0)
        0.0
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Input 'x' must be a numeric value (int or float).")

    # Using x**(1/3) directly can lead to complex numbers for negative x due to float precision
    # when 1/3 is not exact. math.cbrt is preferred for Python 3.11+.
    # For older versions, we can use a sign-aware power function.
    if hasattr(math, 'cbrt'): # Available from Python 3.11+
        return math.cbrt(x)
    else:
        # Fallback for older Python versions
        if x < 0:
            return -((-x)**(1/3))
        else:
            return x**(1/3)


def nth_root(x: Union[int, float], n: Union[int, float]) -> float:
    """
    Calculates the nth root of a number (x^(1/n)).

    This function generalizes the square and cube roots to any positive integer n.
    For negative x, n must be an odd integer to return a real result.

    Args:
        x (Union[int, float]): The number for which to calculate the root.
        n (Union[int, float]): The degree of the root (e.g., 2 for square root, 3 for cube root).
                                Must be a non-zero number. If x < 0, n must be an odd integer.

    Returns:
        float: The nth root of x.

    Raises:
        TypeError: If x or n are not numeric.
        ValueError: If n is 0, or if x is negative and n is an even number,
                    or if x is 0 and n is negative.

    Example of use:
        >>> nth_root(81, 4) # Fourth root of 81
        3.0
        >>> nth_root(1000, 3) # Cube root of 1000
        10.0
        >>> nth_root(-27, 3) # Cube root of -27
        -3.0
        >>> # nth_root(-16, 2) would raise ValueError (even root of negative number)
    """
    if not isinstance(x, (int, float)) or not isinstance(n, (int, float)):
        raise TypeError("Both x and n must be numeric values (int or float).")

    if n == 0:
        raise ValueError("The degree of the root (n) cannot be zero.")
    if x == 0 and n < 0:
        raise ValueError("Cannot calculate the root of 0 with a negative degree (results in division by zero).")

    # Handle negative x raised to an even root
    if x < 0 and n % 2 == 0:
        raise ValueError("Cannot calculate an even root of a negative number (results in a complex number).")

    # Calculate x^(1/n)
    # For negative x and odd n, directly using x**(1/n) works in Python.
    return float(x**(1/n))


