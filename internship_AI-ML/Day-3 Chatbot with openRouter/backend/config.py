from dotenv import dotenv_values

config = dotenv_values("../.env")  

OPENROUTER_API_KEY = config.get("OPENROUTER_API_KEY")
MONGO_URI = config.get("MONGO_URI")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-oss-120b:free"