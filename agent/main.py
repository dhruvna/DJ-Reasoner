import os
from dotenv import load_dotenv
load_dotenv()

print("Spotify Client ID:", os.getenv("SPOTIFY_CLIENT_ID"))
print("Spotify Client Secret:", os.getenv("SPOTIFY_CLIENT_SECRET"))
print("Spotify Redirect URI:", os.getenv("SPOTIFY_REDIRECT_URI"))
print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
