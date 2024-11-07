document.addEventListener('DOMContentLoaded', function() {
    const videoGrid = document.getElementById('videoGrid');
    const searchInput = document.getElementById('searchInput');

    // Function to fetch and display videos
    function fetchAndDisplayVideos() {
        fetch('/get_videos')
            .then(response => response.json())
            .then(videos => {
                displayVideos(videos);
                lazyLoadThumbnails(); // Call lazy loading after displaying videos
            })
            .catch(error => console.error('Error fetching videos:', error));
    }

    // Function to display videos in the grid
    function displayVideos(videos) {
        videoGrid.innerHTML = ''; // Clear previous videos

        videos.forEach(video => {
            const videoItem = document.createElement('div');
            videoItem.classList.add('video-item');

            const videoElement = document.createElement('video');
            videoElement.classList.add('video-thumbnail');
            videoElement.setAttribute('data-src', `/videos/${encodeURIComponent(video)}`);
            videoElement.controls = false;
            videoElement.muted = true; // Mute the video
            videoElement.autoplay = false; // Do not autoplay

            const videoTitle = document.createElement('div');
            videoTitle.classList.add('video-title');
            videoTitle.textContent = video;

            videoItem.appendChild(videoElement);
            videoItem.appendChild(videoTitle);

            videoItem.addEventListener('click', function() {
                // Handle video click (navigate to watch page or play video)
                window.location.href = `/watch/${encodeURIComponent(video)}`;
            });

            videoGrid.appendChild(videoItem);
        });
    }

    // Lazy loading function for video thumbnails
    function lazyLoadThumbnails() {
        const videoThumbnails = document.querySelectorAll('.video-thumbnail');

        const lazyLoadHandler = function() {
            videoThumbnails.forEach(thumbnail => {
                if (thumbnail.getAttribute('data-src') && isElementInViewport(thumbnail)) {
                    thumbnail.src = thumbnail.getAttribute('data-src');
                    thumbnail.removeAttribute('data-src');
                }
            });
        };

        // Initial load
        lazyLoadHandler();

        // Event listener for scrolling and resizing
        window.addEventListener('scroll', lazyLoadHandler);
        window.addEventListener('resize', lazyLoadHandler);
    }

    // Function to check if an element is in the viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Initial fetch and display of videos
    fetchAndDisplayVideos();

    // Event listener for search input changes
    searchInput.addEventListener('input', function() {
        const searchText = searchInput.value.toLowerCase();

        fetch('/get_videos')
            .then(response => response.json())
            .then(videos => {
                // Filter videos based on search input
                const filteredVideos = videos.filter(video =>
                    video.toLowerCase().includes(searchText)
                );
                displayVideos(filteredVideos);
                lazyLoadThumbnails(); // Call lazy loading after displaying filtered videos
            })
            .catch(error => console.error('Error fetching videos:', error));
    });
});
