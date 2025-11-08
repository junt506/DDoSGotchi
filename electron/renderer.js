// ============================================================================
// DDOS GOTCHI v3.0 - Redesigned HUD Renderer
// ============================================================================

// ============================================================================
// PWNAGOTCHI FACES & QUOTES
// ============================================================================

const FACES = {
    HAPPY: "(◕‿‿◕)",
    INTENSE: "(⌐■_■)",
    COOL: "(◕‿◕)✧",
    EXCITED: "ヽ(◕‿‿◕)ﾉ",
    ATTACK: "(╬ಠ益ಠ)",
    BORED: "(◡‿◡✿)",
};

const QUOTES_NORMAL = [
    "monitoring packets...",
    "sniffing networks...",
    "analyzing traffic...",
    "watching connections...",
    "all systems operational",
    "scanning for threats...",
    "neural network active",
    "defenses online",
];

const QUOTES_ATTACK = [
    "ATTACK DETECTED!",
    "network under siege!",
    "defensive mode activated",
    "repelling intruders!",
    "threat neutralization active",
];

// ============================================================================
// STATE VARIABLES
// ============================================================================

let ws = null;
let reconnectInterval = null;
let isAttackMode = false;

// Graph data storage
const maxDataPoints = 60;
let latencyHistory = [];
let packetLossHistory = [];

// Connection tracking
let allConnections = [];
let maxLogEntries = 50;

// Activity bars
let activityData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// ============================================================================
// INITIALIZATION
// ============================================================================

function init() {
    console.log('DDoS Gotchi v3.0 - Initializing...');

    // Generate dynamic 3D elements
    generateTickMarks();
    generateActivityBars();

    // Connect to backend
    connectWebSocket();

    // Start periodic updates
    setInterval(updateTime, 1000);
    setInterval(() => updateQuote(null, true), 5000);

    // Set initial mode
    document.body.classList.add('mode-normal');

    console.log('Initialization complete');
}

// Generate rotating tick marks for #f2
function generateTickMarks() {
    const f2 = document.getElementById('f2');
    for (let i = 0; i < 36; i++) {
        const span = document.createElement('span');
        span.style.transform = `rotateZ(${i * 10}deg) translateY(200px)`;
        f2.appendChild(span);
    }

    // Generate inner tick marks for #f5
    const f5 = document.getElementById('f5');
    for (let i = 0; i < 18; i++) {
        const span = document.createElement('span');
        span.style.transform = `rotateZ(${i * 20}deg) translateY(100px)`;
        f5.appendChild(span);
    }
}

// Generate activity bars
function generateActivityBars() {
    const container = document.getElementById('activity-bars');
    for (let i = 0; i < 10; i++) {
        const bar = document.createElement('div');
        bar.className = 'activity-bar';
        bar.style.height = '5px';
        container.appendChild(bar);
    }
}

// ============================================================================
// WEBSOCKET CONNECTION
// ============================================================================

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
        console.log('✓ Connected to backend');
        updateQuote("connected to backend!", false);

        if (reconnectInterval) {
            clearInterval(reconnectInterval);
            reconnectInterval = null;
        }
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            updateUI(data);
        } catch (error) {
            console.error('Error parsing data:', error);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('✗ Disconnected from backend. Reconnecting...');
        updateQuote("connection lost... retrying", false);

        if (!reconnectInterval) {
            reconnectInterval = setInterval(() => {
                console.log('Attempting to reconnect...');
                connectWebSocket();
            }, 3000);
        }
    };
}

// ============================================================================
// UI UPDATE FUNCTIONS
// ============================================================================

