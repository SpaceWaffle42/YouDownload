let currentVideoId = null; // Variable to store the current video ID

function updateYouTubeEmbed(videoId) {
    const iframe = document.getElementById('youtube-iframe');
    if (iframe) {
        if (videoId !== 'error') {
            iframe.src = 'https://www.youtube.com/embed/' + videoId + '?t=' + Date.now();
        } else {
            iframe.src = 'https://www.youtube.com/embed/1DCBVxH86OE';
        }
    }
}

function fetchVideoId() {
    fetch('/api/video_id')
        .then(response => response.json())
        .then(data => {
            if (data.videoId && data.videoId !== currentVideoId) {
                currentVideoId = data.videoId;
                updateYouTubeEmbed(currentVideoId);
            } else if (data.error === 'Video ID not available' && currentVideoId !== 'error') {
                currentVideoId = 'error';
                updateYouTubeEmbed(currentVideoId);
            }
        })
        .catch(error => console.error('Error fetching video ID:', error));
}

setInterval(fetchVideoId, 100);
document.addEventListener('DOMContentLoaded', fetchVideoId);
