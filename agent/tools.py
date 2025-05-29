# agent/tools.py

from langchain.tools import Tool
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Spotify credentials
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Define search function
def search_spotify_tracks(prompt: str, limit: int = 5) -> str:
    results = sp.search(q=prompt, type='track', limit=limit)
    tracks = results.get("tracks", {}).get("items", [])
    
    if not tracks:
        return "No tracks found."

    output = []
    for i, track in enumerate(tracks):
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]
        output.append(f"{i+1}. '{name}' by {artist} — [Link]({url})")

    return "\n".join(output)

# Wrap it as a LangChain tool
spotify_tool = Tool.from_function(
    func=search_spotify_tracks,
    name="Spotify Music Search",
    description="Search for music on Spotify given a mood, genre, or description prompt."
)
