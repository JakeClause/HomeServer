async function fetchHDDUsage() {
    try {
        const response = await fetch('/disk-info');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Error fetching HDD data:', error);
        return {};
    }
}

function getColorForUsage(percentage) {
    if (percentage < 50) {
        return '#4caf50'; // Green
    } else if (percentage < 75) {
        return '#ffeb3b'; // Yellow
    } else {
        return '#f44336'; // Red
    }
}

function createCircleContainer(drive, data) {
    const container = document.createElement('div');
    container.className = 'container';

    const circleContainer = document.createElement('div');
    circleContainer.className = 'circle-container';

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 150 150');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

    const radius = 65;
    const circumference = 2 * Math.PI * radius;

    const circleBackground = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circleBackground.setAttribute('cx', '75');
    circleBackground.setAttribute('cy', '75');
    circleBackground.setAttribute('r', radius);
    circleBackground.className.baseVal = 'circle-background';
    svg.appendChild(circleBackground);

    const circleProgress = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circleProgress.setAttribute('cx', '75');
    circleProgress.setAttribute('cy', '75');
    circleProgress.setAttribute('r', radius);
    circleProgress.className.baseVal = 'circle-progress';
    circleProgress.style.strokeDasharray = circumference;
    circleProgress.style.strokeDashoffset = circumference;
    svg.appendChild(circleProgress);

    // Add the drive letter to the circle text
    const circleText = document.createElement('div');
    circleText.className = 'circle-text';
    circleText.textContent = `${drive} - ${data.free.toFixed(2)} ${data.unit}`;
    circleContainer.appendChild(svg);
    circleContainer.appendChild(circleText);

    container.appendChild(circleContainer);

    const info = document.createElement('p');
    info.className = 'space-info';
    //info.textContent = `Used: ${data.used.toFixed(2)} ${data.unit} / ${data.total.toFixed(2)} ${data.unit} (Free: ${data.free.toFixed(2)} ${data.unit})`;
    container.appendChild(info);

    return {
        container,
        circleProgress,
        fillPercentage: (data.used / data.total) * 100
    };
}

async function updateHDDDisplay() {
    const diskData = await fetchHDDUsage();
    const container = document.getElementById('diskContainer');
    container.innerHTML = '';

    for (const [drive, data] of Object.entries(diskData)) {
        if (data.error) {
            console.error(`Error with drive ${drive}: ${data.error}`);
            continue;
        }

        const { container: circleContainer, circleProgress, fillPercentage } = createCircleContainer(drive, data);
        container.appendChild(circleContainer);

        const radius = 65;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference * (1 - fillPercentage / 100);

        const color = getColorForUsage(fillPercentage);
        circleProgress.style.stroke = color;
        circleProgress.style.strokeDashoffset = offset;
    }
}

// Update the display on page load
updateHDDDisplay();
