import math
from typing import Union

def natural_log(x: float) -> float:
    """
    Calculates the natural logarithm (base e) of a number.
    Log_e(X) or ln(X).

    Args:
        x (float): The number for which to calculate the natural logarithm. Must be positive.

    Returns:
        float: The natural logarithm of x.

    Raises:
        TypeError: If x is not numeric.
        ValueError: If x is not positive.

    Example of use:
        >>> natural_log(math.e)
        1.0
        >>> round(natural_log(1), 10)
        0.0
        >>> round(natural_log(10), 10)
        2.302585093
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Input 'x' must be a numeric value (int or float).")
    if x <= 0:
        raise ValueError("Domain error: The number (x) for natural logarithm must be positive.")

    return math.log(x)

def common_log(x: float) -> float:
    """
    Calculates the common logarithm (base 10) of a number.
    Log_10(X) or lg(X).

    Args:
        x (float): The number for which to calculate the common logarithm. Must be positive.

    Returns:
        float: The common logarithm of x.

    Raises:
        TypeError: If x is not numeric.
        ValueError: If x is not positive.

    Example of use:
        >>> common_log(10)
        1.0
        >>> round(common_log(100), 10)
        2.0
        >>> round(common_log(1), 10)
        0.0
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Input 'x' must be a numeric value (int or float).")
    if x <= 0:
        raise ValueError("Domain error: The number (x) for common logarithm must be positive.")

    return math.log10(x)

def log_base_n(x: float, base: Union[int, float]) -> float:
    """
    Calculates the logarithm of a number to a specified base N.
    LogN(X) = Log(X) / Log(N) where Log is the natural logarithm (base e).

    Args:
        x (float): The number for which to calculate the logarithm. Must be positive.
        base (Union[int, float]): The base of the logarithm. Must be positive and not 1.

    Returns:
        float: The logarithm of x to the given base.

    Raises:
        TypeError: If x or base are not numeric.
        ValueError: If x is not positive, base is not positive, or base is 1.

    Example of use:
        >>> log_base_n(100, 10)
        2.0
        >>> round(log_base_n(8, 2), 10)
        3.0
        >>> round(log_base_n(math.e, 10), 10)
        0.4342944819
    """
    if not isinstance(x, (int, float)) or not isinstance(base, (int, float)):
        raise TypeError("Both x and base must be numeric values (int or float).")
    if x <= 0:
        raise ValueError("Domain error: The number (x) for logarithm must be positive.")
    if base <= 0:
        raise ValueError("Domain error: The base for logarithm must be positive.")
    if base == 1:
        raise ValueError("Domain error: The base for logarithm cannot be 1.")

    return math.log(x) / math.log(base)

def log1p(x: float) -> float:
    """
    Calculates the natural logarithm of (1 + x).
    This function is designed to provide high precision for x values close to zero,
    where `log(1 + x)` might lose precision due to floating-point arithmetic.

    Args:
        x (float): The number for which to calculate log(1 + x). Must be greater than -1.

    Returns:
        float: The natural logarithm of (1 + x).

    Raises:
        TypeError: If x is not numeric.
        ValueError: If x is less than or equal to -1.

    Example of use:
        >>> round(log1p(0), 10)
        0.0
        >>> # For small x, log1p(x) is more accurate than log(1+x)
        >>> small_x = 1e-9
        >>> round(math.log(1 + small_x), 15)
        0.000000001000000
        >>> round(log1p(small_x), 15)
        0.000000001000000 # More precise for very small x
    """
    if not isinstance(x, (int, float)):
        raise TypeError("Input 'x' must be a numeric value (int or float).")
    if x <= -1:
        raise ValueError("Domain error: x must be greater than -1 for log(1 + x).")

    return math.log1p(x)


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

