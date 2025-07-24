from datetime import datetime, timedelta
from typing import Union, Optional
import calendar
import zoneinfo

#import date_operations as date_ops
from . import date_operations as date_ops

def current_datetime() -> datetime:
    """Gets the current local date and time.

    Returns:
        datetime: A datetime object representing the current local date and time.

    Example:
        >>> get_current_datetime = current_datetime()
        >>> print(get_current_datetime.strftime('%Y-%m-%d %H:%M:%S')) # Output will vary
        2025-06-10 21:46:04
    """
    # The datetime.now() method returns the current local date and time.
    return datetime.now()


def current_date() -> datetime:
    """Gets the current local date (without the time component).

    Returns:
        datetime: A datetime object representing the current local date.

    Example:
        >>> get_current_date = current_date()
        >>> print(get_current_date.strftime('%Y-%m-%d')) # Output will vary
        2025-06-10
    """
    # We get the current datetime and then extract only the date part using .date().
    # To return a datetime object, we reconstruct it with time components set to zero.
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def current_time() -> datetime:
    """Gets the current local time (without the date component).

    Returns:
        datetime: A datetime object representing the current local time.

    Example:
        >>> get_current_time = current_time()
        >>> print(get_current_time.strftime('%H:%M:%S')) # Output will vary
        21:46:04
    """
    # We get the current datetime and then extract only the time part using .time().
    # To return a datetime object with only time information, we use a default date.
    return datetime.combine(datetime.min.date(), datetime.now().time())


def current_year() -> int:
    """Gets the current year.

    Returns:
        int: The current year as an integer.

    Example:
        >>> get_current_year = current_year()
        >>> print(get_current_year) # Output will vary
        2025
    """
    # Extract the year attribute from the current datetime.
    return datetime.now().year


def current_month() -> int:
    """Gets the current month (1-12).

    Returns:
        int: The current month as an integer (1 for January, 12 for December).

    Example:
        >>> get_current_month = current_month()
        >>> print(get_current_month) # Output will vary
        6
    """
    # Extract the month attribute from the current datetime.
    return datetime.now().month


def current_day() -> int:
    """Gets the current day of the month (1-31).

    Returns:
        int: The current day of the month as an integer.

    Example:
        >>> get_current_day = current_day()
        >>> print(get_current_day) # Output will vary
        10
    """
    # Extract the day attribute from the current datetime.
    return datetime.now().day


def current_weekday_number(start_day: str = 'european') -> int:
    """
    Retrieves the current day of the week as a number, allowing for
    either European (Monday=0) or US (Sunday=0) conventions.

    This function utilizes `datetime.now().weekday()` to get the current
    day, which inherently follows the European standard (Monday=0, Sunday=6).
    If the 'us' convention is chosen, the result is adjusted so that Sunday is 0.

    Args:
        start_day (str): Specifies the desired starting day convention.
                         Accepted values are 'european' (Monday=0) or 'us' (Sunday=0).
                         Defaults to 'european'.

    Returns:
        int: The current day of the week as an integer (e.g., 0 for Monday in 'european',
             0 for Sunday in 'us').

    Raises:
        ValueError: If 'start_day' is not 'european' or 'us'.

    Example:
        >>> current_weekday_number(start_day='european') # Output will vary based on current day
        2 # If today is Wednesday
        >>> current_weekday_number(start_day='us') # Output will vary based on current day
        3 # If today is Wednesday (in US convention)
    """
    if start_day not in ['european', 'us']:
        raise ValueError("Invalid value for 'start_day'. Must be 'european' or 'us'.")

    # Get the current weekday using the default datetime.weekday() method,
    # which returns Monday=0, ..., Sunday=6 (European standard).
    current_weekday_index = datetime.now().weekday()

    # If the US convention is requested, adjust the index.
    # The US convention starts with Sunday as 0. Since Python's weekday()
    # returns Sunday as 6, we shift it to 0 by adding 1 and taking modulo 7.
    if start_day == 'us':
        return (current_weekday_index + 1) % 7
    return current_weekday_index


def current_weekday_name(language: str = 'en') -> str:
    """Gets the current weekday name for the current date.

    Args:
        language (str, optional): The language for the weekday name.
                                  Supports 'en' (English) and 'es' (Spanish).
                                  Defaults to 'en'.

    Returns:
        str: The name of the current day of the week.

    Example:
        >>> current_weekday_name('en')
        'Thursday'
        >>> current_weekday_name('es')
        'Jueves'
    """
    return date_ops.weekday_name(datetime.now(), language)




def current_last_day_of_month() -> datetime:
    """Gets the last day of the current month.

    Returns:
        datetime: A datetime object representing the last day of the current month.

    Example:
        >>> current_last_day_of_month()
        datetime.datetime(2023, 10, 31, 0, 0)
    """
    return date_ops.last_day_of_month(datetime.now())


def current_last_friday_of_month() -> datetime:
    """Gets the last Friday of the current month.

    Returns:
        datetime: A datetime object representing the last Friday of the current month.

    Example:
        >>> current_last_friday_of_month()
        datetime.datetime(2023, 10, 27, 0, 0)
    """
    return date_ops.last_weekday_of_month(datetime.now(), calendar.FRIDAY)


def current_next_friday() -> datetime:
    """Gets the next Friday after the current date.

    Returns:
        datetime: A datetime object representing the next Friday after today.

    Example:
        >>> current_next_friday()
        datetime.datetime(2023, 10, 13, 0, 0)
    """
    return date_ops.next_weekday(datetime.now(), calendar.FRIDAY)


