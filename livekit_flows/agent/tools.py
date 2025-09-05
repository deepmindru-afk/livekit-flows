from __future__ import annotations

from livekit.agents import function_tool, RunContext
from ..core import FieldType, Edge, FlowNode


class ToolFactory:
    def __init__(self, on_transition, on_collect_data, get_description=None):
        self._on_transition = on_transition
        self._on_collect_data = on_collect_data
        self._get_description = get_description or (
            lambda edge_id: f"Transition via {edge_id}"
        )

    def build_data_collection_tool(self, edge: Edge):
        collect_params = edge.collect_data

        param_type_map = {
            FieldType.STRING: "string",
            FieldType.INTEGER: "integer",
            FieldType.FLOAT: "number",
            FieldType.BOOLEAN: "boolean",
        }

        properties = {}
        required_fields = []

        for param in collect_params:
            properties[param.name] = {
                "type": param_type_map[param.type],
                "description": param.description,
            }
            required_fields.append(param.name)

        raw_schema = {
            "type": "function",
            "name": edge.id,
            "description": edge.condition,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required_fields,
                "additionalProperties": False,
            },
        }

        async def data_collection_func(
            raw_arguments: dict[str, object], context: RunContext
        ):
            collected_data = {}
            for param in collect_params:
                value = raw_arguments[param.name]
                collected_data[param.name] = value

            await self._on_collect_data(collected_data, edge.target_node_id, edge.id)

        return function_tool(data_collection_func, raw_schema=raw_schema)

    def build_transition_tool(self, edge_id: str, target_node_id: str):
        async def transition_func(context: RunContext):
            await self._on_transition(target_node_id, edge_id)

        return function_tool(
            transition_func,
            name=edge_id,
            description=self._get_description(edge_id),
        )

    def build_tools_for_node(self, node: FlowNode):
        tools = []

        for edge in node.edges:
            if edge.collect_data:
                tools.append(self.build_data_collection_tool(edge))
            else:
                tools.append(self.build_transition_tool(edge.id, edge.target_node_id))

        return tools
