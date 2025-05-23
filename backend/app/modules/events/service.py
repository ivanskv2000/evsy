from app.modules.events.schemas import EventOut


def map_field_type_to_openapi(field_type: str) -> dict:
    return {
        "string": {"type": "string"},
        "integer": {"type": "integer", "format": "int32"},
        "number": {"type": "number", "format": "float"},
        "boolean": {"type": "boolean"},
        "object": {"type": "object"},
        "array": {"type": "array"},
    }.get(field_type, {"type": "string"})


def generate_json_schema_for_event(
    event: EventOut,
    *,
    additional_properties: bool = True,
    include_descriptions: bool = True,
    include_examples: bool = True,
) -> dict:
    schema = {
        "type": "object",
        "additionalProperties": additional_properties,
        "properties": {},
        "required": [],
    }

    for field in event.fields:
        field_type_info = map_field_type_to_openapi(field.field_type)

        field_schema = {"type": field_type_info["type"]}
        if "format" in field_type_info:
            field_schema["format"] = field_type_info["format"]

        if include_descriptions and field.description:
            field_schema["description"] = field.description

        if include_examples and field.example is not None:
            field_schema["example"] = field.example

        schema["properties"][field.name] = field_schema

        # if not field.optional:
        if True:
            schema["required"].append(field.name)

    if not schema["required"]:
        del schema["required"]

    return schema
