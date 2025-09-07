export const workerTemplate = `from livekit.agents import (
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, cartesia, deepgram, silero
from dotenv import load_dotenv
import logging
from livekit_flows import (
    FlowAgent,
    ConversationFlow,
)

load_dotenv()
logger = logging.getLogger(__name__)

yaml_flow = """{{YAML_CONTENT}}"""

flow = ConversationFlow.from_yaml_string(yaml_flow)


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = FlowAgent(flow=flow)
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4.1-mini"),
        tts=cartesia.TTS(),
    )

    await session.start(agent=agent, room=ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
`
