// ============================================================================
// DDOS GOTCHI v3.0 - HUD RENDERER
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
    SLEEPING: "(◡_◡)",
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
    "standing guard...",
    "pattern matching...",
];

const QUOTES_ATTACK = [
    "ATTACK DETECTED!",
    "network under siege!",
    "defensive mode activated",
    "repelling intruders!",
    "threat neutralization active",
    "shields up! engaging...",
];

// ============================================================================
// STATE VARIABLES
// ============================================================================

let ws = null;
let reconnectInterval = null;
let isAttackMode = false;
let connectionHistory = [];
let packetLossHistory = [];
let connectionsPerSecond = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
let currentQuote = QUOTES_NORMAL[0];

// ============================================================================
// DYNAMIC ELEMENT GENERATION (from original CodePen)
// ============================================================================

function initializeElements() {
    // Generate blinking numbers for #a3 (connection ports/IPs)
    const a3 = document.getElementById('a3');
    for (let i = 1; i < 11; i++) {
        const span = document.createElement('span');
        span.className = 'a3' + i;
        span.style.animation = `pulse ${1 + Math.random()}s ease-in-out infinite`;
        a3.appendChild(span);
    }

    // Generate activity bars for #a4
    const a4 = document.getElementById('a4');
    for (let i = 1; i < 31; i++) {
        const span = document.createElement('span');
        span.className = 'a4' + i;
        a4.appendChild(span);
    }

    // Generate connection indicators for #a5
    const a5 = document.getElementById('a5');
    for (let i = 1; i < 16; i++) {
        const span = document.createElement('span');
        const b = document.createElement('b');
        b.className = 'a5' + i;
        b.style.animation = `blink ${1 + i * 0.1}s linear infinite`;
        span.appendChild(b);
        a5.appendChild(span);
    }

    // Generate grid lines for #a8 (packet loss graph)
    const a8 = document.getElementById('a8');
    for (let i = 1; i < 41; i++) {
        const span = document.createElement('span');
        a8.appendChild(span);
    }

    // Generate rotating tick marks for #f2
    const f2 = document.getElementById('f2');
    for (let i = 1; i < 37; i++) {
        const span = document.createElement('span');
        span.className = 'f2' + i;
        span.style.transform = `rotateZ(${i * 10}deg) translateY(190px)`;
        f2.appendChild(span);
    }

    // Generate inner rotating numbers for #f5
    const f5 = document.getElementById('f5');
    for (let i = 1; i < 19; i++) {
        const span = document.createElement('span');
        const b = document.createElement('b');
        b.textContent = Math.floor(Math.random() * 30);
        span.appendChild(b);
        span.className = 'f5' + i;
        span.style.transform = `rotateZ(${i * 20}deg) translateY(80px)`;
        f5.appendChild(span);
    }

    // Generate outer ring markers for #f1
    const f1 = document.getElementById('f1');
    for (let i = 1; i < 13; i++) {
        const span = document.createElement('span');
        span.className = 'f1' + i;
        span.style.transform = `rotateZ(${i * 30}deg) translateY(182px)`;
        f1.appendChild(span);
    }

    console.log('UI elements initialized');
}

// ============================================================================
// WEBSOCKET CONNECTION
// ============================================================================

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
        console.log('Connected to DDoS Gotchi backend');
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
            console.error('Error parsing WebSocket data:', error);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('Disconnected from backend. Reconnecting...');
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
    isAttackMode = data.attack_detected || false;

    // Update body class for global color changes
    if (isAttackMode) {
        document.body.classList.add('attack-mode');
        document.getElementById('container').classList.remove('normal', 'warning');
        document.getElementById('container').classList.add('attack');
    } else if (data.threat_level === 'warning') {
        document.body.classList.remove('attack-mode');
        document.getElementById('container').classList.remove('normal', 'attack');
        document.getElementById('container').classList.add('warning');
    } else {
        document.body.classList.remove('attack-mode');
        document.getElementById('container').classList.remove('warning', 'attack');
        document.getElementById('container').classList.add('normal');
    }

    // Update network load bar (#a1 - top progress bar)
    const networkLoad = Math.min(100, (data.total_connections / 100) * 100);
    document.getElementById('a11').style.width = networkLoad + '%';

    // Update latency gauge (#a2 - rotating needle)
    const latencyAngle = Math.min(180, (data.latency / 200) * 180);
    document.getElementById('a21').style.transform = `rotateZ(${latencyAngle}deg) translateY(50%)`;

    // Update connection ports/IPs display (#a3)
    updateConnectionNumbers(data.recent_connections);

    // Update connection activity bars (#a4)
    updateActivityBars(data.total_connections);

    // Update network stats panel (#a7)
    document.getElementById('stat-connections').textContent = data.total_connections || 0;
    document.getElementById('stat-unique-ips').textContent = data.unique_ips || 0;

    const threatEl = document.getElementById('stat-threat');
    if (isAttackMode) {
        threatEl.textContent = 'ATTACK';
        threatEl.className = 'attack';
    } else if (data.threat_level === 'warning') {
        threatEl.textContent = 'WARN';
        threatEl.className = 'warning';
    } else {
        threatEl.textContent = 'SAFE';
        threatEl.className = 'safe';
    }

    // Update packet loss graph (#a8)
    const packetLossPercent = data.packet_loss || 0;
    const graphHeight = Math.min(320, (packetLossPercent / 100) * 320);
    document.getElementById('a81').style.height = graphHeight + 'px';

    // Update live IP addresses (#a9)
    updateLiveIPs(data.recent_connections);

    // Update threat level bar and quote (#a10)
    const threatWidth = isAttackMode ? 200 : Math.min(200, (data.total_connections / 50) * 200);
    const threatBar = document.getElementById('threat-bar');
    threatBar.style.width = threatWidth + 'px';

    if (isAttackMode) {
        threatBar.style.background = '#F00';
    } else if (data.threat_level === 'warning') {
        threatBar.style.background = '#FC0';
    } else {
        threatBar.style.background = '#666';
    }

    // Update connections per second bar graph (#b1)
    updateConnectionsBars(data.total_connections);

    // Update 3D figure info panel
    document.getElementById('fig-latency').textContent = data.latency || 0;
    document.getElementById('fig-packet-loss').textContent = packetLossPercent.toFixed(1);

    // Update Pwnagotchi face
    updateFace(data);

    // Update connection log
    if (data.recent_connections && data.recent_connections.length > 0) {
        updateConnectionLog(data.recent_connections);
    }

    // Update current time
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleTimeString();
}

