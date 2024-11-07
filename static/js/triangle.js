document.addEventListener('DOMContentLoaded', function () {
    console.log('Document is fully loaded.');

    const canvas = document.getElementById('trianglecanvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;
    let isAnimating = true;
    let stopAnimationFlag = false; // Flag to stop animations

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

   // Function to create particles along a line with a delay
    function createParticlesAlongLineWithDelay(startX, startY, endX, endY, style, delay, color) {
        return new Promise(resolve => {
            const numParticles = 100;
            let particlesCreated = 0;
            let timeoutId;

            function createParticle() {
                if (particlesCreated > numParticles || stopAnimationFlag) {
                    resolve(); // Resolve the promise when all particles are created or animation is stopped
                    return;
                }

                const t = particlesCreated / numParticles;
                const particleX = startX + t * (endX - startX);
                const particleY = startY + t * (endY - startY);
                const particle = {
                    x: particleX,
                    y: particleY,
                    style: style,
                    speed: 2 * Math.random() + 1,
                    color: color, // Set the color property
                };
                particles.push(particle);
                drawParticles(); // Draw the particles immediately

                particlesCreated++;
                timeoutId = setTimeout(createParticle, delay); // Introduce a delay between particles
            }

            createParticle(); // Start the particle creation process

            // Listen for the stopAnimationFlag and clear the timeout if needed
            const stopListener = () => {
                clearTimeout(timeoutId);
                resolve(); // Resolve the promise when the timeout is cleared
            };

            stopListeners.push(stopListener);
            if (stopAnimationFlag) {
                stopListener(); // If the flag is set immediately, clear the timeout
            }
        });
    }

    // Function to draw particles
    function drawParticles() {
        // Draw particles
        for (const particle of particles) {
            particle.x += particle.speed * Math.cos(particle.style);
            particle.y += particle.speed * Math.sin(particle.style);

            ctx.beginPath();
            ctx.arc(particle.x, particle.y, 2, 0, 2 * Math.PI);
            ctx.fillStyle = particle.color; // Use particle's color property
            ctx.fill();
            ctx.closePath();
        }
    }

    
    let stopListeners = []; // Array to store stop listeners

    // Function to stop ongoing animations
    function stopAnimation() {
        stopAnimationFlag = true;

        // Execute all stop listeners to clear timeouts
        stopListeners.forEach(listener => listener());

        stopAnimationFlag = false; // Reset the flag
    }

    // Animation loop
    async function setup() {

        console.log('Triangle Style Loaded');
        // Draw first triangle
        const triangleSize = 50;
        const leftCornerX = 0;
        const leftCornerY = canvas.height;
        const rightCornerX = canvas.width;
        const rightCornerY = canvas.height;
        const middleX = canvas.width / 2;
        const middleY = 0;

        // Generate a random color for the triangle
        const randomColor = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.5)`;

        // Create particles along the lines of the triangle with a delay and random color
        particles = [];
        await createParticlesAlongLineWithDelay(leftCornerX, leftCornerY, middleX - triangleSize / 9, middleY, 0, 10, randomColor);
        await createParticlesAlongLineWithDelay(middleX + triangleSize / 9, middleY, rightCornerX, rightCornerY, 0, 10, randomColor);
        await createParticlesAlongLineWithDelay(leftCornerX, leftCornerY - 10, rightCornerX, rightCornerY, 1, 10, randomColor);

        // Continue with the animation loop if not explicitly stopped
        if (isAnimating && !stopAnimationFlag) {
            animationId = requestAnimationFrame(setup);
        } else {
            stopAnimationFlag = false; // Reset the stopAnimationFlag
        }
    }

    // Function to start or stop the animation
    function toggleAnimation() {
        if (isAnimating) {
            stopAnimationFlag = true; // Set the flag to stop the animation
        } else {
            setup();
        }
        isAnimating = !isAnimating;

        // Update button text and color
        const startStopButton = document.getElementById('ssb');
        startStopButton.style.backgroundColor = isAnimating ? 'red' : 'green';
        startStopButton.textContent = isAnimating ? 'Stop' : 'Start';
    }

    // Start animation with delay
    setup();
});
