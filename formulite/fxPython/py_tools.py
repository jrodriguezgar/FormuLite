def set_key_value(p_key_columns, p_values):
    """Creates a dictionary by mapping key column names to their corresponding values.

    This function takes a string or list of key column names and a value or tuple of values,
    then combines them into a dictionary. It handles cases where p_key_columns is a
    comma-separated string or a list, ensuring that column names are properly cleaned.

    Args:
        p_key_columns (str or list): A comma-separated string of column names
                                     (e.g., "id,name") or a list of column names
                                     (e.g., ["id", "name"]).
        p_values (any or tuple): A single value or a tuple of values to be
                                 associated with the key columns.

    Returns:
        dict: A dictionary where keys are the column names and values are the
              corresponding input values. Returns None if inputs are empty or invalid.

    Raises:
        ValueError: If the number of key columns does not match the number of values.

    Example of use:
        >>> set_key_value("id,name", (1, "Alice"))
        {'id': 1, 'name': 'Alice'}
        >>> set_key_value(["product_id"], "P123")
        {'product_id': 'P123'}
    """
    # Validate inputs to ensure they are not empty.
    if not p_key_columns or not p_values:
        print("The request cannot be empty.")
        return None

    # Normalize key_columns into a list of strings.
    if isinstance(p_key_columns, str):
        # Ensure key_columns is a list, even for a single column string.
        # This simplifies subsequent processing by consistently working with a list.
        key_column_names = [col.strip() for col in p_key_columns.split(',') if col.strip()]
    elif isinstance(p_key_columns, list):
        # Clean any whitespace from list elements directly.
        key_column_names = [col.strip() for col in p_key_columns if col.strip()]
    else:
        # Handle unexpected types for p_key_columns gracefully.
        print("Invalid type for p_key_columns. Expected string or list.")
        return None

    # Normalize p_values into a tuple for consistent zipping.
    # We wrap single values in a tuple to allow iteration.
    values = p_values if isinstance(p_values, tuple) else (p_values,)

    # Ensure the number of keys matches the number of values to prevent errors during zipping.
    if len(key_column_names) != len(values):
        raise ValueError(
            f"The number of key columns ({len(key_column_names)}) "
            f"does not match the number of values ({len(values)})."
        )

    # Create the dictionary by zipping column names and values.
    # This is efficient and idiomatic Python for combining two lists into a dictionary.
    dict_keys = dict(zip(key_column_names, values))

    return dict_keys

