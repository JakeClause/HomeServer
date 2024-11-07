document.addEventListener('DOMContentLoaded', function() {
    // Array of background image URLs
    var backgrounds = [
        "url('https://images3.alphacoders.com/132/1325254.png')",
        "url('https://i.pinimg.com/originals/04/b8/48/04b848ceb67469b2029598fc66b59dd5.jpg')",
        "url('https://i.redd.it/4vztk5m7p9651.jpg')",
        "url('https://wallpapers.com/images/hd/funny-monkey-closeup-hc2uqyfra5r5hf9t.jpg')",
        "url('https://png.pngtree.com/background/20230612/original/pngtree-underwater-wallpaper-with-corals-and-sharks-picture-image_3183726.jpg')",
        "url('https://wallpapers.com/images/hd/jungle-desktop-v376os7u4d8ghswj.jpg')",
        "url('https://wallpapers.com/images/hd/1920x1080-hd-space-oo9nd7iccchf25t8.jpg')",
    ];

    // Function to set background image
    function setBackground(index) {
        document.body.style.backgroundImage = backgrounds[index];
        localStorage.setItem('backgroundIndex', index); // Store index in localStorage
    }

    // Check if there's a stored background index in localStorage
    var storedIndex = localStorage.getItem('backgroundIndex');
    if (storedIndex !== null) {
        setBackground(parseInt(storedIndex)); // Set background from stored index
    } else {
        setBackground(0); // Set default background
    }

    // Add event listener to cycle through backgrounds if the button exists
    var cycleBackgroundBtn = document.getElementById('cycleBackgroundBtn');
    if (cycleBackgroundBtn) {
        cycleBackgroundBtn.addEventListener('click', function() {
            var currentIndex = parseInt(localStorage.getItem('backgroundIndex')) || 0;
            var nextIndex = (currentIndex + 1) % backgrounds.length;
            setBackground(nextIndex);
        });
    }
});
