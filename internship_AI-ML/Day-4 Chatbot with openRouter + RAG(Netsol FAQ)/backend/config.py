from pathlib import Path
from dotenv import dotenv_values

env_path = Path(__file__).resolve().parent.parent / ".env"
config = dotenv_values(env_path)

OPENROUTER_API_KEY = config.get("OPENROUTER_API_KEY")
MONGO_URI = config.get("MONGO_URI")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"
MODEL = "openai/gpt-oss-120b:free"
EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"