function updateUI(data) {
    // Update attack mode state
    const wasAttackMode = isAttackMode;
    isAttackMode = data.attack_detected || false;

    // Switch modes
    if (isAttackMode !== wasAttackMode) {
        if (isAttackMode) {
            document.body.classList.remove('mode-normal');
            document.body.classList.add('mode-attack');
        } else {
            document.body.classList.remove('mode-attack');
            document.body.classList.add('mode-normal');
        }
    }

    // Update stats
    document.getElementById('stat-connections').textContent = data.total_connections || 0;
    document.getElementById('stat-unique-ips').textContent = data.unique_ips || 0;
    document.getElementById('stat-latency').textContent = `${data.latency || 0} ms`;
    document.getElementById('stat-packet-loss').textContent = `${(data.packet_loss || 0).toFixed(1)}%`;

    // Update threat level
    const threatEl = document.getElementById('stat-threat');
    threatEl.classList.remove('threat-normal', 'threat-warning', 'threat-attack');

    if (isAttackMode) {
        threatEl.textContent = 'ATTACK';
        threatEl.classList.add('threat-attack');
    } else if (data.threat_level === 'warning') {
        threatEl.textContent = 'WARNING';
        threatEl.classList.add('threat-warning');
    } else {
        threatEl.textContent = 'NORMAL';
        threatEl.classList.add('threat-normal');
    }

    // Update Pwnagotchi face
    updateFace(data);

    // Update connection log
    if (data.recent_connections) {
        updateConnectionLog(data.recent_connections);
    }

    // Update activity bars
    updateActivityBars(data.total_connections);

    // Update graphs
    updateGraphs(data.latency || 0, data.packet_loss || 0);
}

function updateFace(data) {
    const faceEl = document.getElementById('gotchi-face');

    if (data.attack_detected) {
        faceEl.textContent = FACES.ATTACK;
    } else if (data.total_connections > 50) {
        faceEl.textContent = FACES.INTENSE;
    } else if (data.total_connections > 20) {
        faceEl.textContent = FACES.COOL;
    } else if (data.total_connections > 0) {
        faceEl.textContent = FACES.HAPPY;
    } else {
        faceEl.textContent = FACES.BORED;
    }
}

function updateQuote(customQuote = null, checkAttack = true) {
    const quoteEl = document.getElementById('gotchi-quote');

    if (customQuote) {
        quoteEl.textContent = customQuote;
        return;
    }

    if (checkAttack && isAttackMode) {
        quoteEl.textContent = QUOTES_ATTACK[Math.floor(Math.random() * QUOTES_ATTACK.length)];
    } else {
        quoteEl.textContent = QUOTES_NORMAL[Math.floor(Math.random() * QUOTES_NORMAL.length)];
    }
}

function updateConnectionLog(connections) {
    if (!connections || connections.length === 0) return;

    const logEl = document.getElementById('connection-log');

    // Add new connections to the top
    connections.forEach(conn => {
        const isLocal = conn.remote_ip.startsWith('192.168.') ||
                       conn.remote_ip.startsWith('10.') ||
                       conn.remote_ip.startsWith('172.');

        const entry = document.createElement('div');
        entry.className = `log-entry ${isLocal ? 'local' : 'public'}`;

        const prefix = isLocal ? 'LOCAL' : 'REMOTE';
        entry.textContent = `${prefix} ${conn.remote_ip}:${conn.remote_port} → :${conn.local_port}`;

        // Add to top
        logEl.insertBefore(entry, logEl.firstChild);
    });

    // Keep only recent entries
    while (logEl.children.length > maxLogEntries) {
        logEl.removeChild(logEl.lastChild);
    }
}

function updateActivityBars(totalConnections) {
    // Shift data
    activityData.shift();
    activityData.push(totalConnections);

    // Update bar heights
    const bars = document.querySelectorAll('.activity-bar');
    bars.forEach((bar, index) => {
        const height = Math.min(150, Math.max(5, (activityData[index] / 10) * 150));
        bar.style.height = height + 'px';
    });
}

function updateTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('current-time').textContent = timeStr;
}

// ============================================================================
// GRAPHS
// ============================================================================

function updateGraphs(latency, packetLoss) {
    // Add to history
    latencyHistory.push(latency);
    packetLossHistory.push(packetLoss);

    // Keep only recent data
    if (latencyHistory.length > maxDataPoints) {
        latencyHistory.shift();
        packetLossHistory.shift();
    }

    // Draw both graphs
    drawGraph('latency-graph', latencyHistory, '#0F0', 200);
    drawGraph('packetloss-graph', packetLossHistory, '#F00', 100);
}

function drawGraph(canvasId, data, color, maxValue) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);

    if (data.length < 2) return;

    // Draw grid
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Draw data line
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.shadowBlur = 5;
    ctx.shadowColor = color;
    ctx.beginPath();

    const pointSpacing = width / (maxDataPoints - 1);

    data.forEach((value, index) => {
        const x = index * pointSpacing;
        const y = height - (value / maxValue) * height;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();
    ctx.shadowBlur = 0;
}

// ============================================================================
// START APPLICATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    init();
});
