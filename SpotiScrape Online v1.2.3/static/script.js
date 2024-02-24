// JavaScript code for pasting content into the input field
document.getElementById('paste_button').addEventListener('click', function() {
    navigator.clipboard.readText()
    .then(text => {
        document.getElementById('spotify_url').value = text;
    })
    .catch(err => {
        console.error('Failed to read clipboard contents: ', err);
    });
});

// Function to handle the download action
function downloadArtwork(url) {
    fetch(url)
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
}

// Check if the scrape has completed and show the download button
function checkScrapeCompletion() {
    // Assuming you have some variable or condition to check if scraping is completed
    var scrapeCompleted = true; // Replace with your actual condition

    if (scrapeCompleted) {
        document.getElementById('download_button').style.display = 'block';
        document.getElementById('clear_button').style.display = 'block'; // Show clear button after scraping is complete
    }
}

// Event listener for the scrape button click
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
        // After scraping is completed, check if it's completed
        checkScrapeCompletion();
    })
    .catch(error => console.error('Error:', error));
});

// Event listener for the download button click
document.getElementById('download_button').addEventListener('click', function() {
    // Assuming you have the URL of the artwork to be downloaded
    var artworkUrl = document.getElementById('playlist_image').src;
    downloadArtwork(artworkUrl);
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
        // Hide the download button and clear button when clearing input
        document.getElementById('download_button').style.display = 'none';
        document.getElementById('clear_button').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
});
