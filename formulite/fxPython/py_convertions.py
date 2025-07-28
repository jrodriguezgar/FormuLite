import json
from typing import Iterable, Callable, Any, Union, List, Tuple, Set, Dict, Tuple, Union, Type, Optional
from pydantic import BaseModel, Field, create_model

def replace_void(primary_value: Any, replacement_value: Any = 'NaN') -> Any:
    """Replaces empty or None values with a specified replacement value.

    Problem/User Need: When handling data, it's common to need to replace empty,
    None, or zero-length values with a default value to ensure data consistency.

    Args:
        primary_value (Any): The primary value to check.
        replacement_value (Any): The value to use if primary_value is empty/None.

    Returns:
        Any: replacement_value if primary_value is empty/None/zero-length,
             otherwise returns primary_value.

    Example:
        >>> replace_void("", "default")
        'default'
        >>> replace_void(None, 0)
        0
        >>> replace_void([], [1, 2, 3])
        [1, 2, 3]
        >>> replace_void("hello", "default")
        'hello'
        >>> replace_void(0, 42)
        0  # 0 is not considered void
        
    Cost:
        Time complexity: O(1) for most types
        Space complexity: O(1)
    """
    # Check for None first as it's the most common case
    if primary_value is None:
        return replacement_value
    
    # For strings, lists, tuples, sets, dicts - check if empty
    if isinstance(primary_value, (str, list, tuple, set, dict)):
        if len(primary_value) == 0:
            return replacement_value
            
    # Return original value if not void
    return primary_value


# --- JSON Conversions ---

def any_to_json_string(data: Any, indent: Union[int, None] = None) -> str:
    """Converts a Python object to a JSON string.

    This function serializes various Python objects (dictionaries, lists, strings, numbers,
    booleans, and None) into a JSON formatted string. It allows for optional indentation
    to improve readability of the output JSON.

    Args:
        data (Any): The Python object to convert.
        indent (Union[int, None]): The number of spaces to indent the JSON for readability.
                                   If `None`, the JSON output will be compact (no indentation or newlines).

    Returns:
        str: The resulting JSON string.

    Raises:
        TypeError: If the Python object is not JSON serializable (e.g., a `datetime` object directly).

    Example of use:
        >>> any_to_json_string({"name": "Alice", "age": 30}, indent=2)
        '{\n  "name": "Alice",\n  "age": 30\n}'
        >>> any_to_json_string(["apple", "banana"])
        '["apple", "banana"]'
    """
    try:
        # `ensure_ascii=False` allows non-ASCII characters (like 'ñ') to be encoded directly,
        # making the JSON more readable and often smaller for international data.
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except TypeError as e:
        # Re-raise the exception with a more helpful message, preserving the original traceback.
        raise TypeError(
            f"The object is not JSON serializable: {e}. "
            f"Ensure it contains only valid JSON types (dict, list, str, int, float, bool, None)."
        ) from e