function updateConnectionNumbers(connections) {
    if (!connections || connections.length === 0) return;

    const spans = document.querySelectorAll('#a3 span');
    spans.forEach((span, index) => {
        if (connections[index]) {
            // Show last octet of IP or port number
            const conn = connections[index];
            const parts = conn.remote_ip.split('.');
            span.textContent = parts[3] || conn.remote_port;
        } else {
            span.textContent = Math.floor(Math.random() * 999);
        }
    });
}

function updateActivityBars(totalConnections) {
    const bars = document.querySelectorAll('#a4 span');
    bars.forEach((bar) => {
        const width = Math.random() * 15;
        bar.style.width = width + 'px';
    });
}

function updateLiveIPs(connections) {
    if (!connections || connections.length === 0) return;

    const segments = document.querySelectorAll('#a9 .ip-segment');

    // Show latest IP address parts
    if (connections[0]) {
        const ip = connections[0].remote_ip;
        const parts = ip.split('.');

        if (parts.length === 4) {
            segments[0].textContent = parts[0];
            segments[1].textContent = parts[1];
            segments[2].textContent = parts[2];
            segments[3].textContent = parts[3];
            segments[4].textContent = connections[0].remote_port;

            // Color code based on local vs public
            const isLocal = ip.startsWith('192.168.') || ip.startsWith('10.') || ip.startsWith('172.');
            segments.forEach(seg => {
                seg.className = isLocal ? 'ip-segment local-ip' : 'ip-segment public-ip';
            });
        }
    }
}

function updateConnectionsBars(totalConnections) {
    // Shift history
    connectionsPerSecond.shift();
    connectionsPerSecond.push(totalConnections);

    // Update bar heights
    const bars = document.querySelectorAll('#b1 span');
    bars.forEach((bar, index) => {
        const height = Math.min(100, (connectionsPerSecond[index] / 10) * 100);
        bar.style.height = height + 'px';
    });
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
    const quoteEl = document.getElementById('threat-quote');

    if (customQuote) {
        quoteEl.textContent = customQuote;
        currentQuote = customQuote;
        return;
    }

    if (checkAttack && isAttackMode) {
        currentQuote = QUOTES_ATTACK[Math.floor(Math.random() * QUOTES_ATTACK.length)];
    } else {
        currentQuote = QUOTES_NORMAL[Math.floor(Math.random() * QUOTES_NORMAL.length)];
    }

    quoteEl.textContent = currentQuote;
}

function updateConnectionLog(connections) {
    const logEl = document.getElementById('connection-log');

    // Add new connections to log
    connections.forEach(conn => {
        const isLocal = conn.remote_ip.startsWith('192.168.') ||
                       conn.remote_ip.startsWith('10.') ||
                       conn.remote_ip.startsWith('172.');

        const logClass = isLocal ? 'local' : 'public';
        const prefix = isLocal ? 'LOCAL' : 'REMOTE';

        const entry = document.createElement('div');
        entry.className = `log-entry ${logClass}`;
        entry.textContent = `${prefix} ${conn.remote_ip}:${conn.remote_port}`;

        // Add to top of log
        logEl.insertBefore(entry, logEl.firstChild);

        // Keep only last 20 entries
        while (logEl.children.length > 20) {
            logEl.removeChild(logEl.lastChild);
        }
    });
}

// ============================================================================
// PERIODIC UPDATES
// ============================================================================

// Change quote every 5 seconds
setInterval(() => {
    updateQuote(null, true);
}, 5000);

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('DDoS Gotchi v3.0 - HUD Interface Loaded');

    // Initialize all UI elements
    initializeElements();

    // Connect to backend
    connectWebSocket();

    // Set initial quote
    updateQuote("booting system...", false);

    console.log('Initialization complete');
});
