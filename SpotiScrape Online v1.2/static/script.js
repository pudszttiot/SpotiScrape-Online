// JavaScript code for downloading artwork
document.getElementById('download_button').addEventListener('click', function() {
    var imageUrl = document.getElementById('playlist_image').src;
    fetch(imageUrl)
    .then(response => response.blob())
    .then(blob => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'artwork.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
});

// JavaScript code for scraping Spotify URL
document.getElementById('scrape_button').addEventListener('click', function() {
    var spotifyUrl = document.getElementById('spotify_url').value;
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'spotify_url=' + encodeURIComponent(spotifyUrl)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerText = data.error;
            return;
        }
        if (data.type === 'track') {
            document.getElementById('result').innerHTML = `<p>Artist: ${data.artist}</p><p>Album: ${data.album}</p><p>Track: ${data.track}</p>`;
            var img = document.createElement('img');
            img.src = data.artwork_url;
            img.id = 'playlist_image';
            document.getElementById('result').appendChild(img);
        } else if (data.type === 'playlist') {
            document.getElementById('result').innerHTML = `<p>Playlist Name: ${data.playlist_name}</p><p>Owner: ${data.playlist_owner}</p><p>Total Tracks: ${data.total_tracks}</p>`;
            var img = document.createElement('img');
            img.src = data.playlist_image_url;
            img.id = 'playlist_image';
            document.getElementById('result').appendChild(img);
        }
    })
    .catch(error => console.error('Error:', error));
});

// JavaScript code for clearing input
document.getElementById('clear_button').addEventListener('click', function() {
    fetch('/clear_input', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('spotify_url').value = '';
        document.getElementById('result').innerText = '';
        var img = document.getElementById('playlist_image');
        if (img) {
            img.remove();
        }
    })
    .catch(error => console.error('Error:', error));
});

// JavaScript code for scraping Spotify URL
document.getElementById('scrape_button').addEventListener('click', function() {
    // Other existing code for scraping...
    // After scraping is completed, show the buttons
    document.getElementById('download_button').style.display = 'inline-block';
    document.getElementById('clear_button').style.display = 'inline-block';
});

