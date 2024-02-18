import webview
from threading import Thread
from flask import Flask, render_template, request, jsonify
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import urlparse

# Spotify API credentials
client_id = "84d6cd4d6351419d8dc750a2768930ff"
client_secret = "94ca367fbd01433b8b01923d661c3431"

# Initialize Flask app
app = Flask(__name__)

# Initialize Spotify client
sp = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)

def is_valid_spotify_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "open.spotify.com" and (
        parsed_url.path.startswith("/track/")
        or parsed_url.path.startswith("/playlist/")
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    spotify_url = request.form['spotify_url']

    if not is_valid_spotify_url(spotify_url):
        return jsonify({'error': 'Invalid Spotify URL'}), 400

    try:
        if "/track/" in spotify_url:
            track_info = sp.track(spotify_url)
            artist = track_info["artists"][0]["name"]
            album = track_info["album"]["name"]
            track = track_info["name"]
            artwork_url = track_info["album"]["images"][0]["url"]

            return jsonify({'type': 'track', 'artist': artist, 'album': album, 'track': track, 'artwork_url': artwork_url})

        elif "/playlist/" in spotify_url:
            playlist_id = spotify_url.split("/playlist/")[-1]
            playlist_info = sp.playlist(playlist_id)
            playlist_name = playlist_info["name"]
            playlist_owner = playlist_info["owner"]["display_name"]
            total_tracks = playlist_info["tracks"]["total"]
            playlist_image_url = playlist_info["images"][0]["url"]
            tracks = []
            for track in playlist_info['tracks']['items']:
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                tracks.append({'track_name': track_name, 'artist_name': artist_name})

            return jsonify({'type': 'playlist', 'playlist_name': playlist_name, 'playlist_owner': playlist_owner, 'total_tracks': total_tracks, 'playlist_image_url': playlist_image_url, 'tracks': tracks})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_artwork', methods=['POST'])
def download_artwork():
    artwork_url = request.form['artwork_url']
    try:
        response = requests.get(artwork_url)
        img_data = response.content
        with open("artwork.png", "wb") as f:
            f.write(img_data)
        return jsonify({'message': 'Artwork saved as artwork.png'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_input', methods=['POST'])
def clear_input():
    return jsonify({'message': 'Input cleared successfully'}), 200

@app.route('/load_and_display_artwork', methods=['POST'])
def load_and_display_artwork():
    artwork_url = request.form['artwork_url']
    try:
        response = requests.get(artwork_url)
        img_data = response.content
        return img_data, 200, {'Content-Type': 'image/png'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_flask_thread():
    app.run(debug=False)

if __name__ == "__main__":
    flask_thread = Thread(target=create_flask_thread)
    flask_thread.start()

    # Create a standard webview window
    window = webview.create_window(
        title='SpotiScrape Online', 
        url='http://127.0.0.1:5000', 
        width=800, 
        height=610, 
        resizable=True, 
        fullscreen=False,
        confirm_close=True
    )
    
    # Start the webview
    webview.start()
