# LiveKit Voice Agent Example with Voice.ai TTS

A simple example demonstrating how to build a voice agent using LiveKit Agents with the Voice.ai TTS plugin.

## Quick Start

1. **Clone this repo (including the Voice.ai plugin submodule):**
   ```bash
   git clone --recurse-submodules https://github.com/voice-ai/livekit-plugins-voiceai-example.git
   cd livekit-plugins-voiceai-example
   ```
   If you already cloned without submodules, run: `git submodule update --init --recursive`

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the Voice.ai plugin from this repo** (required — the plugin is not on PyPI yet):
   ```bash
   pip install -e ./livekit-plugins-voiceai
   ```

4. **Install the rest of the dependencies:**
   
   Using `uv` (recommended):
   ```bash
   uv pip install -e .
   ```
   
   Or using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Download required models:**
   ```bash
   python agent_voiceai_example.py download-files
   ```

6. **Configure environment variables:**
   Copy `env.example` to `.env` and fill in your API keys:
   ```bash
   cp env.example .env
   # Then edit .env with your actual API keys
   ```

7. **Run the agent:**
   ```bash
   python agent_voiceai_example.py dev
   ```

## Project Structure

- `agent_voiceai_example.py` - Example agent entrypoint
- `livekit-plugins-voiceai/` - Voice.ai TTS plugin (install from this repo; see Quick Start step 3)

## Testing

Generate a participant token and connect to a room:
```bash
lk token create \
  --url YOUR_LIVEKIT_SERVER_URL \
  --api-key YOUR_API_KEY \
  --api-secret YOUR_API_SECRET \
  --room test-room \
  --identity test-user \
  --join --valid-for 1h
```

