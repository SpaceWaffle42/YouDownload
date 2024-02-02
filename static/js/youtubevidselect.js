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

// Function to handle repeated fetching with delay
function repeatFetchVideoId(times, delay) {
    function attemptFetch(remainingAttempts) {
        if (remainingAttempts > 0) {
            fetchVideoId(); // Call your fetch function
            setTimeout(() => attemptFetch(remainingAttempts - 1), delay);
        }
    }
    attemptFetch(times);
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch the video ID three times with a 10-second delay between each fetch
    repeatFetchVideoId(3, 10000); // 3 times, 10000 ms (10 seconds) delay

    // Add event listener for the submit button click
    const submitBtn = document.getElementById('SubmitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => repeatFetchVideoId(3, 10000)); // Also fetch 3 times on click, with delay
    } else {
        console.error('Submit button not found!');
    }
});
