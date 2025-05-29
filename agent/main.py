import os
from dotenv import load_dotenv
load_dotenv()

print("Spotify Client ID:", os.getenv("SPOTIFY_CLIENT_ID"))
