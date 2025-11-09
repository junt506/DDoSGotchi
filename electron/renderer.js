// ============================================================================
// DDOS GOTCHI v3.0 - Neural Nexus HUD Renderer
// ============================================================================

import { NeuralNexusVisualization } from './visualization.js';

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
let visualization = null;

// Graph data storage
const maxDataPoints = 120; // Increased for smoother graphs
let latencyHistory = [];
let packetLossHistory = [];
let timestampHistory = [];

// Connection tracking - refresh every 4 seconds
let allConnections = new Map(); // Map<connectionId, {conn, timestamp, isNew}>
let maxLogEntries = 50;
let connectionLogRefreshInterval = null;

// Activity bars
let activityData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// ============================================================================
// INITIALIZATION
// ============================================================================

function init() {
    console.log('DDoS Gotchi v3.0 - Neural Nexus Initializing...');

    // Initialize Neural Nexus visualization
    const centerDisplay = document.getElementById('center-display');
    visualization = new NeuralNexusVisualization(centerDisplay);
    console.log('✓ Neural Nexus visualization initialized');

    // Generate activity bars
    generateActivityBars();

    // Connect to backend
    connectWebSocket();

    // Start periodic updates
    setInterval(updateTime, 1000);
    setInterval(() => updateQuote(null, true), 5000);

    // Connection log refresh every 4 seconds
    connectionLogRefreshInterval = setInterval(refreshConnectionLog, 4000);

    // Set initial mode
    document.body.classList.add('mode-normal');

    console.log('Initialization complete');
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

    // Update visualization attack state
    if (visualization) {
        visualization.setAttackMode(isAttackMode);
    }

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

    // Update network info
    if (data.network_info) {
        document.getElementById('stat-my-ip').textContent = data.network_info.local_ip || '0.0.0.0';
        document.getElementById('stat-gateway').textContent = data.network_info.gateway || '0.0.0.0';
        document.getElementById('stat-network').textContent = data.network_info.network || '0.0.0.0/24';
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

    // Track connections
    if (data.recent_connections) {
        trackConnections(data.recent_connections);
    }

    // Update activity bars
    updateActivityBars(data.total_connections);

    // Update graphs (faster for smoother display)
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

// Track connections with timestamps
function trackConnections(connections) {
    if (!connections || connections.length === 0) return;

    const now = Date.now();

    connections.forEach(conn => {
        const connectionId = `${conn.remote_ip}:${conn.remote_port}`;

        if (!allConnections.has(connectionId)) {
            // New connection
            allConnections.set(connectionId, {
                conn: conn,
                timestamp: now,
                isNew: true
            });
        }
    });

    // Remove old connections (older than 30 seconds)
    for (const [id, entry] of allConnections.entries()) {
        if (now - entry.timestamp > 30000) {
            allConnections.delete(id);
        }
    }
}

// Refresh connection log every 4 seconds
function refreshConnectionLog() {
    const logEl = document.getElementById('connection-log');
    logEl.innerHTML = ''; // Clear log

    const now = Date.now();
    const sortedConnections = Array.from(allConnections.entries())
        .sort((a, b) => b[1].timestamp - a[1].timestamp); // Newest first

    sortedConnections.slice(0, maxLogEntries).forEach(([connectionId, entry]) => {
        const conn = entry.conn;
        const age = now - entry.timestamp;
        const isNew = age < 4000; // New if less than 4 seconds old

        const isLocal = conn.remote_ip.startsWith('192.168.') ||
                       conn.remote_ip.startsWith('10.') ||
                       conn.remote_ip.startsWith('172.');

        const logEntry = document.createElement('div');

        // Red for new connections, green for existing
        if (isNew) {
            logEntry.className = `log-entry new-connection ${isLocal ? 'local' : 'public'}`;
        } else {
            logEntry.className = `log-entry ${isLocal ? 'local' : 'public'}`;
        }

        const prefix = isLocal ? 'LOCAL' : 'REMOTE';
        const timestamp = new Date(entry.timestamp).toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${prefix} ${conn.remote_ip}:${conn.remote_port} → :${conn.local_port}`;

        logEl.appendChild(logEntry);

        // Mark as not new after first display
        entry.isNew = false;
    });
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
// GRAPHS - FASTER UPDATE FOR SMOOTHER DISPLAY
// ============================================================================

function updateGraphs(latency, packetLoss) {
    // Add to history
    const now = new Date();
    latencyHistory.push(latency);
    packetLossHistory.push(packetLoss);
    timestampHistory.push(now);

    // Keep only recent data (increased to 120 points for smoother curves)
    if (latencyHistory.length > maxDataPoints) {
        latencyHistory.shift();
        packetLossHistory.shift();
        timestampHistory.shift();
    }

    // Draw both graphs
    drawGraph('latency-graph', latencyHistory, '#0F0', 200, timestampHistory);
    drawGraph('packetloss-graph', packetLossHistory, '#F00', 100, timestampHistory);
}

function drawGraph(canvasId, data, color, maxValue, timestamps) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 20;
    const graphHeight = height - padding;

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);

    if (data.length < 2) return;

    // Draw grid
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (graphHeight / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Fill area under the line for smoother look
    ctx.fillStyle = color.replace(')', ', 0.1)').replace('rgb', 'rgba').replace('#0F0', 'rgba(0, 255, 0, 0.1)').replace('#F00', 'rgba(255, 0, 0, 0.1)');
    ctx.beginPath();

    const pointSpacing = width / (maxDataPoints - 1);

    // Start from bottom left
    ctx.moveTo(0, graphHeight);

    // Draw curve
    data.forEach((value, index) => {
        const x = index * pointSpacing;
        const y = graphHeight - (value / maxValue) * graphHeight;
        ctx.lineTo(x, y);
    });

    // Complete the area
    ctx.lineTo((data.length - 1) * pointSpacing, graphHeight);
    ctx.closePath();
    ctx.fill();

    // Draw data line on top
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.shadowBlur = 5;
    ctx.shadowColor = color;
    ctx.beginPath();

    data.forEach((value, index) => {
        const x = index * pointSpacing;
        const y = graphHeight - (value / maxValue) * graphHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();
    ctx.shadowBlur = 0;

    // Draw time labels
    if (timestamps && timestamps.length > 0) {
        ctx.fillStyle = 'rgba(0, 255, 0, 0.6)';
        ctx.font = '9px Courier New';
        ctx.textAlign = 'center';

        // Show labels at start, middle, and end
        const labelIndices = [0, Math.floor(data.length / 2), data.length - 1];

        labelIndices.forEach(index => {
            if (index < timestamps.length) {
                const x = index * pointSpacing;
                const time = timestamps[index].toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                ctx.fillText(time, x, height - 5);
            }
        });
    }
}

// ============================================================================
// START APPLICATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    init();
});
