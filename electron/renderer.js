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
let connectionsByIP = new Map(); // Map<ip, {firstSeen, lastSeen, ports: Set, connCount, isLocal}>
let maxLogEntries = 50;
let connectionLogRefreshInterval = null;
let lastRefreshTime = 0;

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

// Track connections grouped by IP
function trackConnections(connections) {
    if (!connections || connections.length === 0) return;

    const now = Date.now();
    const currentIPs = new Set();

    connections.forEach(conn => {
        const ip = conn.remote_ip;
        currentIPs.add(ip);

        const isLocal = ip.startsWith('192.168.') ||
                       ip.startsWith('10.') ||
                       ip.startsWith('172.');

        if (!connectionsByIP.has(ip)) {
            // New IP
            connectionsByIP.set(ip, {
                firstSeen: now,
                lastSeen: now,
                ports: new Set([conn.remote_port]),
                localPorts: new Set([conn.local_port]),
                connCount: 1,
                isLocal: isLocal
            });
        } else {
            // Update existing IP
            const entry = connectionsByIP.get(ip);
            entry.lastSeen = now;
            entry.ports.add(conn.remote_port);
            entry.localPorts.add(conn.local_port);
            entry.connCount = connections.filter(c => c.remote_ip === ip).length;
        }
    });

    // Remove IPs not seen in last 30 seconds
    for (const [ip, entry] of connectionsByIP.entries()) {
        if (now - entry.lastSeen > 30000) {
            connectionsByIP.delete(ip);
        }
    }
}

// Refresh connection log every 4 seconds
function refreshConnectionLog() {
    const logEl = document.getElementById('connection-log');
    const totalIPsEl = document.getElementById('total-ips');
    const newIPsEl = document.getElementById('new-ips');

    const now = Date.now();

    // Sort IPs by most recent activity
    const sortedIPs = Array.from(connectionsByIP.entries())
        .sort((a, b) => b[1].lastSeen - a[1].lastSeen);

    // Count new IPs (first seen in last 4 seconds)
    const newCount = sortedIPs.filter(([ip, entry]) => (now - entry.firstSeen) < 4000).length;

    // Update summary
    totalIPsEl.textContent = `${sortedIPs.length} unique IP${sortedIPs.length !== 1 ? 's' : ''}`;
    newIPsEl.textContent = `${newCount} new`;
    newIPsEl.style.color = newCount > 0 ? '#F00' : '#0F0';

    // Clear and rebuild log
    logEl.innerHTML = '';

    sortedIPs.slice(0, maxLogEntries).forEach(([ip, entry]) => {
        const age = now - entry.firstSeen;
        const isNew = age < 4000;

        const ipEntry = document.createElement('div');

        // Red for new IPs, green for existing, cyan for local
        if (isNew) {
            ipEntry.className = `ip-entry new-connection ${entry.isLocal ? 'local' : 'public'}`;
        } else {
            ipEntry.className = `ip-entry ${entry.isLocal ? 'local' : 'public'}`;
        }

        // Create IP header
        const ipHeader = document.createElement('div');
        ipHeader.className = 'ip-header';

        const ipLabel = document.createElement('span');
        ipLabel.className = 'ip-label';
        const prefix = entry.isLocal ? 'LOCAL' : 'REMOTE';
        ipLabel.textContent = `${prefix}`;

        const ipAddress = document.createElement('span');
        ipAddress.className = 'ip-address';
        ipAddress.textContent = ip;

        const connCount = document.createElement('span');
        connCount.className = 'conn-count';
        connCount.textContent = `${entry.connCount} conn${entry.connCount !== 1 ? 's' : ''}`;

        ipHeader.appendChild(ipLabel);
        ipHeader.appendChild(ipAddress);
        ipHeader.appendChild(connCount);

        // Create port info
        const portInfo = document.createElement('div');
        portInfo.className = 'port-info';
        const portsArray = Array.from(entry.ports).slice(0, 5);
        const localPortsArray = Array.from(entry.localPorts).slice(0, 3);
        portInfo.textContent = `Ports: ${portsArray.join(', ')}${entry.ports.size > 5 ? '...' : ''} → ${localPortsArray.join(', ')}`;

        // Create timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'ip-timestamp';
        timestamp.textContent = `First seen: ${new Date(entry.firstSeen).toLocaleTimeString()}`;

        ipEntry.appendChild(ipHeader);
        ipEntry.appendChild(portInfo);
        ipEntry.appendChild(timestamp);

        logEl.appendChild(ipEntry);
    });

    lastRefreshTime = now;
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
// GRAPHS - KIBANA-STYLE INTERACTIVE GRAPHS
// ============================================================================

// Graph state for interactivity
const graphState = {
    latency: { hovering: false, hoverIndex: -1 },
    packetloss: { hovering: false, hoverIndex: -1 }
};

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
    drawInteractiveGraph('latency-graph', latencyHistory, '#0F0', 200, timestampHistory, 'latency');
    drawInteractiveGraph('packetloss-graph', packetLossHistory, '#F00', 100, timestampHistory, 'packetloss');
}

