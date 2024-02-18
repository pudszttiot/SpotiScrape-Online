import time

print("\nWelcome to SpotiScrape Online\n")
time.sleep(3)
print("Starting SpotiScrape...\n")
time.sleep(3)
print("Successfully running SpotiScrape Online\n")
time.sleep(3)
print("Copy the URL below and paste into ur web browser\n")
time.sleep(3)
print("http://localhost:50100")

from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image
import io
from urllib.parse import urlparse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import filedialog
from waitress import serve

app = Flask(__name__)

# Spotify API credentials
client_id = "84d6cd4d6351419d8dc750a2768930ff"
client_secret = "94ca367fbd01433b8b01923d661c3431"

# Initialize Spotify client
sp = Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape_spotify", methods=["POST"])
def scrape_spotify():
    try:
        spotify_url = request.form["spotify_url"]

        if not is_valid_spotify_url(spotify_url):
            return jsonify({"error": "Invalid Spotify URL"})

        track_info = sp.track(spotify_url)
        artist = track_info["artists"][0]["name"]
        album = track_info["album"]["name"]
        track = track_info["name"]
        artwork_url = track_info["album"]["images"][0]["url"]

        return jsonify(
            {
                "artist": artist,
                "album": album,
                "track": track,
                "artwork_url": artwork_url,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/download_artwork", methods=["POST"])
def download_artwork():
    try:
        artwork_url = request.form["artwork_url"]
        response = requests.get(artwork_url)
        image = Image.open(io.BytesIO(response.content))

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            image.save(file_path)
            return jsonify({"success": "Artwork saved successfully"})

        return jsonify({"error": "No file selected"})

    except Exception as e:
        return jsonify({"error": str(e)})


def is_valid_spotify_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "open.spotify.com" and parsed_url.path.startswith(
        "/track/"
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=50100, threads=1)
