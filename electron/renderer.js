// Import Three.js from node_modules
const THREE = require('three');

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
// THREE.JS - 3D WIREFRAME SPHERE
// ============================================================================

const container = document.getElementById("canvas");
const canvasWidth = 300;
const canvasHeight = 300;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(canvasWidth, canvasHeight);
renderer.setClearColor(0x000000, 0);
container.appendChild(renderer.domElement);

const geometry = new THREE.SphereGeometry(2, 12, 12);
const material = new THREE.MeshBasicMaterial({
  color: 0x92ff38,
  wireframe: true,
  wireframeLinewidth: 2
});
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

camera.position.z = 5;

function animateSphere() {
  requestAnimationFrame(animateSphere);
  sphere.rotation.y += 0.008;
  renderer.render(scene, camera);
}
animateSphere();

// ============================================================================
// WEBSOCKET CONNECTION TO PYTHON BACKEND
// ============================================================================

let ws = null;
let reconnectInterval = null;
let isAttackMode = false;
let connectionLogEntries = [];
let maxLogEntries = 15;

// Network data storage
const maxDataPoints = 60;
let latencyData = [];
let packetLossData = [];
let timeLabels = [];

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

// Start connection
connectWebSocket();

// ============================================================================
// UI UPDATE FUNCTIONS
// ============================================================================

function updateUI(data) {
  // Update stats
  document.getElementById('stat-connections').textContent = data.total_connections || 0;
  document.getElementById('stat-unique-ips').textContent = data.unique_ips || 0;
  document.getElementById('stat-latency').textContent = `${data.latency || 0}ms`;
  document.getElementById('stat-packet-loss').textContent = `${data.packet_loss || 0}%`;

  // Update threat level
  const threatElement = document.getElementById('stat-threat');
  isAttackMode = data.attack_detected || false;

  if (isAttackMode) {
    threatElement.textContent = 'CRITICAL';
    threatElement.className = 'stat-value status-critical';
    document.getElementById('attack-warning').style.display = 'block';
  } else if (data.threat_level === 'warning') {
    threatElement.textContent = 'WARNING';
    threatElement.className = 'stat-value status-warning';
    document.getElementById('attack-warning').style.display = 'none';
  } else {
    threatElement.textContent = 'NORMAL';
    threatElement.className = 'stat-value status-normal';
    document.getElementById('attack-warning').style.display = 'none';
  }

  // Update Pwnagotchi face
  updateFace(data);

  // Update connection log
  if (data.recent_connections && data.recent_connections.length > 0) {
    updateConnectionLog(data.recent_connections);
  }

  // Update graphs
  if (data.latency !== undefined && data.packet_loss !== undefined) {
    updateGraphData(data.latency, data.packet_loss);
  }
}

function updateFace(data) {
  const faceElement = document.getElementById('gotchi-face');

  if (data.attack_detected) {
    faceElement.textContent = FACES.ATTACK;
  } else if (data.total_connections > 50) {
    faceElement.textContent = FACES.INTENSE;
  } else if (data.total_connections > 20) {
    faceElement.textContent = FACES.COOL;
  } else if (data.total_connections > 0) {
    faceElement.textContent = FACES.HAPPY;
  } else {
    faceElement.textContent = FACES.BORED;
  }
}

function updateQuote(customQuote = null, checkAttack = true) {
  const quoteElement = document.getElementById('gotchi-quote');

  if (customQuote) {
    quoteElement.textContent = customQuote;
    return;
  }

  if (checkAttack && isAttackMode) {
    quoteElement.textContent = QUOTES_ATTACK[Math.floor(Math.random() * QUOTES_ATTACK.length)];
  } else {
    quoteElement.textContent = QUOTES_NORMAL[Math.floor(Math.random() * QUOTES_NORMAL.length)];
  }
}

// Change quote every 5 seconds
setInterval(() => updateQuote(null, true), 5000);

function updateConnectionLog(connections) {
  const logElement = document.getElementById('connection-log');

  // Add new connections to the log
  connections.forEach(conn => {
    const isLocal = conn.remote_ip.startsWith('192.168.') ||
                   conn.remote_ip.startsWith('10.') ||
                   conn.remote_ip.startsWith('172.');

    const logClass = isLocal ? 'log-local' : 'log-public';
    const prefix = isLocal ? 'LOCAL' : 'PUBLIC';
    const entry = `→ ${prefix} ${conn.remote_ip}:${conn.remote_port} → :${conn.local_port}`;

    // Avoid duplicates
    if (!connectionLogEntries.includes(entry)) {
      connectionLogEntries.unshift(entry);

      // Keep only recent entries
      if (connectionLogEntries.length > maxLogEntries) {
        connectionLogEntries.pop();
      }
    }
  });

  // Render log
  logElement.innerHTML = connectionLogEntries
    .map(entry => {
      const isLocal = entry.includes('LOCAL');
      const logClass = isLocal ? 'log-local' : 'log-public';
      return `<div class="log-entry ${logClass}">${entry}</div>`;
    })
    .join('');

  // Auto-scroll to bottom
  logElement.scrollTop = logElement.scrollHeight;
}

