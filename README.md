# Formulite

A Python library for high-level functions following simplicity and doing one thing philosophy. This library provides simple and efficient functions that mimic the behavior of application formula languages (like Excel), making it easy to perform common data operations with minimal code.

## Features

### String Operations
- String manipulation and formatting with support for:
  - Case formatting (upper, lower, title, capitalization)
  - String similarity comparison using multiple algorithms
  - Pattern matching and validation
  - Text normalization and cleaning
  - Phone number and postal code extraction
  - Email address and domain validation/parsing
  - Company name formatting and parsing

### String Format Functions
- Date formatting with locale support
- Number formatting with locale and currency support
- Automatic type detection and formatting
- Special character handling and normalization
- Company name and legal form parsing
- URL and email address formatting

### String Evaluations
- Format validation for:
  - Email addresses
  - Domain names
  - URLs
  - NIF/VAT numbers (with focus on Spanish formats)
  - Date strings
- Text content analysis
  - Character type checking
  - String similarity metrics
  - Pattern matching

### Python Utilities
- General purpose Python helper functions
- Type checking and conversion utilities

## Installation

```bash
pip install formulite
```

## Usage

### Basic String Operations
```python
from formulite.fxString import string_operations as strops

# Replace occurrences in a string
result = strops.replace_string("Hello World", "World", "Python")
# Output: "Hello Python"

# Find common words between strings
common = strops.find_common_words("The quick brown fox", "A quick brown dog")
# Output: ['quick', 'brown']
```

### String Formatting
```python
from formulite.fxString import string_format as strfmt

# Format dates with locale support
date_str = strfmt.format_date("2023-12-31", output_format="%d/%m/%Y", locale="es_ES")
# Output: "31/12/2023"

# Format numbers with locale
num = strfmt.format_number(1234.56, decimal_places=2, locale="en_US", currency_symbol="$")
# Output: "$1,234.56"

# Format company names
company = strfmt.format_company_name("Acme Corp", "Ltd", format_style="brackets")
# Output: "Acme Corp (Ltd)"
```

### String Validation
```python
from formulite.fxString import string_evaluations as streval

# Validate email format
is_valid = streval.is_valid_email_format("user@example.com")
# Output: True

# Check domain format
is_valid = streval.is_valid_domain_format("example.com")
# Output: True

# Parse email components
parts = streval.parse_email("user@example.com")
# Output: {'username': 'user', 'domain': 'example.com'}
```

### String Similarity
```python
from formulite.fxString import string_grammar as strgrammar

# Compare string similarity
ws = strgrammar.WordSimilarity()
result = ws.are_words_effectively_the_same("color", "colour")
# Output: (True, {...similarity metrics...})

# Get similarity scores
scores = ws.compare("hello", "hallo")
# Output: Dictionary with various similarity metrics
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Make sure to follow these guidelines:
- Write clear commit messages
- Add tests for new functionality
- Update documentation
- Follow PEP 8 style guide

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- DatamanEdge
