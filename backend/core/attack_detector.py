"""
Attack Detector - Detects and classifies DDoS attacks
"""

from typing import Dict, Optional
from collections import deque


class AttackDetector:
    """Advanced attack detection with classification"""

    def __init__(self):
        self.anomaly_scores = deque(maxlen=50)
        self.attack_history = deque(maxlen=100)

        # Default thresholds
        self.thresholds = {
            'happy': {'max_latency': 10, 'max_packet_loss': 1},
            'alert': {'max_latency': 50, 'max_packet_loss': 5},
            'under_attack': {'max_latency': 200, 'max_packet_loss': 20},
            'stressed': {'min_latency': 200, 'min_packet_loss': 20}
        }

    def detect(self, stats: Dict) -> Dict:
        """Detect attacks and classify them"""
        if not stats['connected']:
            return {
                'state': 'disconnected',
                'attack_detected': False,
                'attack_type': None,
                'anomaly_score': 0,
                'confidence': 0
            }

        latency = stats.get('avg_latency', 0)
        packet_loss = stats.get('avg_packet_loss', 0)

        # Determine state
        state = self._determine_state(latency, packet_loss)

        # Classify attack type
        attack_type = self._classify_attack(latency, packet_loss)

        # Calculate anomaly score
        anomaly_score = self._calculate_anomaly_score(stats)

        # Calculate confidence
        confidence = self._calculate_confidence(latency, packet_loss)

        return {
            'state': state,
            'attack_detected': attack_type is not None,
            'attack_type': attack_type,
            'anomaly_score': anomaly_score,
            'confidence': confidence
        }

    def _determine_state(self, latency: float, packet_loss: float) -> str:
        """Determine current state based on thresholds"""
        if latency < self.thresholds['happy']['max_latency'] and \
           packet_loss < self.thresholds['happy']['max_packet_loss']:
            return 'happy'

        elif latency < self.thresholds['alert']['max_latency'] and \
             packet_loss < self.thresholds['alert']['max_packet_loss']:
            return 'alert'

        elif latency < self.thresholds['under_attack']['max_latency'] and \
             packet_loss < self.thresholds['under_attack']['max_packet_loss']:
            return 'under_attack'

        else:
            return 'stressed'

    def _classify_attack(self, latency: float, packet_loss: float) -> Optional[str]:
        """Classify attack type based on patterns"""
        if packet_loss > 50:
            return "ICMP Flood / Network Saturation"
        elif packet_loss > 20 and latency > 200:
            return "UDP Flood Detected"
        elif latency > 500 and packet_loss < 10:
            return "SYN Flood / Resource Exhaustion"
        elif latency > 100 and packet_loss > 10:
            return "Mixed DDoS Attack"
        elif latency > 50:
            return "Network Congestion / Slow DDoS"

        return None

    def _calculate_anomaly_score(self, stats: Dict) -> float:
        """Calculate anomaly score"""
        score = 0.0

        baseline_lat = stats.get('baseline_latency', 0)
        current_lat = stats.get('avg_latency', 0)
        baseline_loss = stats.get('baseline_packet_loss', 0)
        current_loss = stats.get('avg_packet_loss', 0)

        if baseline_lat > 0:
            lat_deviation = (current_lat - baseline_lat) / baseline_lat
            score += min(lat_deviation * 30, 50)

        if baseline_loss >= 0:
            loss_deviation = current_loss - baseline_loss
            score += min(loss_deviation * 2, 50)

        self.anomaly_scores.append(score)
        return score

    def _calculate_confidence(self, latency: float, packet_loss: float) -> float:
        """Calculate detection confidence"""
        confidence = 0.0

        if latency > 200:
            confidence += 40
        elif latency > 100:
            confidence += 20
        elif latency > 50:
            confidence += 10

        if packet_loss > 20:
            confidence += 60
        elif packet_loss > 10:
            confidence += 30
        elif packet_loss > 5:
            confidence += 15

        return min(confidence, 100.0)
