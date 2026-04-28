# MCP Server

The Model Context Protocol (MCP) server allows AI agents to discover and execute any shortfx function as a tool.

## Installation

```bash
# MCP support only
pip install shortfx[mcp]

# MCP + semantic search (recommended)
pip install shortfx[mcp-semantic]
```

## Client Configuration

### VS Code (GitHub Copilot)

Add to your VS Code `settings.json` or `.vscode/mcp.json`:

```json
{
  "servers": {
    "shortfx": {
      "command": "shortfx-mcp",
      "args": []
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shortfx": {
      "command": "shortfx-mcp",
      "args": []
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "shortfx": {
      "command": "shortfx-mcp",
      "args": []
    }
  }
}
```

## Available Meta-Tools

| Tool | Description |
|------|-------------|
| `search_shortfx_tools` | Natural-language search across all functions |
| `list_shortfx_tools` | List functions by module (with optional filter) |
| `get_shortfx_tool_details` | Get JSON Schema for a specific function |
| `call_shortfx` | Execute a function by qualified name with JSON arguments |
| `scientific_calculate` | Evaluate a math expression (AST-based, safe) |

---

## Tool Usage Guide

### `search_shortfx_tools`

Find functions by natural-language query. Uses **semantic search** (when `fastembed` is installed) to match by intent, not just keywords. Falls back to substring matching otherwise.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language query or keyword |

**Example call:**

```json
{
  "tool": "search_shortfx_tools",
  "arguments": {
    "query": "convert temperature from celsius to fahrenheit"
  }
}
```

**Example response:**

```json
[
  {
    "name": "fxNumeric.conversion_functions.celsius_to_fahrenheit",
    "description": "Convert a temperature from Celsius to Fahrenheit.",
    "parameters": {
      "type": "object",
      "properties": {
        "celsius": {"type": "number", "description": "Temperature in Celsius"}
      },
      "required": ["celsius"]
    }
  }
]
```

---

### `list_shortfx_tools`

Browse all available functions, optionally filtered by module or submodule prefix.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `module` | string | No | Module prefix to filter results. Valid: `fxDate`, `fxNumeric`, `fxString`, `fxPython`, `fxExcel`, `fxVBA`. Supports submodule filtering (e.g. `fxExcel.math`). Leave empty for all. |

**Example calls:**

```json
// List all functions in fxExcel
{
  "tool": "list_shortfx_tools",
  "arguments": {
    "module": "fxExcel"
  }
}

// List only math-related Excel formulas
{
  "tool": "list_shortfx_tools",
  "arguments": {
    "module": "fxExcel.math"
  }
}

// List everything (no filter)
{
  "tool": "list_shortfx_tools",
  "arguments": {}
}
```

**Example response:**

```json
[
  {"name": "fxExcel.math_formulas.ABS", "description": "Returns the absolute value of a number."},
  {"name": "fxExcel.math_formulas.ROUND", "description": "Rounds a number to a specified number of digits."},
  {"name": "fxExcel.math_formulas.SUM", "description": "Adds all numbers in a range."}
]
```

---

### `get_shortfx_tool_details`

Get the full parameter schema for a specific function. Use this **before calling** a function to understand its exact argument names, types, and defaults.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tool_name` | string | Yes | Full qualified name of the function (format: `module.file.function`) |

**Example call:**

```json
{
  "tool": "get_shortfx_tool_details",
  "arguments": {
    "tool_name": "fxExcel.lookup_formulas.VLOOKUP"
  }
}
```

**Example response:**

```json
{
  "name": "fxExcel.lookup_formulas.VLOOKUP",
  "description": "Searches for a value in the first column of a table and returns a value in the same row from another column.",
  "parameters": {
    "type": "object",
    "properties": {
      "lookup_value": {"type": "string", "description": "The value to search for"},
      "table_array": {"type": "array", "description": "The table of data"},
      "col_index_num": {"type": "integer", "description": "Column number to return from"},
      "range_lookup": {"type": "boolean", "description": "True for approximate match, False for exact", "default": true}
    },
    "required": ["lookup_value", "table_array", "col_index_num"]
  }
}
```

**Error response (function not found):**

```json
{"error": "Tool 'fxExcel.invalid_name' not found."}
```

---

## Recommended Workflow

The recommended pattern for AI agents is **Search → Inspect → Execute**:

```
1. SEARCH   → search_shortfx_tools("calculate days between two dates")
2. INSPECT  → get_shortfx_tool_details("fxDate.date_operations.calculate_days_between_dates")
3. EXECUTE  → call_shortfx("fxDate.date_operations.calculate_days_between_dates",
                             '{"start_date": "2025-01-01", "end_date": "2025-12-31"}')
```

## Security

| Measure | Detail |
|---------|--------|
| No `eval()` / `exec()` | Expression evaluators use AST-based parsing with whitelisted operations |
| No OS command execution | `subprocess` and OS shell access are not used |
| Sandboxed `apply_expression` | Attribute access restricted to built-in types; private attributes blocked |
| DoS protection | Factorial capped at n ≤ 170; exponents ≤ 10,000; expressions ≤ 1,000 chars |
