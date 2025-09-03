from livekit.agents import (
    Agent,
    RunContext,
    ChatContext,
    function_tool,
    get_job_context,
)
from livekit import api
from livekit.agents.voice import SpeechHandle
from livekit_flows.flow import ConversationFlow, FlowNode


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

        tools = []
        for edge in self._current_node.edges:
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

    def _build_function_for_edge(self, edge_id: str, target_node_id: str):
        async def placeholder_func(context: RunContext):
            target_node = next(
                (node for node in self._flow.nodes if node.id == target_node_id), None
            )
            if not target_node:
                raise ValueError(f"Target node {target_node_id} not found in flow")

            self.session.update_agent(FlowAgent(self._flow, target_node, self.chat_ctx))

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