def current_previous_friday() -> datetime:
    """Gets the previous Friday before the current date.

    Returns:
        datetime: A datetime object representing the previous Friday before today.

    Example:
        >>> current_previous_friday()
        datetime.datetime(2023, 10, 6, 0, 0)
    """
    return date_ops.previous_weekday(datetime.now(), calendar.FRIDAY)


def current_is_working_day() -> bool:
    """Checks if the current date is a working day (Monday to Friday).

    Returns:
        bool: True if the current date is a working day, False otherwise.

    Example:
        >>> current_is_working_day()
        True
    """
    return date_ops.is_working_day(datetime.now())


def current_is_weekend() -> bool:
    """Checks if the current date is a weekend (Saturday or Sunday).

    Returns:
        bool: True if the current date is a weekend, False otherwise.

    Example:
        >>> is_weekend = current_is_weekend()
        >>> print(is_weekend) # Output will vary
        False
    """
    return date_ops.is_weekend(datetime.now())


def get_local_now(tz: Optional[str] = None) -> datetime:
    """Obtiene la fecha y hora actuales, localizadas en la zona horaria especificada.

    Problema/Necesidad del Usuario: Obtener la fecha y hora actuales en una zona horaria
    específica (no solo la del sistema) es una necesidad frecuente para logging,
    sellos de tiempo de eventos o visualización localizada.

    Objetivos del Producto: Proporcionar una forma directa de obtener la hora actual
    en cualquier zona horaria deseada, simplificando la gestión de la hora local
    en aplicaciones globales.

    Descripción: Esta función devuelve un objeto `datetime` consciente de la zona horaria,
    representando la hora actual en la zona horaria indicada por 'tz'.
    Si 'tz' es `None`, la función devuelve la hora actual en la zona horaria configurada
    en el sistema local.
    Las zonas horarias deben especificarse utilizando los nombres de la base de datos IANA
    (ej., 'America/New_York', 'Europe/Madrid', 'Asia/Tokyo').

    Args:
        tz (str, optional): Nombre de la zona horaria IANA (ej. 'America/New_York').
                            Si es `None`, se usará la zona horaria del sistema.

    Returns:
        datetime: Un objeto `datetime` consciente de la zona horaria actual,
                  localizado en la zona horaria especificada o del sistema.

    Raises:
        TypeError: Si 'tz' no es una cadena cuando se proporciona.
        ValueError: Si la cadena 'tz' no es un nombre de zona horaria IANA válido o conocido.
        zoneinfo.ZoneInfoNotFoundError: (Aunque se captura y se convierte a ValueError)
                                        Si la zona horaria especificada no es encontrada.

    Example:
        >>> from datetime import datetime
        >>> # Para este ejemplo, asumiremos que la zona horaria local del sistema
        >>> # está configurada en 'Europe/Madrid', y la fecha/hora actual es
        >>> # 2025-06-11 02:04:10 CEST.

        >>> # Ejemplo 1: Hora actual en Tokio
        >>> tokyo_now = get_local_now('Asia/Tokyo')
        >>> print(f"Hora actual en Tokio: {tokyo_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
        # Salida esperada (aproximada para la hora de Madrid): Hora actual en Tokio: 2025-06-11 09:04:10 JST+0900

        >>> # Ejemplo 2: Hora actual en la zona horaria del sistema (ej. Madrid)
        >>> madrid_now = get_local_now()
        >>> print(f"Hora actual en Madrid: {madrid_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
        # Salida esperada: Hora actual en Madrid: 2025-06-11 02:04:10 CEST+0200

        >>> # Ejemplo 3: Hora actual en Nueva York
        >>> ny_now = get_local_now('America/New_York')
        >>> print(f"Hora actual en Nueva York: {ny_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
        # Salida esperada: Hora actual en Nueva York: 2025-06-10 20:04:10 EDT-0400

        >>> # Ejemplo 4: Zona horaria inválida (levantará ValueError)
        >>> try:
        >>>     get_local_now('Invalid/Zone')
        >>> except ValueError as e:
        >>>     print(f"Error: {e}")
        # Salida esperada: Error: Invalid or unknown timezone: 'Invalid/Zone'.
    """
    if tz is None:
        # Si no se especifica una zona horaria, se devuelve la hora actual
        # localizada en la zona horaria del sistema.
        return datetime.now().astimezone()
    else:
        # Si se especifica una zona horaria, se valida y se usa.
        if not isinstance(tz, str):
            raise TypeError("Input 'tz' must be a string representing a timezone.")
        try:
            # Cargar la información de la zona horaria IANA.
            target_tz_info = zoneinfo.ZoneInfo(tz)
            
            # Obtener la hora UTC actual. Es el punto de partida más seguro para conversiones.
            # Se usa zoneinfo.ZoneInfo('UTC') para consistencia.
            utc_now = datetime.now(zoneinfo.ZoneInfo('UTC'))
            
            # Convertir la hora UTC a la zona horaria objetivo.
            return utc_now.astimezone(target_tz_info)
        except zoneinfo.ZoneInfoNotFoundError:
            # Capturar errores si el nombre de la zona horaria no es válido.
            raise ValueError(f"Invalid or unknown timezone: '{tz}'.")
        except Exception as e:
            # Capturar cualquier otro error inesperado.
            raise RuntimeError(f"An unexpected error occurred while getting local time for timezone '{tz}': {e}")