function drawInteractiveGraph(canvasId, data, color, maxValue, timestamps, graphKey) {
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

    const pointSpacing = width / (maxDataPoints - 1);

    // Draw enhanced grid with more lines
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.08)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 8; i++) {
        const y = (graphHeight / 8) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Draw vertical grid lines
    const verticalGridCount = 10;
    for (let i = 0; i <= verticalGridCount; i++) {
        const x = (width / verticalGridCount) * i;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, graphHeight);
        ctx.stroke();
    }

    // Fill area under the line
    ctx.fillStyle = color.replace(')', ', 0.1)').replace('rgb', 'rgba').replace('#0F0', 'rgba(0, 255, 0, 0.1)').replace('#F00', 'rgba(255, 0, 0, 0.1)');
    ctx.beginPath();
    ctx.moveTo(0, graphHeight);

    data.forEach((value, index) => {
        const x = index * pointSpacing;
        const y = graphHeight - (value / maxValue) * graphHeight;
        ctx.lineTo(x, y);
    });

    ctx.lineTo((data.length - 1) * pointSpacing, graphHeight);
    ctx.closePath();
    ctx.fill();

    // Draw data line
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

    // Draw enhanced time labels (more frequent)
    if (timestamps && timestamps.length > 0) {
        ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
        ctx.font = '9px Courier New';
        ctx.textAlign = 'center';

        // Smart time formatting - show more labels
        const labelCount = Math.min(6, data.length);
        const labelIndices = [];
        for (let i = 0; i < labelCount; i++) {
            labelIndices.push(Math.floor((data.length - 1) * (i / (labelCount - 1))));
        }

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

    // Draw crosshair and tooltip if hovering
    const state = graphState[graphKey];
    if (state && state.hovering && state.hoverIndex >= 0 && state.hoverIndex < data.length) {
        const hoverX = state.hoverIndex * pointSpacing;
        const hoverY = graphHeight - (data[state.hoverIndex] / maxValue) * graphHeight;

        // Draw vertical crosshair line
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(hoverX, 0);
        ctx.lineTo(hoverX, graphHeight);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw horizontal crosshair line
        ctx.beginPath();
        ctx.moveTo(0, hoverY);
        ctx.lineTo(width, hoverY);
        ctx.stroke();

        // Highlight the point
        ctx.fillStyle = color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
        ctx.beginPath();
        ctx.arc(hoverX, hoverY, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Draw tooltip
        const value = data[state.hoverIndex].toFixed(2);
        const timestamp = timestamps[state.hoverIndex];
        const timeStr = timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        const tooltipText = `${timeStr}: ${value}`;
        ctx.font = '11px Courier New';
        const textWidth = ctx.measureText(tooltipText).width;

        // Position tooltip above the point, adjust if near edges
        let tooltipX = hoverX - textWidth / 2 - 5;
        let tooltipY = hoverY - 35;

        // Keep tooltip within canvas bounds
        if (tooltipX < 0) tooltipX = 5;
        if (tooltipX + textWidth + 10 > width) tooltipX = width - textWidth - 15;
        if (tooltipY < 0) tooltipY = hoverY + 25;

        // Draw tooltip background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
        ctx.fillRect(tooltipX, tooltipY, textWidth + 10, 20);

        // Draw tooltip border
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        ctx.strokeRect(tooltipX, tooltipY, textWidth + 10, 20);

        // Draw tooltip text
        ctx.fillStyle = color;
        ctx.fillText(tooltipText, tooltipX + 5, tooltipY + 14);
    }

    // Setup mouse events (only once per canvas)
    if (!canvas.hasMouseEvents) {
        canvas.hasMouseEvents = true;

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            // Scale for canvas resolution
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const scaledX = mouseX * scaleX;

            // Find nearest data point
            const index = Math.round(scaledX / pointSpacing);

            if (index >= 0 && index < data.length) {
                graphState[graphKey].hovering = true;
                graphState[graphKey].hoverIndex = index;

                // Redraw to show tooltip
                if (graphKey === 'latency') {
                    drawInteractiveGraph(canvasId, latencyHistory, color, maxValue, timestamps, graphKey);
                } else {
                    drawInteractiveGraph(canvasId, packetLossHistory, color, maxValue, timestamps, graphKey);
                }
            }
        });

        canvas.addEventListener('mouseleave', () => {
            graphState[graphKey].hovering = false;
            graphState[graphKey].hoverIndex = -1;

            // Redraw without tooltip
            if (graphKey === 'latency') {
                drawInteractiveGraph(canvasId, latencyHistory, color, maxValue, timestamps, graphKey);
            } else {
                drawInteractiveGraph(canvasId, packetLossHistory, color, maxValue, timestamps, graphKey);
            }
        });

        // Add cursor style
        canvas.style.cursor = 'crosshair';
    }
}

// ============================================================================
// START APPLICATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    init();
});
