from datetime import datetime, timedelta
import re
from typing import Union, Optional, List



def DIAS(end_date: datetime, start_date: datetime) -> int:
    """Devuelve la cantidad de días entre dos fechas."""
    return (end_date - start_date).days

def DIAS360(start_date: datetime, end_date: datetime, method: bool = False) -> int:
    """Calcula el número de días entre dos fechas a partir de un año de 360 días."""
    if method:  # European method
        day1 = min(start_date.day, 30)
        day2 = min(end_date.day, 30)
    else:  # US method
        day1 = start_date.day if start_date.day < 31 else 30
        day2 = end_date.day if end_date.day < 31 else 30
        if end_date.day == 31 and start_date.day >= 30:
            day2 = 30
    return (end_date.year - start_date.year) * 360 + (end_date.month - start_date.month) * 30 + (day2 - day1)

def DIAS_LAB(start_date: datetime, end_date: datetime, holidays: Optional[List[datetime]] = None) -> int:
    """Devuelve la cantidad de días laborables entre dos fechas."""
    holidays = holidays or []
    days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current not in holidays:
            days += 1
        current += timedelta(days=1)
    return days

def DIAS_LAB_INTL(start_date: datetime, end_date: datetime, weekend: Union[int, str] = 1, holidays: Optional[List[datetime]] = None) -> int:
    """Devuelve los días laborables entre dos fechas con parámetros de fin de semana."""
    holidays = holidays or []
    if isinstance(weekend, int):
        weekend_days = {1: {5, 6}, 2: {6, 0}, 3: {0, 1}, 4: {1, 2}, 5: {2, 3}, 6: {3, 4}, 7: {4, 5}}.get(weekend, {5, 6})
    else:
        weekend_days = {int(i) - 1 for i in weekend if i == '1'}
    
    days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() not in weekend_days and current not in holidays:
            days += 1
        current += timedelta(days=1)
    return days


