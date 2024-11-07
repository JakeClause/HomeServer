const canvas = document.getElementById("waterCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const waves = [
    { amplitude: 20, frequency: 0.02, phase: 0, speed: 0.1, color: "#3498db" },
    { amplitude: 15, frequency: 0.03, phase: Math.PI, speed: 0.15, color: "#003cff" },
    { amplitude: 25, frequency: 0.01, phase: Math.PI / 2, speed: 0.08, color: "#77b2ff" }
];

const boat = {
    x: canvas.width / 2,
    y: canvas.height / 1.2,
    width: 160,
    height: 40,
    poleHeight: 320,
    flagWidth: 20,
    flagHeight: 50,
    rockingAmplitude: 5,
    rockingFrequency: 0.1,
    rockingPhase: 0
};

const birds = [];

function initializeBirds() {
    const gap = canvas.width / 5; // Adjust the gap between birds
    for (let i = 0; i < 3; i++) {
    birds.push({
        x: i * gap,
        y: Math.random() * (canvas.height / 2),
        speed: 1 + Math.random() * 2
    });
    }
}

function drawBoat() {
    // Pole
    ctx.fillStyle = "#964B00"; // Brown color for pole
    ctx.fillRect(boat.x - boat.flagWidth / 2, boat.y / 1.5 - boat.height, boat.flagWidth, boat.poleHeight);

    // Boat body
    ctx.fillStyle = "#8B4513"; // Brown color for boat
    ctx.beginPath();
    ctx.arc(boat.x, boat.y / 1.1, boat.width, Math.PI, 0, true);
    ctx.closePath();
    ctx.fill();

    // Flag
    ctx.fillStyle = "#FF0000"; // Red color for flag
    ctx.beginPath();
    ctx.moveTo(boat.x - boat.flagWidth / 2, boat.y / 1.5 - boat.height);
    ctx.lineTo(boat.x * 1.5 - boat.flagWidth / 1.1, boat.y / 1.3 - boat.height - boat.flagHeight);
    ctx.lineTo(boat.x + boat.flagWidth / 2, boat.y / 2.1 - boat.height - boat.flagHeight / 2);
    ctx.closePath();
    ctx.fill();
}

function drawWater() {
    waves.forEach(wave => {
    ctx.beginPath();

    for (let x = 0; x < canvas.width; x += 5) {
        const y = wave.amplitude * Math.sin(wave.frequency * x + wave.phase);
        ctx.lineTo(x, y + canvas.height / 1.2);
    }

    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.closePath();

    ctx.fillStyle = wave.color;
    ctx.fill();
    });
}

function drawBirds() {
    ctx.fillStyle = "#000"; // Black color for birds
    birds.forEach(bird => {
    ctx.beginPath();
    ctx.moveTo(bird.x, bird.y);
    ctx.lineTo(bird.x + 10, bird.y - 20);
    ctx.lineTo(bird.x + 20, bird.y);
    ctx.closePath();
    ctx.fill();

    // Update bird position for animation
    bird.x += bird.speed;

    // Reset bird position if it goes beyond the canvas
    if (bird.x > canvas.width) {
        bird.x = -20;
    }
    });
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBirds();
    drawBoat();
    drawWater();   

    // Update wave phases for animation
    waves.forEach(wave => {
    wave.phase += wave.speed;
    });

    // Update rocking motion of the boat
    boat.y = canvas.height / 1.2 + boat.rockingAmplitude * Math.sin(boat.rockingFrequency * boat.rockingPhase);
    boat.rockingPhase += 0.05;

    requestAnimationFrame(update);
}

initializeBirds();
update();