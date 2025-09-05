from pydantic import BaseModel, Field, create_model
from typing import Optional, Type
from ..core import FieldType, ConversationFlow, DataField


def _get_python_type(field_type: FieldType) -> Type:
    type_mapping = {
        FieldType.STRING: str,
        FieldType.INTEGER: int,
        FieldType.FLOAT: float,
        FieldType.BOOLEAN: bool,
    }
    return type_mapping.get(field_type, str)


def _build_field_map(flow: ConversationFlow) -> dict[str, DataField]:
    field_map = {}

    for node in flow.nodes:
        for edge in node.edges:
            for param in edge.collect_data:
                field_name = param.name

                if field_name not in field_map:
                    field_map[field_name] = param
                else:
                    # Handle conflicts by keeping the first definition
                    # TODO: Add proper conflict resolution strategy
                    pass

    return field_map


def _build_field_definitions(field_map: dict[str, DataField]) -> dict[str, tuple]:
    field_definitions = {}

    for param in field_map.values():
        base_type = _get_python_type(param.type)

        if param.required:
            field_type = base_type
            field_definition = Field(description=param.description)
        else:
            field_type = Optional[base_type]
            field_definition = Field(default=None, description=param.description)

        field_definitions[param.name] = (field_type, field_definition)

    return field_definitions


def generate_userdata_class(
    flow: ConversationFlow, class_name: str = "FlowUserData"
) -> Type[BaseModel]:
    field_map = _build_field_map(flow)

    if not field_map:
        return create_model(class_name)

    field_definitions = _build_field_definitions(field_map)
    return create_model(class_name, **field_definitions)