def FECHA_MES(start_date: Union[datetime, float], months: int) -> float:
    """Devuelve el número de serie de una fecha meses antes o después."""
    if isinstance(start_date, (int, float)):
        start_date = datetime(1899, 12, 30) + timedelta(days=start_date)
    
    year = start_date.year + (start_date.month + months - 1) // 12
    month = (start_date.month + months - 1) % 12 + 1
    day = min(start_date.day, (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31)
    
    return FECHA(year, month, day)


def FIN_MES(start_date: Union[datetime, float], months: int) -> float:
    """Devuelve el número de serie del último día del mes."""
    if isinstance(start_date, (int, float)):
        start_date = datetime(1899, 12, 30) + timedelta(days=start_date)
    
    year = start_date.year + (start_date.month + months - 1) // 12
    month = (start_date.month + months - 1) % 12 + 1
    day = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    
    return FECHA(year, month, day)

def FRAC_AÑO(start_date: datetime, end_date: datetime, basis: int = 0) -> float:
    """Devuelve la fracción de año entre dos fechas."""
    days = DIAS(end_date, start_date)
    if basis == 0:  # US 30/360
        days = DIAS360(start_date, end_date)
        year_days = 360
    else:  # Actual/Actual
        year_days = 365.25 if start_date.year != end_date.year else (366 if start_date.year % 4 == 0 else 365)
    
    return days / year_days


def ISO_NUM_SEMANA(date: datetime) -> int:
    """Devuelve el número de semana ISO."""
    return date.isocalendar()[1]


def SIFECHA(start_date: datetime, end_date: datetime, unit: str) -> int:
    """Calcula la diferencia entre fechas en días, meses o años."""
    if unit == "Y":
        return end_date.year - start_date.year - (1 if (end_date.month, end_date.day) < (start_date.month, start_date.day) else 0)
    elif unit == "M":
        return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month - (1 if end_date.day < start_date.day else 0)
    else:  # D
        return (end_date - start_date).days

def VALOR_TIEMPO(time_text: str) -> float:
    """Convierte una hora en formato texto a número de serie."""
    t = datetime.strptime(time_text, "%H:%M:%S")
    return TIME(t.hour, t.minute, t.second)


def NUM_SEMANA(serial_number: Union[float, datetime], return_type: int = 1) -> int:
    """Convierte un número de serie en número de semana."""
    if isinstance(serial_number, float):
        dt = datetime(1899, 12, 30) + timedelta(days=serial_number)
    else:
        dt = serial_number
    if return_type == 21:
        return ISO_NUM_SEMANA(dt)
    return dt.isocalendar()[1]

def WORKDAY(start_date: Union[float, datetime], days: int, holidays: Optional[List[datetime]] = None) -> float:
    """Devuelve la fecha tras un número de días laborables."""
    holidays = holidays or []
    if isinstance(start_date, float):
        start_date = datetime(1899, 12, 30) + timedelta(days=start_date)
    
    count = 0
    current = start_date
    step = 1 if days >= 0 else -1
    days = abs(days)
    
    while count < days:
        current += timedelta(days=step)
        if current.weekday() < 5 and current not in holidays:
            count += 1
    
    return FECHA(current.year, current.month, current.day)

def WORKDAY_INTL(start_date: Union[float, datetime], days: int, weekend: Union[int, str] = 1, holidays: Optional[List[datetime]] = None) -> float:
    """Devuelve la fecha tras días laborables con fines de semana personalizados."""
    holidays = holidays or []
    if isinstance(start_date, float):
        start_date = datetime(1899, 12, 30) + timedelta(days=start_date)
    
    if isinstance(weekend, int):
        weekend_days = {1: {5, 6}, 2: {6, 0}, 3: {0, 1}, 4: {1, 2}, 5: {2, 3}, 6: {3, 4}, 7: {4, 5}}.get(weekend, {5, 6})
    else:
        weekend_days = {int(i) - 1 for i in weekend if i == '1'}
    
    count = 0
    current = start_date
    step = 1 if days >= 0 else -1
    days = abs(days)
    
    while count < days:
        current += timedelta(days=step)
        if current.weekday() not in weekend_days and current not in holidays:
            count += 1
    
    return FECHA(current.year, current.month, current.day)




def excel_serial_to_year(serial_number: Union[float, datetime]) -> int:
    """Extracts the year from an Excel-style serial number or a datetime object.
    equivalent to Excel's YEAR function.

    This function is equivalent to Excel's YEAR function. It takes a date
    represented as an Excel serial number (number of days since December 30, 1899)
    or a standard Python datetime object, and returns the corresponding year.

    Args:
        serial_number (Union[float, datetime]): The date value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.

    Returns:
        int: The year as an integer.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.

    Example:
        >>> excel_serial_to_year(44361.0) # Represents June 15, 2021
        2021
        >>> excel_serial_to_year(datetime(2023, 10, 26))
        2023
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_object = serial_number
    else:
        # Ensure that the input type is valid to prevent unexpected errors later.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Return the year component of the datetime object.
    return date_object.year


def excel_serial_to__month(serial_number: Union[float, datetime]) -> int:
    """Extracts the month from an Excel-style serial number or a datetime object.
    Equivalent to Excel's MONTH function.

    This function takes a date value, represented either as an Excel serial number
    (a float where the integer part denotes days since December 30, 1899) or a
    standard Python datetime object, and returns the corresponding month.

    Args:
        serial_number (Union[float, datetime]): The date value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.

    Returns:
        int: The month (1-12) as an integer.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.

    Example:
        >>> # Assuming serial_number 44361.0 corresponds to June 15, 2021
        >>> excel_serial_to__month(44361.0)
        6
        >>> excel_serial_to__month(datetime(2023, 10, 26))
        10
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_object = serial_number
    else:
        # Raise an error for invalid input types, ensuring robust behavior.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Return the month component of the datetime object.
    return date_object.month


def excel_serial_to_weekday(serial_number: Union[float, datetime], return_type: int = 1) -> int:
    """Converts a serial number or datetime object to the day of the week.
    Equivalent to Excel's WEEKDAY function.

    This function is equivalent to Excel's WEEKDAY function, returning an
    integer representing the day of the week. The behavior changes based on
    the `return_type` argument, mimicking Excel's options:

    - `return_type = 1` (default): Sunday = 1, Monday = 2, ..., Saturday = 7.
      (Excel's default)
    - `return_type = 2`: Monday = 1, Tuesday = 2, ..., Saturday = 6, Sunday = 7.
    - `return_type = 3`: Monday = 0, Tuesday = 1, ..., Saturday = 5, Sunday = 6.

    Args:
        serial_number (Union[float, datetime]): The date value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.
        return_type (int, optional): An integer specifying the return type.
                                      Defaults to 1. Valid values are 1, 2, or 3.

    Returns:
        int: The day of the week as an integer based on the `return_type`.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.
        ValueError: If 'return_type' is not 1, 2, or 3.

    Example:
        >>> # Assuming serial_number 44361.0 corresponds to Tuesday, June 15, 2021
        >>> excel_serial_to_weekday(44361.0, return_type=1)
        3
        >>> excel_serial_to_weekday(datetime(2023, 10, 26), return_type=2) # 2023-10-26 was a Thursday
        4
        >>> excel_serial_to_weekday(datetime(2023, 10, 29), return_type=3) # 2023-10-29 was a Sunday
        6
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_object = serial_number
    else:
        # Raise an error for invalid input types, ensuring robust behavior.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Get the weekday (Monday=0, Sunday=6) from the datetime object.
    # This is Python's default representation for weekday.
    weekday_index = date_object.weekday()

    # Adjust the weekday based on the specified return_type, mirroring Excel's behavior.
    if return_type == 1:
        # Excel Type 1: Sunday (0) = 1, Monday (1) = 2, ..., Saturday (6) = 7
        # Python's weekday_index starts from Monday=0, so add 1 to align.
        return weekday_index + 1
    elif return_type == 2:
        # Excel Type 2: Monday (0) = 1, Tuesday (1) = 2, ..., Sunday (6) = 7
        # If weekday_index is 6 (Sunday), return 7. Otherwise, add 1.
        return weekday_index + 2 if weekday_index < 6 else 1
    elif return_type == 3:
        # Excel Type 3: Monday (0) = 0, Tuesday (1) = 1, ..., Sunday (6) = 6
        # This directly matches Python's default weekday_index.
        return weekday_index
    else:
        # Raise an error for invalid return_type to ensure proper usage.
        raise ValueError("Invalid 'return_type'. Must be 1, 2, or 3.")
    

def excel_serial_to_day(serial_number: Union[int, float, datetime]) -> int:
    """Converts a serial number or datetime object into the day of the month.
    Equivalent to Excel's DAY function.

    This function is equivalent to the DAY function in Excel, extracting the day
    component from a given date representation. If a serial number (integer or float)
    is provided, it's treated as the number of days since '1899-12-30', which is
    Excel's epoch for date calculations.

    Args:
        serial_number (Union[int, float, datetime]): The date represented as an
                                                      Excel-like serial number
                                                      or a datetime object.

    Returns:
        int: The day of the month (1 to 31) for the given date.

    Raises:
        TypeError: If the input 'serial_number' is not an int, float, or datetime object.

    Example:
        >>> excel_serial_to_day(44361) # Equivalent to '2021-06-15'
        15
        >>> excel_serial_to_day(datetime(2023, 10, 26))
        26
    """
    # Convert Excel serial numbers to datetime objects.
    # Excel's epoch is '1899-12-30', so we add the serial number of days to this date.
    if isinstance(serial_number, (int, float)):
        date_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_object = serial_number
    else:
        # Raise an error to ensure type safety and clear usage.
        raise TypeError("Input 'serial_number' must be an int, float, or datetime object.")

    # Extract and return the day component from the datetime object.
    return date_object.day


def excel_serial_to_hour(serial_number: Union[float, datetime]) -> int:
    """Extracts the hour component from an Excel-style serial number or a datetime object.
    Equivalent to Excel's HOUR function.

    This function takes a date and/or time value, represented either as an
    Excel serial number (a float where the fractional part denotes time) or a
    standard Python datetime object, and returns the corresponding hour (0-23).

    Args:
        serial_number (Union[float, datetime]): The date/time value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.

    Returns:
        int: The hour (0-23) as an integer.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.

    Example:
        >>> # Assuming serial_number 44361.771354166667 represents 2021-06-15 18:30:45
        >>> excel_serial_to_hour(44361.771354166667)
        18
        >>> excel_serial_to_hour(datetime(2023, 10, 26, 9, 15, 30))
        9
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_time_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_time_object = serial_number
    else:
        # Raise an error for invalid input types, ensuring robust behavior.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Return the hour component of the datetime object.
    return date_time_object.hour


def excel_serial_to_minute(serial_number: Union[float, datetime]) -> int:
    """Extracts the minute component from an Excel-style serial number or a datetime object.
    Equivalent to Excel's MINUTE function.

    This function takes a date and/or time value, represented either as an
    Excel serial number (a float where the fractional part denotes time) or a
    standard Python datetime object, and returns the corresponding minute.

    Args:
        serial_number (Union[float, datetime]): The date/time value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.

    Returns:
        int: The minute (0-59) as an integer.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.

    Example:
        >>> # Assuming serial_number 44361.771354166667 represents 2021-06-15 18:30:45
        >>> excel_serial_to_minute(44361.771354166667)
        30
        >>> excel_serial_to_minute(datetime(2023, 10, 26, 15, 45, 10))
        45
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_time_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_time_object = serial_number
    else:
        # Raise an error for invalid input types, ensuring robust behavior.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Return the minute component of the datetime object.
    return date_time_object.minute


def excel_serial_to_second(serial_number: Union[float, datetime]) -> int:
    """Extracts the second component from an Excel-style serial number or a datetime object.
    Equivalent to Excel's SECOND function.

    This function takes a date and/or time value, represented either as an
    Excel serial number (a float where the fractional part denotes time) or a
    standard Python datetime object, and returns the corresponding second.

    Args:
        serial_number (Union[float, datetime]): The date/time value, either as an
                                                  Excel serial number (float) or
                                                  a datetime object.

    Returns:
        int: The second (0-59) as an integer.

    Raises:
        TypeError: If 'serial_number' is not a float or a datetime object.

    Example:
        >>> excel_serial_to_second(44361.771354166667) # Represents 2021-06-15 18:30:45
        45
        >>> excel_serial_to_second(datetime(2023, 10, 26, 15, 30, 10))
        10
    """
    # Convert Excel serial numbers to a datetime object.
    # Excel's date system effectively starts from December 30, 1899.
    if isinstance(serial_number, float):
        date_time_object = datetime(1899, 12, 30) + timedelta(days=serial_number)
    elif isinstance(serial_number, datetime):
        date_time_object = serial_number
    else:
        # Ensure the input type is valid to prevent unexpected errors.
        raise TypeError("Input 'serial_number' must be a float or a datetime object.")

    # Return the second component of the datetime object.
    return date_time_object.second


def int_date_to_excel_serial(year: int, month: int, day: int) -> float:
    """Converts a given date into its Excel serial number equivalent.
    Equivalent to Excel's DATE function.

    This function is analogous to the DATE function in Excel. Excel stores dates
    as serial numbers, representing the number of days since January 1, 1900
    (with an intentional error where 1900 is treated as a leap year, making
    December 30, 1899, the effective epoch for calculations).

    Args:
        year (int): The year of the date (e.g., 2023).
        month (int): The month of the date (1-12).
        day (int): The day of the month (1-31).

    Returns:
        float: The Excel serial number representing the date. This can include
               a fractional part if time components were considered (though this
               function only handles full days).

    Raises:
        ValueError: If the provided year, month, or day form an invalid date.

    Example:
        >>> int_date_to_excel_serial(2023, 10, 26)
        45227.0
        >>> int_date_to_excel_serial(1900, 1, 1) # Excel's day 1
        1.0
    """
    # Create a datetime object for the input date.
    # This will automatically raise a ValueError if the date is invalid (e.g., February 30).
    input_date = datetime(year, month, day)

    # Define Excel's epoch date.
    # Excel's date system starts effectively from December 30, 1899, due to how it handles leap years.
    excel_epoch = datetime(1899, 12, 30)

    # Calculate the difference in days.
    # The .days attribute gives the whole number of days.
    # The fractional part accounts for any time component, though here it will be 0
    # since we are only dealing with full days.
    time_difference = input_date - excel_epoch
    serial_number = time_difference.days + time_difference.seconds / 86400.0

    return serial_number


def date_to_excel_serial(date_input: Union[str, datetime]) -> float:
    """Converts a date, provided as a text string or a datetime object,
    into its Excel serial number equivalent.
    Equivalent to Excel's DATEVALUE function.

    This function is a versatile tool for converting dates into Excel's numerical
    representation. If a string is provided, it must be in the "DD/MM/YYYY" format.
    If a datetime object is provided, it's used directly. The Excel serial number
    represents the number of days since December 30, 1899, which is Excel's
    effective epoch for date calculations.

    Args:
        date_input (Union[str, datetime]): The date value to convert.
                                           Can be a string (e.g., "26/10/2023")
                                           or a datetime object (e.g., datetime(2023, 10, 26)).

    Returns:
        float: The Excel serial number representing the parsed date.

    Raises:
        ValueError: If 'date_input' is a string that does not match the expected
                    "DD/MM/YYYY" format or represents an invalid date.
        TypeError: If 'date_input' is neither a string nor a datetime object.

    Example:
        >>> date_to_excel_serial("15/06/2021")
        44361.0
        >>> from datetime import datetime
        >>> date_to_excel_serial(datetime(2023, 10, 26))
        45227.0
        >>> date_to_excel_serial("01/01/1900") # Excel's day 1
        1.0
    """
    # Define Excel's epoch date.
    # Excel's date system effectively starts from December 30, 1899.
    excel_epoch = datetime(1899, 12, 30)

    # Determine the type of the input and convert it to a datetime object.
    if isinstance(date_input, str):
        # If it's a string, parse it from the "DD/MM/YYYY" format.
        # This will raise a ValueError if the format is incorrect or the date is invalid.
        parsed_date = datetime.strptime(date_input, "%d/%m/%Y")
    elif isinstance(date_input, datetime):
        # If it's already a datetime object, use it directly.
        parsed_date = date_input
    else:
        # Raise an error for any other unsupported input types.
        raise TypeError("Input 'date_input' must be a string in 'DD/MM/YYYY' format or a datetime object.")

    # Calculate the difference in days from the Excel epoch.
    # The .days attribute gives the whole number of days.
    time_difference = parsed_date - excel_epoch
    serial_number = float(time_difference.days)

    return serial_number


def time_to_excel_serial(hour: int, minute: int, second: int) -> float:
    """Converts a given time into its Excel serial number equivalent.
    Equivalent to Excel's TIME function.

    This function is analogous to the TIME function in Excel. It takes
    hours, minutes, and seconds, and returns a serial number that
    represents the fraction of a 24-hour day that has elapsed. For instance,
    6:00 AM would be 0.25, 12:00 PM would be 0.5, and 6:00 PM would be 0.75.

    Args:
        hour (int): The hour component of the time (0-23).
        minute (int): The minute component of the time (0-59).
        second (int): The second component of the time (0-59).

    Returns:
        float: The Excel serial number representing the time as a fraction of a day.

    Raises:
        ValueError: If the provided hour, minute, or second are outside
                    their valid ranges.

    Example:
        >>> time_to_excel_serial(12, 0, 0) # 12:00 PM
        0.5
        >>> time_to_excel_serial(6, 0, 0)  # 6:00 AM
        0.25
        >>> time_to_excel_serial(18, 30, 45) # 6:30:45 PM
        0.7713541666666667
    """
    # Validate input ranges to ensure a meaningful time is being converted.
    if not (0 <= hour <= 23):
        raise ValueError("Hour must be between 0 and 23.")
    if not (0 <= minute <= 59):
        raise ValueError("Minute must be between 0 and 59.")
    if not (0 <= second <= 59):
        raise ValueError("Second must be between 0 and 59.")

    # Calculate the total number of seconds in the given time.
    # We multiply hours by 3600 (seconds in an hour) and minutes by 60 (seconds in a minute).
    total_seconds = (hour * 3600) + (minute * 60) + second

    # Divide by the total number of seconds in a day (24 hours * 60 minutes * 60 seconds)
    # to get the fractional part of the day.
    seconds_in_a_day = 86400.0
    serial_time = total_seconds / seconds_in_a_day

    return serial_time


def now_to_excel_serial() -> float:
    """Returns the current date and time as an Excel serial number.
    Eqivalent to Excel's NOW function.

    This function combines the current date and time (obtained using `datetime.now()`)
    and converts it into an Excel-compatible floating-point serial number.
    The integer part of the serial number represents the number of days since
    December 30, 1899 (Excel's epoch), and the fractional part represents
    the time as a proportion of a 24-hour day.

    Returns:
        float: The current date and time as an Excel serial number.

    Example:
        >>> # The exact output will vary depending on when the function is called.
        >>> # Example output if called on June 10, 2025, at 9:15:13 PM
        >>> now_to_excel_serial()
        45811.88552199074
    """
    # Get the current local date and time.
    current_datetime = datetime.now()

    # Define Excel's epoch date.
    # Excel's date system effectively starts from December 30, 1899.
    excel_epoch = datetime(1899, 12, 30)

    # Calculate the total difference in days and seconds from the epoch.
    time_difference = current_datetime - excel_epoch

    # Convert the timedelta to an Excel serial number.
    # The .days attribute gives the whole number of days.
    # The .seconds attribute gives the number of seconds in the time component,
    # which is then divided by the total seconds in a day (86400.0) to get the fractional part.
    total_seconds_in_day = 86400.0
    excel_serial = time_difference.days + (time_difference.seconds / total_seconds_in_a_day)

    return excel_serial