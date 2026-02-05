"""
Simple Voice Agent Example using Voice.ai TTS

Demonstrates using the Voice.ai TTS plugin with LiveKit Agents.

Environment variables required:
- LIVEKIT_URL: LiveKit server URL
- LIVEKIT_API_KEY: LiveKit API key
- LIVEKIT_API_SECRET: LiveKit API secret
- OPENAI_API_KEY: OpenAI API key
- VOICEAI_API_KEY: Voice.ai API key (vk_*)
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from livekit.agents import AgentServer, JobContext, JobProcess, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, silero
from livekit.plugins.turn_detector.english import EnglishModel

# Import Voice.ai TTS plugin
from livekit.plugins.voiceai import TTS as VoiceAITTS

logger = logging.getLogger("voiceai-agent")

# Load environment variables
load_dotenv()


server = AgentServer()


def prewarm(proc: JobProcess):
    """Prewarm VAD model for faster startup."""
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    """Main entrypoint for the voice agent."""
    
    # Get optional voice_id from room metadata
    voice_id = None
    if ctx.room.metadata:
        import json
        try:
            metadata = json.loads(ctx.room.metadata)
            voice_id = metadata.get("voice_id")
            if voice_id:
                logger.info(f"Using voice_id: {voice_id}")
        except json.JSONDecodeError:
            pass

    # Configure Voice.ai TTS
    tts_config = {
        "model": "voiceai-tts-v1-latest",
        "language": "en",
        "temperature": 1.0,
        "top_p": 0.8,
    }
    if voice_id:
        tts_config["voice_id"] = voice_id

    # Create agent session with all components
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT(model="gpt-4o-mini-transcribe"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=VoiceAITTS(**tts_config),
        turn_detection=EnglishModel(),
    )

    # Start the session with a simple agent
    await session.start(
        agent=Agent(
            instructions=(
                "You are a helpful voice assistant created by Voice.ai. "
                "Keep responses short and conversational. "
                "Avoid special characters that don't work in speech."
            )
        ),
        room=ctx.room,
    )


if __name__ == "__main__":
    cli.run_app(server)