// ============================================================================
// GRAPH RENDERING
// ============================================================================

const graphCanvas = document.getElementById('graph-canvas');
const graphCtx = graphCanvas.getContext('2d');

function updateGraphData(latency, packetLoss) {
  latencyData.push(latency);
  packetLossData.push(packetLoss);
  timeLabels.push(new Date().toLocaleTimeString());

  // Keep only recent data
  if (latencyData.length > maxDataPoints) {
    latencyData.shift();
    packetLossData.shift();
    timeLabels.shift();
  }

  drawGraph();
}

function drawGraph() {
  const width = graphCanvas.width;
  const height = graphCanvas.height;
  const padding = 40;
  const graphWidth = width - padding * 2;
  const graphHeight = height - padding * 2;

  // Clear canvas
  graphCtx.fillStyle = '#0a0d08';
  graphCtx.fillRect(0, 0, width, height);

  if (latencyData.length < 2) return;

  // Find max values for scaling
  const maxLatency = Math.max(...latencyData, 100);
  const maxPacketLoss = Math.max(...packetLossData, 10);

  // Draw grid
  graphCtx.strokeStyle = '#1b3a22';
  graphCtx.lineWidth = 1;
  for (let i = 0; i <= 5; i++) {
    const y = padding + (graphHeight / 5) * i;
    graphCtx.beginPath();
    graphCtx.moveTo(padding, y);
    graphCtx.lineTo(width - padding, y);
    graphCtx.stroke();
  }

  // Draw latency line (green)
  graphCtx.strokeStyle = '#00ff00';
  graphCtx.lineWidth = 2;
  graphCtx.shadowBlur = 5;
  graphCtx.shadowColor = '#00ff00';
  graphCtx.beginPath();

  latencyData.forEach((value, index) => {
    const x = padding + (graphWidth / (maxDataPoints - 1)) * index;
    const y = padding + graphHeight - (value / maxLatency) * graphHeight;

    if (index === 0) {
      graphCtx.moveTo(x, y);
    } else {
      graphCtx.lineTo(x, y);
    }
  });
  graphCtx.stroke();

  // Draw packet loss line (red)
  graphCtx.strokeStyle = '#ff3333';
  graphCtx.shadowColor = '#ff3333';
  graphCtx.beginPath();

  packetLossData.forEach((value, index) => {
    const x = padding + (graphWidth / (maxDataPoints - 1)) * index;
    const y = padding + graphHeight - (value / maxPacketLoss) * graphHeight;

    if (index === 0) {
      graphCtx.moveTo(x, y);
    } else {
      graphCtx.lineTo(x, y);
    }
  });
  graphCtx.stroke();

  // Draw labels
  graphCtx.shadowBlur = 0;
  graphCtx.fillStyle = '#95e208';
  graphCtx.font = '14px VT323';
  graphCtx.fillText('Latency (ms)', padding, 20);
  graphCtx.fillStyle = '#ff3333';
  graphCtx.fillText('Packet Loss (%)', padding + 150, 20);

  // Draw axis labels
  graphCtx.fillStyle = '#95e208';
  graphCtx.font = '12px VT323';
  graphCtx.fillText('0', padding - 20, height - padding + 5);
  graphCtx.fillText(maxLatency.toFixed(0), padding - 30, padding + 5);
}

// ============================================================================
// BUTTON HANDLERS
// ============================================================================

document.getElementById('btn-fullscreen').addEventListener('click', () => {
  const elem = document.documentElement;
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => {
      console.log(`Error attempting to enable fullscreen: ${err.message}`);
    });
  } else {
    document.exitFullscreen();
  }
});

document.getElementById('btn-start').addEventListener('click', () => {
  // Toggle monitoring (for future implementation)
  console.log('Monitoring toggle clicked');
});

// ============================================================================
// INITIALIZATION
// ============================================================================

console.log('DDoS Gotchi v3.0 - Electron Frontend Loaded');
updateQuote("booting system...", false);
