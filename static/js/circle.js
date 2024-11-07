document.addEventListener('DOMContentLoaded', function () {
  const canvas = document.getElementById('circlecanvas');
  const ctx = canvas.getContext('2d');

  const resolution = 40;
  let particles = [];
  const numVectors = 36; // Number of vectors/arrows
  const historyLength = 30; // Length of the history/trail
  let animationId; // Variable to store the animation frame ID
  isAnimating = true; // Flag to stop animations


  function Particle() {
    this.angle = 0;
    this.radius = 10;
    this.history = [];
  }

  Particle.prototype.update = function () {
    this.angle += 0.05; // Adjust the rotation speed
    this.radius -= 0.1; // Adjust the spiraling speed

    const x = canvas.width / 2 + Math.cos(this.angle) * this.radius;
    const y = canvas.height / 2 + Math.sin(this.angle) * this.radius;

    // Wrap particles around the circular vectors
    if (x < 0 || x > canvas.width || y < 0 || y > canvas.height) {
      this.angle += Math.PI; // Reverse direction
    }

    this.pos = { x, y };
    this.history.push({ x, y });

    // Keep the history length limited
    if (this.history.length > historyLength) {
      this.history.shift();
    }
  };

  Particle.prototype.display = function () {
    Particle.prototype.display = function () {
      ctx.fillStyle = '#000';
    
      // Adjust the size to make the particles (arrows) thicker
      ctx.fillRect(this.pos.x, this.pos.y, 10, 10); // Increase the size to make them thicker
    };
    
  };

  Particle.prototype.displayTrail = function () {
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;

    for (let i = 1; i < this.history.length; i++) {
      ctx.beginPath();
      ctx.moveTo(this.history[i - 1].x, this.history[i - 1].y);
      ctx.lineTo(this.history[i].x, this.history[i].y);
      ctx.stroke();
    }
  };

  function drawVectors() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
  
    // Set a thicker line width
    ctx.lineWidth = 1;
  
    for (let i = 0; i < numVectors; i++) {
      const angle = (i / numVectors) * Math.PI * 2;
      const x = centerX + Math.cos(angle) * canvas.width / 2;
      const y = centerY + Math.sin(angle) * canvas.height / 2;
  
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  }
  

  function setup() {
    console.log('Circle Style Loaded');
    canvas.width = 800;
    canvas.height = 600;
  
    // Create particles
    for (let i = 0; i < 1; i++) {
      particles.push(new Particle());
    }
    
    animate(); // Start the animation automatically
  }
  

  function applyStyle(style) {
  switch (style) {
    case 1:
      // You can customize the styles for style 1 here
      // For simplicity, I'm keeping only one style (style 1) in this example

      // Update particle display size
      Particle.prototype.display = function () {
        ctx.fillStyle = '#000';
        ctx.fillRect(this.pos.x, this.pos.y, 4, 4); // Adjust size as needed
      };

      // Update vector line width
      function drawVectors() {
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        // Set a thicker line width
        ctx.lineWidth = 2;

        for (let i = 0; i < numVectors; i++) {
          const angle = (i / numVectors) * Math.PI * 2;
          const x = centerX + Math.cos(angle) * canvas.width / 2;
          const y = centerY + Math.sin(angle) * canvas.height / 2;

          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.lineTo(x, y);
          ctx.stroke();
        }
      }

      break;

    // Add more cases for other styles if needed

    default:
      // Default to style 1 if an unsupported style is selected
      applyStyle(1);
      break;
  }
}


  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw vectors/arrows
    drawVectors();

    // Update and display particles
    particles.forEach(function (particle) {
      particle.update();
      particle.display();
      particle.displayTrail();
    });

    if (isAnimating) {
      animationId = requestAnimationFrame(animate);
    }
  }

  function resetAnimation() {
    // Reset particles and start the animation from the beginning
    particles = [new Particle()];
    animate();
  }

  // Initialize the animation when the page loads
  setup();
});
