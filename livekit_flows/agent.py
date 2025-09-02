from livekit.agents import Agent, RunContext, ChatContext, function_tool
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

    async def on_enter(self):
        if self._current_node.instruction:
            await self.session.generate_reply(
                instructions=self._current_node.instruction
            )
        elif self._current_node.static_text:
            await self.session.say(self._current_node.static_text)
