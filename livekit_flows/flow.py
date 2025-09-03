from pydantic import BaseModel, Field, create_model
from typing import Optional, Type
from enum import Enum


class FieldType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"


class DataField(BaseModel):
    name: str
    type: FieldType
    description: str
    required: bool = False


class Edge(BaseModel):
    condition: str
    id: str
    target_node_id: str | None = None
    collect_data: list[DataField] = Field(default_factory=list)


class FlowNode(BaseModel):
    id: str
    name: str
    instruction: str | None = None
    static_text: str | None = None
    is_final: bool = False
    edges: list[Edge] = Field(default_factory=list)


class ConversationFlow(BaseModel):
    system_prompt: str
    initial_node: str
    nodes: list[FlowNode]

    def generate_userdata_class(self) -> Type[BaseModel]:
        field_map = {}

        for node in self.nodes:
            for edge in node.edges:
                for param in edge.collect_data:
                    field_name = param.name

                    if field_name not in field_map:
                        field_map[field_name] = param
                    else:
                        # TODO: handle conflicts
                        ...

        if not field_map:
            return create_model("FlowUserData")

        field_definitions = {}

        for param in field_map.values():
            if param.type == FieldType.STRING:
                base_type = str
            elif param.type == FieldType.INTEGER:
                base_type = int
            elif param.type == FieldType.FLOAT:
                base_type = float
            elif param.type == FieldType.BOOLEAN:
                base_type = bool
            else:
                base_type = str

            if param.required:
                field_type = base_type
                field_definition = Field(description=param.description)
            else:
                field_type = Optional[base_type]
                field_definition = Field(default=None, description=param.description)

            field_definitions[param.name] = (field_type, field_definition)

        return create_model("FlowUserData", **field_definitions)