def json_string_to_any(json_string: str) -> Any:
    """Converts a JSON string to a Python object.

    The outcome is typically a **dictionary** (if the JSON represents an object)
    or a **list** (if the JSON represents an array).

    Args:
        json_string (str): The JSON string to parse.

    Returns:
        Any: The resulting Python object.

    Raises:
        json.JSONDecodeError: If the input JSON string is invalid.

    Example of use:
        >>> json_string_to_any('{"name": "Bob", "city": "Madrid"}')
        {'name': 'Bob', 'city': 'Madrid'}
        >>> json_string_to_any('[10, 20, 30]')
        [10, 20, 30]
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        # Re-raise with a more specific error and keep the original traceback.
        raise json.JSONDecodeError(
            f"Invalid JSON string: {e.msg}", e.doc, e.pos
        ) from e


def convert_collection(
    data_collection: Union[List[Any], Tuple[Any, ...], Set[Any]],
    target_type: Type[Union[List, Tuple, Set]]
) -> Union[List[Any], Tuple[Any, ...], Set[Any]]:
    """Converts a list, tuple, or set to a specified target collection type.

    This function takes an input collection (list, tuple, or set) and converts
    it to the desired target type. It handles type conversions between these
    three common collection types.

    Args:
        data_collection (Union[List[Any], Tuple[Any, ...], Set[Any]]): The
            input collection to convert. It can be a list, tuple, or set.
        target_type (Type[Union[List, Tuple, Set]]): The desired type for the
            output collection. Must be list, tuple, or set.

    Returns:
        Union[List[Any], Tuple[Any, ...], Set[Any]]: The converted collection
            of the specified `target_type`.

    Raises:
        TypeError: If `data_collection` is not a list, tuple, or set, or if
            `target_type` is not list, tuple, or set.

    Examples of use:
        >>> convert_collection([1, 'a', 3.5], tuple)
        (1, 'a', 3.5)
        >>> convert_collection((1, 2, 2, 'a'), set)
        {1, 2, 'a'} # Order not guaranteed
        >>> convert_collection({'red', 'green', 'blue'}, list)
        ['green', 'blue', 'red'] # Order not guaranteed
        >>> convert_collection([1, 2, 3], list)
        [1, 2, 3]
    Cost:
        The cost of this function is O(n), where n is the number of elements
        in the input collection, due to the iteration required for conversion
        by built-in constructors (list(), tuple(), set()).
    """
    if not isinstance(data_collection, (list, tuple, set)):
        # Because we only support list, tuple, and set as input.
        raise TypeError("Input 'data_collection' must be a list, tuple, or set.")

    if target_type not in (list, tuple, set):
        # Because the target type must be one of the supported collection types.
        raise TypeError("Target 'target_type' must be list, tuple, or set.")

    # Perform the conversion based on the target_type.
    if target_type is list:
        return list(data_collection)
    elif target_type is tuple:
        return tuple(data_collection)
    elif target_type is set:
        return set(data_collection)


# --- Set Conversions ---

def set_to_string(input_set: Set[Any], separator: str = ' ', use_quotes: bool = False) -> Optional[str]:
    """Converts a given set to its string representation.

    This function takes a set and converts its elements into a single string,
    joined by a specified separator. Optionally, string elements can be wrapped
    in single quotes. The order of elements in the resulting string is not
    guaranteed, as sets are inherently unordered. Returns None if the input set is empty.

    Args:
        input_set: The set to be converted.
        separator: The string used to join the elements. Defaults to a single space.
        use_quotes: If True, wraps string elements in single quotes. Defaults to False.

    Returns:
        The string representation of the set, or None if the input set is empty.

    Raises:
        TypeError: If the input 'input_set' is not a set.

    Example of use:
        >>> set_to_string({'apple', 'banana'}, separator=', ', use_quotes=True) # Order may vary
        "'apple', 'banana'"

        >>> set_to_string({1, 2, 3}, separator='-') # Order may vary
        "1-2-3"

        >>> set_to_string(set())
        None
    """
    # Return None immediately if the set is empty, aligning with the return type.
    if not input_set:
        return None

    # Use a generator expression to convert each item to a string.
    # Conditionally add quotes if 'use_quotes' is True.
    # It's important to note that the order of elements in the string
    # will be arbitrary, as sets do not guarantee order.
    if use_quotes:
        string_elements = (f"'{str(item)}'" for item in input_set)
    else:
        string_elements = (str(item) for item in input_set)

    # Join the processed string elements using the specified separator.
    return separator.join(string_elements)


def set_to_list(input_set: Set[Any]) -> List[Any]:
    """Converts a given set into a list.

    This function takes a set as input and returns a new list containing
    all the elements from the set. The order of elements in the resulting
    list is not guaranteed, as sets are inherently unordered.

    Args:
        input_set: The set to be converted to a list.

    Returns:
        A list containing the elements from the input set.

    Raises:
        TypeError: If the input 'input_set' is not a set.

    Example of use:
        >>> set_to_list({1, 2, 3}) # Order may vary
        [1, 2, 3]

        >>> set_to_list({'apple', 'banana'}) # Order may vary
        ['banana', 'apple']

        >>> set_to_list(set())
        []
    """
    # The built-in list() constructor is the most Pythonic and efficient
    # way to convert any iterable (like a set) into a list.
    # It handles all cases, including empty sets, correctly.
    converted_list = list(input_set)

    return converted_list


def set_to_tuple(input_set: Set[Any]) -> Tuple[Any, ...]:
    """Converts a given set into a tuple.

    This function takes a set as input and returns a new tuple containing
    all the elements from the set. The order of elements in the resulting
    tuple is not guaranteed, as sets are inherently unordered.

    Args:
        input_set: The set to be converted to a tuple.

    Returns:
        A tuple containing the elements from the input set.

    Raises:
        TypeError: If the input 'input_set' is not a set.

    Example of use:
        >>> set_to_tuple({1, 2, 3}) # Order may vary
        (1, 2, 3)

        >>> set_to_tuple({'red', 'green', 'blue'}) # Order may vary
        ('blue', 'red', 'green')

        >>> set_to_tuple(set())
        ()
    """
    # The built-in tuple() constructor is the most Pythonic and efficient
    # way to convert any iterable (like a set) into a tuple.
    # It handles all cases, including empty sets, correctly.
    converted_tuple = tuple(input_set)

    return converted_tuple


# --- Tuple Conversions ---

def tuple_to_string(input_tuple: Tuple[Any, ...], separator: str = ' ', use_quotes: bool = False) -> Optional[str]:
    """Converts a given tuple to its string representation.

    This function takes a tuple and converts its elements into a single string,
    joined by a specified separator. Optionally, string elements can be wrapped
    in single quotes. Returns None if the input tuple is empty.

    Args:
        input_tuple: The tuple to be converted.
        separator: The string used to join the elements. Defaults to a single space.
        use_quotes: If True, wraps string elements in single quotes. Defaults to False.

    Returns:
        The string representation of the tuple, or None if the input tuple is empty.

    Raises:
        TypeError: If the input 'input_tuple' is not a tuple.

    Example of use:
        >>> tuple_to_string(('apple', 'banana', 'orange'), separator=', ', use_quotes=True)
        "'apple', 'banana', 'orange'"

        >>> tuple_to_string((1, 2, 3), separator='-')
        "1-2-3"

        >>> tuple_to_string(())
        None
    """
    # Return None immediately if the tuple is empty, aligning with the return type.
    if not input_tuple:
        return None

    # Use a generator expression to convert each item to a string.
    # Conditionally add quotes if 'use_quotes' is True.
    # This approach is concise and efficient, avoiding intermediate list creation.
    if use_quotes:
        string_elements = (f"'{str(item)}'" for item in input_tuple)
    else:
        string_elements = (str(item) for item in input_tuple)

    # Join the processed string elements using the specified separator.
    return separator.join(string_elements)


def tuple_to_list(input_tuple: Tuple[Any, ...]) -> List[Any]:
    """Converts a given tuple into a list.

    This function takes a tuple as input and returns a new list containing
    all the elements from the tuple, maintaining their original order.

    Args:
        input_tuple: The tuple to be converted to a list.

    Returns:
        A list containing the elements from the input tuple.

    Raises:
        TypeError: If the input 'input_tuple' is not a tuple.

    Example of use:
        >>> tuple_to_list((1, 2, 3, 4, 5))
        [1, 2, 3, 4, 5]

        >>> tuple_to_list(('red', 'green', 'blue'))
        ['red', 'green', 'blue']

        >>> tuple_to_list(())
        []
    """
    # The built-in list() constructor is the most Pythonic and efficient
    # way to convert any iterable (like a tuple) into a list.
    # It handles all cases, including empty tuples, correctly.
    converted_list = list(input_tuple)

    return converted_list


def tuple_to_set(input_tuple: Tuple[Any, ...]) -> Set[Any]:
    """Converts a given tuple into a set.

    This function takes a tuple as input and returns a new set containing
    all the unique elements from the tuple. The order of elements is not
    preserved in the resulting set.

    Args:
        input_tuple: The tuple to be converted to a set.

    Returns:
        A set containing the unique elements from the input tuple.

    Raises:
        TypeError: If the input 'input_tuple' is not a tuple.

    Example of use:
        >>> tuple_to_set((1, 2, 2, 3, 4, 4, 5))
        {1, 2, 3, 4, 5}

        >>> tuple_to_set(('apple', 'banana', 'apple'))
        {'apple', 'banana'}

        >>> tuple_to_set(())
        set()
    """
    # The built-in set() constructor is the most Pythonic and efficient
    # way to convert any iterable (like a tuple) into a set.
    # It automatically handles duplicate removal and provides O(N) average
    # time complexity for the conversion.
    unique_elements_set = set(input_tuple)

    return unique_elements_set


# --- List Conversions ---

def list_to_string(lst: List[Any], separator: str = ' ', use_quotes: bool = False) -> Optional[str]:
    """Converts a list to its string representation.

    This function takes a list and converts its elements into a single string,
    joined by a specified separator. Optionally, string elements can be wrapped in
    single quotes. Returns None if the input list is empty.

    Args:
        lst: The list to be converted.
        separator: The string used to join the elements. Defaults to a single space.
        use_quotes: If True, wraps string elements in single quotes. Defaults to False.

    Returns:
        The string representation of the list, or None if the input list is empty.

    Raises:
        TypeError: If the input 'lst' is not a list.

    Example of use:
        >>> list_to_string(['apple', 'banana', 'orange'], separator=', ', use_quotes=True)
        "'apple', 'banana', 'orange'"

        >>> list_to_string([1, 2, 3], separator='-')
        "1-2-3"

        >>> list_to_string([])
        None
    """
    # Return None immediately if the list is empty, aligning with the return type.
    if not lst:
        return None

    # Use a generator expression to convert each item to a string.
    # Conditionally add quotes if 'use_quotes' is True.
    # This approach is concise and efficient, avoiding intermediate list creation.
    if use_quotes:
        string_elements = (f"'{str(item)}'" for item in lst)
    else:
        string_elements = (str(item) for item in lst)

    # Join the processed string elements using the specified separator.
    return separator.join(string_elements)


def list_to_set(input_list: List[Any]) -> Set[Any]:
    """Converts a given list into a set.

    This function takes a list as input and returns a new set containing
    all the unique elements from the list. The order of elements is not
    preserved in the resulting set.

    Args:
        input_list: The list to be converted to a set.

    Returns:
        A set containing the unique elements from the input list.

    Raises:
        TypeError: If the input 'input_list' is not a list.

    Example of use:
        >>> list_to_set([1, 2, 2, 3, 4, 4, 5])
        {1, 2, 3, 4, 5}

        >>> list_to_set(['apple', 'banana', 'apple'])
        {'apple', 'banana'}

        >>> list_to_set([])
        set()
    """
    # Create a set from the input list. This automatically handles
    # duplicate removal and provides O(N) average time complexity.
    unique_elements_set = set(input_list)

    return unique_elements_set


def list_to_tuple(input_list: List[Any]) -> Tuple[Any, ...]:
    """Converts a given list into a tuple.

    This function takes a list as input and returns a new tuple containing
    all the elements from the list, maintaining their order.

    Args:
        input_list: The list to be converted to a tuple.

    Returns:
        A tuple containing the elements from the input list.

    Raises:
        TypeError: If the input 'input_list' is not a list.

    Example of use:
        >>> list_to_tuple([1, 2, 3, 4, 5])
        (1, 2, 3, 4, 5)

        >>> list_to_tuple(['apple', 'banana', 'cherry'])
        ('apple', 'banana', 'cherry')

        >>> list_to_tuple([])
        ()
    """
    # The built-in tuple() constructor is the most Pythonic and efficient
    # way to convert any iterable (like a list) into a tuple.
    # It handles all cases, including empty lists, correctly.
    converted_tuple = tuple(input_list)

    return converted_tuple


# --- Dictionary Conversions ---

def dict_keys_to_list(data_dict: Dict[Any, Any]) -> List[Any]:
    """Returns the keys of a dictionary as a list.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        List[Any]: A list containing all keys from the dictionary.

    Example of use:
        >>> dict_keys_to_list({"name": "Alice", "age": 30})
        ['name', 'age']
    """
    return list(data_dict.keys())


def dict_values_to_list(data_dict: Dict[Any, Any]) -> List[Any]:
    """Returns the values of a dictionary as a list.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        List[Any]: A list containing all values from the dictionary.

    Example of use:
        >>> dict_values_to_list({"item": "Laptop", "price": 1200})
        ['Laptop', 1200]
    """
    return list(data_dict.values())


def dict_items_to_list_of_tuples(data_dict: Dict[Any, Any]) -> List[Tuple[Any, Any]]:
    """Returns the key-value pairs (items) of a dictionary as a list of tuples.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        List[Tuple[Any, Any]]: A list where each element is a `(key, value)` tuple.

    Example of use:
        >>> dict_items_to_list_of_tuples({"city": "London", "population": 9000000})
        [('city', 'London'), ('population', 9000000)]
    """
    return list(data_dict.items())


def dict_keys_to_set(data_dict: Dict[Any, Any]) -> Set[Any]:
    """Returns the keys of a dictionary as a set.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        Set[Any]: A set containing all unique keys from the dictionary.

    Example of use:
        >>> dict_keys_to_set({"color": "red", "value": 50})
        {'color', 'value'} # Order not guaranteed
    """
    return set(data_dict.keys())


def dict_values_to_set(data_dict: Dict[Any, Any]) -> Set[Any]:
    """Returns the values of a dictionary as a set, which inherently removes duplicate values.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        Set[Any]: A set containing all unique values from the dictionary.

    Example of use:
        >>> dict_values_to_set({"a": 1, "b": 2, "c": 1})
        {1, 2} # Order not guaranteed
    """
    return set(data_dict.values())


def dict_items_to_set_of_tuples(data_dict: Dict[Any, Any]) -> Set[Tuple[Any, Any]]:
    """Returns the key-value pairs (items) of a dictionary as a set of tuples.

    Args:
        data_dict (Dict[Any, Any]): The input dictionary.

    Returns:
        Set[Tuple[Any, Any]]: A set where each element is a unique `(key, value)` tuple.

    Example of use:
        >>> dict_items_to_set_of_tuples({"id": 101, "status": "active"})
        {('id', 101), ('status', 'active')} # Order not guaranteed
    """
    return set(data_dict.items())


# --- List/Tuple to Dictionary Conversions ---

def list_of_tuples_to_dict(data_list: List[Tuple[Any, Any]]) -> Dict[Any, Any]:
    """Converts a list of tuples (where each tuple is a key-value pair) to a dictionary.

    If there are duplicate keys in the list, the value from the **last tuple**
    with that key will prevail.

    Args:
        data_list (List[Tuple[Any, Any]]): The input list of `(key, value)` tuples.

    Returns:
        Dict[Any, Any]: The converted dictionary.

    Example of use:
        >>> list_of_tuples_to_dict([("a", 1), ("b", 2), ("a", 3)])
        {'a': 3, 'b': 2}
    """
    return dict(data_list)


def list_of_lists_to_dict(data_list: List[List[Any]]) -> Dict[Any, Any]:
    """Converts a list of lists (where each inner list is a key-value pair) to a dictionary.

    If there are duplicate keys, the value from the **last inner list** with that key will prevail.

    Args:
        data_list (List[List[Any]]): The input list of `[key, value]` lists.

    Returns:
        Dict[Any, Any]: The converted dictionary.

    Example of use:
        >>> list_of_lists_to_dict([["name", "Bob"], ["age", 25], ["name", "Robert"]])
        {'name': 'Robert', 'age': 25}
    """
    # The `dict()` constructor also works directly with lists of lists like `[key, value]`.
    return dict(data_list)


def list_of_dicts_to_merged_dict(list_of_dicts: List[Dict[Any, Any]]) -> Dict[Any, Any]:
    """Merges a list of dictionaries into a single dictionary.

    If there are **duplicate keys** across the dictionaries, the value from the
    **last dictionary** in the list will take precedence.

    Args:
        list_of_dicts (List[Dict[Any, Any]]): A list of dictionaries to be merged.

    Returns:
        Dict[Any, Any]: The single merged dictionary.

    Example of use:
        >>> list_of_dicts_to_merged_dict([{"a": 1, "b": 2}, {"b": 3, "c": 4}, {"d": 5}])
        {'a': 1, 'b': 3, 'c': 4, 'd': 5}
    """
    merged_dict = {}
    # Iterate through each dictionary and update the `merged_dict`.
    # The `.update()` method adds new keys or overwrites existing keys from the current dictionary.
    for d in list_of_dicts:
        merged_dict.update(d)
    return merged_dict


def json_schema_to_pydantic_model(
    json_schema: Dict[str, Any], model_name: str = "DynamicModel"
) -> Type[BaseModel]:
    """
    Converts a JSON schema dictionary into a Pydantic BaseModel class.

    This function dynamically creates a Pydantic model based on the provided
    JSON schema, mapping schema properties to Pydantic fields. It supports
    basic types, nested objects, arrays, and common validation constraints.

    Args:
        json_schema (Dict[str, Any]): The JSON schema dictionary to convert.
                                       Must contain 'type': 'object' and 'properties'.
        model_name (str, optional): The name of the Pydantic model class to be created.
                                    Defaults to "DynamicModel".

    Returns:
        Type[BaseModel]: A Pydantic BaseModel class generated from the JSON schema.

    Raises:
        ValueError: If the 'json_schema' is not a dictionary, or if it's missing
                    'type' or 'properties' for an object schema.

    Example usage:
        >>> user_schema = {
        ...     "title": "User",
        ...     "description": "Schema for a user object",
        ...     "type": "object",
        ...     "properties": {
        ...         "name": {"type": "string", "minLength": 1, "description": "User's full name"},
        ...         "age": {"type": "integer", "minimum": 0, "maximum": 120, "description": "User's age"},
        ...         "email": {"type": "string", "format": "email", "pattern": "^.+@.+\\..+$"},
        ...         "is_active": {"type": "boolean", "default": True},
        ...         "address": {
        ...             "type": "object",
        ...             "properties": {
        ...                 "street": {"type": "string"},
        ...                 "city": {"type": "string"}
        ...             },
        ...             "required": ["street", "city"]
        ...         },
        ...         "tags": {
        ...             "type": "array",
        ...             "items": {"type": "string"}
        ...         },
        ...         "hobbies": {
        ...             "type": "array",
        ...             "items": {
        ...                 "type": "object",
        ...                 "properties": {
        ...                     "name": {"type": "string"},
        ...                     "difficulty": {"type": "integer", "minimum": 1, "maximum": 5}
        ...                 },
        ...                 "required": ["name", "difficulty"]
        ...             }
        ...         }
        ...     },
        ...     "required": ["name", "email"]
        ... }
        >>> User = json_schema_to_pydantic_model(user_schema, "User")
        >>> user_data = {
        ...     "name": "Alice Smith",
        ...     "age": 30,
        ...     "email": "alice@example.com",
        ...     "address": {"street": "123 Main St", "city": "Anytown"},
        ...     "tags": ["developer", "python"],
        ...     "hobbies": [{"name": "reading", "difficulty": 2}]
        ... }
        >>> user_instance = User(**user_data)
        >>> print(user_instance.name)
        Alice Smith
        >>> print(user_instance.is_active)
        True

    Cost:
        The cost of this function is primarily determined by the depth and number
        of properties in the JSON schema. In the worst case, for a schema with `N`
        properties and a maximum nesting depth of `D`, the complexity is roughly
        O(N*D) due to recursive calls for nested objects and array items.
    """
    if not isinstance(json_schema, dict):
        raise ValueError("Input 'json_schema' must be a dictionary.")
    if json_schema.get("type") != "object":
        raise ValueError(
            "The root of the JSON schema must have 'type': 'object' to be converted to a Pydantic model."
        )
    if "properties" not in json_schema:
        raise ValueError(
            "JSON schema for an object must contain a 'properties' key."
        )

    fields: Dict[str, Any] = {}
    required_fields: List[str] = json_schema.get("required", [])

    # Iterate through each property defined in the JSON schema.
    for prop_name, prop_schema in json_schema["properties"].items():
        field_type: Any = Any  # Default to Any if type is not specified or recognized
        pydantic_field_kwargs: Dict[str, Any] = {}

        # Determine the base Python type based on the JSON schema 'type'.
        json_type = prop_schema.get("type")

        if json_type == "string":
            field_type = str
            if "minLength" in prop_schema:
                pydantic_field_kwargs["min_length"] = prop_schema["minLength"]
            if "maxLength" in prop_schema:
                pydantic_field_kwargs["max_length"] = prop_schema["maxLength"]
            if "pattern" in prop_schema:
                pydantic_field_kwargs["pattern"] = prop_schema["pattern"]
            # 'format' like "email", "uri" are handled implicitly by Pydantic if type is str
            # and may require specific Pydantic types or validators, but for
            # basic conversion, str is sufficient.
        elif json_type == "integer":
            field_type = int
            if "minimum" in prop_schema:
                pydantic_field_kwargs["ge"] = prop_schema["minimum"]  # Greater than or equal
            if "maximum" in prop_schema:
                pydantic_field_kwargs["le"] = prop_schema["maximum"]  # Less than or equal
        elif json_type == "number":
            field_type = float  # Pydantic's 'number' maps to float
            if "minimum" in prop_schema:
                pydantic_field_kwargs["ge"] = prop_schema["minimum"]
            if "maximum" in prop_schema:
                pydantic_field_kwargs["le"] = prop_schema["maximum"]
        elif json_type == "boolean":
            field_type = bool
        elif json_type == "array":
            items_schema = prop_schema.get("items")
            if items_schema:
                if items_schema.get("type") == "object":
                    # Recursively create a model for complex array items
                    item_model_name = (
                        f"{model_name}{prop_name.replace('_', '').title()}Item"
                    )
                    field_type = List[
                        json_schema_to_pydantic_model(items_schema, item_model_name)
                    ]
                else:
                    # Map primitive array item types
                    primitive_item_type_map = {
                        "string": str,
                        "integer": int,
                        "number": float,
                        "boolean": bool,
                    }
                    item_type = primitive_item_type_map.get(
                        items_schema.get("type", ""), Any
                    )
                    field_type = List[item_type]
            else:
                field_type = List[Any]  # Default to list of Any if no items schema
        elif json_type == "object":
            # Recursively call the function to create a nested Pydantic model
            nested_model_name = f"{model_name}{prop_name.replace('_', '').title()}"
            field_type = json_schema_to_pydantic_model(
                prop_schema, nested_model_name
            )
        else:
            # For unsupported or unknown types, default to Any.
            # This allows the model to be created but provides less strict validation.
            field_type = Any

        # Add description if available
        if "description" in prop_schema:
            pydantic_field_kwargs["description"] = prop_schema["description"]

        # Add default value if available
        if "default" in prop_schema:
            pydantic_field_kwargs["default"] = prop_schema["default"]

        # Handle 'enum' by creating a Union of literals or simply checking against a set.
        # Pydantic Field doesn't directly support enum validation like this without
        # a dedicated Enum class or Literal types. For simplicity, we'll
        # just add the enum list to the Field metadata.
        # A more robust solution might dynamically create an Enum.
        if "enum" in prop_schema:
            pydantic_field_kwargs["json_schema_extra"] = {
                "enum": prop_schema["enum"]
            }

        # Determine if the field is required or optional
        is_required = prop_name in required_fields

        if pydantic_field_kwargs:
            # If there are any Pydantic Field arguments, use Field.
            # We use `Optional` for non-required fields that don't have a default.
            # If a default is provided, Pydantic handles optionality.
            if not is_required and "default" not in pydantic_field_kwargs:
                fields[prop_name] = (Optional[field_type], Field(None, **pydantic_field_kwargs))
            else:
                fields[prop_name] = (field_type, Field(**pydantic_field_kwargs))
        else:
            # If no special Pydantic Field arguments, simply assign the type.
            # Handle optionality.
            if not is_required:
                fields[prop_name] = (Optional[field_type], None) # None for Pydantic's default optional
            else:
                fields[prop_name] = field_type

    # Create the Pydantic model dynamically.
    model_class = create_model(
        model_name,
        __base__=BaseModel,
        __doc__=json_schema.get("description", f"Pydantic model generated from JSON schema for {model_name}."),
        **fields,
    )

    return model_class

