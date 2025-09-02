from livekit.agents import Agent
from livekit_flows.flow import ConversationFlow


class FlowAgent(Agent):
    def __init__(self, flow: ConversationFlow):
        self.flow = flow

        super().__init__(
            instructions=flow.system_prompt,
        )

    async def on_enter(self):
        initial_node_id = self.flow.initial_node
        initial_node = next(
            (node for node in self.flow.nodes if node.id == initial_node_id), None
        )

        if not initial_node:
            raise ValueError(f"Initial node {initial_node_id} not found in flow")

        if initial_node.instruction:
            await self.session.generate_reply(instructions=initial_node.instruction)
        elif initial_node.static_text:
            await self.session.say(initial_node.static_text)
