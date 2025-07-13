# Formulite

A Python library for high-level functions similar to Excel formulas. This library provides simple and efficient functions that mimic the behavior of Microsoft Excel formulas, making it easy to perform common data operations with minimal code.

## Features

- Excel-like functions for data manipulation
- Simple and intuitive API
- Built on top of NumPy and Pandas for performance
- Comprehensive test coverage

## Installation

```bash
pip install formulite
```

## Usage

```python
from formulite import math, text, lookup

# Math operations
result = math.sum_if([1, 2, 3, 4], ">2")  # Returns 7

# Text operations
result = text.concat("Hello", " ", "World")  # Returns "Hello World"

# Lookup operations
result = lookup.vlookup(value, table, col_index)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
