from livekit.agents import (
    Agent,
    RunContext,
    ChatContext,
    function_tool,
    get_job_context,
)
from livekit import api
from livekit.agents.voice import SpeechHandle
from livekit_flows.flow import ConversationFlow, FlowNode, FieldType


class FlowAgent(Agent):
    def __init__(
        self,
        flow: ConversationFlow,
        current_node: FlowNode | None = None,
        chat_ctx: ChatContext | None = None,
    ):
        self._flow = flow

        initial_node_id = self._flow.initial_node
        initial_node = next(
            (node for node in self._flow.nodes if node.id == initial_node_id), None
        )

        if not initial_node:
            raise ValueError(f"Initial node {initial_node_id} not found in flow")

        self._current_node = initial_node if current_node is None else current_node
        self._userdata_class = flow.generate_userdata_class()

        tools = []
        for edge in self._current_node.edges:
            if edge.collect_data:
                tools.append(self._build_data_collection_tool(edge))
            else:
                tools.append(
                    function_tool(
                        self._build_function_for_edge(
                            edge_id=edge.id, target_node_id=edge.target_node_id
                        ),
                        name=edge.id,
                        description=edge.condition,
                    )
                )

        super().__init__(
            instructions=flow.system_prompt,
            tools=tools,
            chat_ctx=chat_ctx,
        )

    def _build_data_collection_tool(self, edge):
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
            if not self.session._userdata:
                self.session.userdata = self._userdata_class.model_construct()

            for param in collect_params:
                value = raw_arguments[param.name]
                setattr(self.session.userdata, param.name, value)

            if edge.target_node_id:
                target_node = next(
                    (
                        node
                        for node in self._flow.nodes
                        if node.id == edge.target_node_id
                    ),
                    None,
                )
                if not target_node:
                    raise ValueError(
                        f"Target node {edge.target_node_id} not found in flow"
                    )

                new_agent = FlowAgent(self._flow, target_node, self.chat_ctx)
                self.session.update_agent(new_agent)

        return function_tool(data_collection_func, raw_schema=raw_schema)

    def _build_function_for_edge(self, edge_id: str, target_node_id: str):
        async def placeholder_func(context: RunContext):
            target_node = next(
                (node for node in self._flow.nodes if node.id == target_node_id), None
            )
            if not target_node:
                raise ValueError(f"Target node {target_node_id} not found in flow")

            new_agent = FlowAgent(self._flow, target_node, self.chat_ctx)
            self.session.update_agent(new_agent)

        return placeholder_func

    async def _end_session(self, speech_handle: SpeechHandle | None):
        if speech_handle:
            await speech_handle

        ctx = get_job_context()
        if ctx is None:
            return

        await ctx.api.room.delete_room(
            api.DeleteRoomRequest(
                room=ctx.room.name,
            )
        )

    async def on_enter(self):
        speech_handle: SpeechHandle | None = None

        if self._current_node.instruction:
            speech_handle = self.session.generate_reply(
                instructions=self._current_node.instruction
            )
        elif self._current_node.static_text:
            speech_handle = self.session.say(self._current_node.static_text)

        if self._current_node.is_final:
            await self._end_session(speech_handle)
