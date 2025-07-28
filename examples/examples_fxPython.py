
# importing the my modules
mymoudules_path  ="C:/apps/onedrive/jrodriguezgar/OneDrive/dev/git/DatamanEdge"
import sys  
sys.path.append(mymoudules_path + '/Formulite') 
import formulite as fxlite

# Example of using the function json_schema_to_pydantic_model

# Example JSON schema
example_schema = {
    "title": "Person",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age"]
}

# Generate the Pydantic model class dynamically
PersonModel = fxlite.json_schema_to_pydantic_model(example_schema)
print('json schema:')
print(example_schema)

# Use the generated model
person = PersonModel(name="Alice", age=30, email="alice@example.com")

print('pydantic model:')
print(person)

# Segundo ejemplo: convertir otro JSON schema
capital_schema = {
    'type': 'object',
    'properties': {
        'capital': {'type': 'string'}
    },
    'required': ['capital']
}

CapitalModel = fxlite.json_schema_to_pydantic_model(capital_schema)
print('\njson schema:')
print(capital_schema)
capital_instance = CapitalModel(capital='Madrid')
print('pydantic model:')
print(capital_instance)



