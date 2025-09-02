from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import openai, cartesia, deepgram, silero
from dotenv import load_dotenv

from livekit_flows.flow import ConversationFlow, FlowNode, Edge

load_dotenv()

reservation_flow = ConversationFlow(
    system_prompt="You take restaurant reservations. Be friendly and get: name, party size, date, time.",
    initial_node="welcome",
    nodes=[
        FlowNode(
            id="welcome",
            name="Welcome",
            instruction="Hi! I'll help you make a reservation. What's your name?",
            edges=[
                Edge(
                    condition="Got name",
                    id="welcome_to_get_details",
                    target_node_id="get_details",
                )
            ],
        ),
        FlowNode(
            id="get_details",
            name="Get Details",
            instruction="Great! How many people and what date and time?",
            edges=[
                Edge(
                    condition="Got details",
                    id="get_details_to_confirm",
                    target_node_id="confirm",
                )
            ],
        ),
        FlowNode(
            id="confirm",
            name="Confirm",
            instruction="I have your reservation. Is everything correct?",
            edges=[
                Edge(condition="Yes", id="confirm_to_done", target_node_id="done"),
                Edge(
                    condition="No",
                    id="confirm_to_get_details",
                    target_node_id="get_details",
                ),
            ],
        ),
        FlowNode(id="done", name="Done", static_text="All set! See you then!"),
    ],
)


@function_tool
async def lookup_weather(
    context: RunContext,
    location: str,
):
    """Used to look up weather information."""

    return {"weather": "sunny", "temperature": 30}


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions="You are a friendly voice assistant",
        tools=[lookup_weather],
    )
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="Greet the user.")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
