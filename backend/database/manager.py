"""
Database Manager - SQLite database for persistent storage
"""

import aiosqlite
import json
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database for storing statistics and attacks"""

    def __init__(self, db_path: str = "ddosgotchi.db"):
        self.db_path = db_path
        self.db = None

    async def init_db(self):
        """Initialize database and create tables"""
        self.db = await aiosqlite.connect(self.db_path)

        # Create stats table
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                connected BOOLEAN,
                latency REAL,
                packet_loss REAL,
                state TEXT,
                anomaly_score REAL
            )
        ''')

        # Create attacks table
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                attack_type TEXT,
                latency REAL,
                packet_loss REAL,
                anomaly_score REAL,
                confidence REAL,
                severity TEXT
            )
        ''')

        await self.db.commit()
        print("✅ Database initialized")

    async def log_stats(self, stats: Dict, state: str, anomaly_score: float):
        """Log network statistics"""
        await self.db.execute('''
            INSERT INTO stats (connected, latency, packet_loss, state, anomaly_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            stats['connected'],
            stats.get('latency', 0),
            stats.get('packet_loss', 0),
            state,
            anomaly_score
        ))
        await self.db.commit()

    async def log_attack(self, attack_info: Dict):
        """Log detected attack"""
        await self.db.execute('''
            INSERT INTO attacks (attack_type, latency, packet_loss, anomaly_score, confidence, severity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            attack_info.get('attack_type'),
            attack_info.get('latency', 0),
            attack_info.get('packet_loss', 0),
            attack_info.get('anomaly_score', 0),
            attack_info.get('confidence', 0),
            attack_info.get('severity', 'unknown')
        ))
        await self.db.commit()

    async def get_stats_history(self, limit: int = 100) -> List[Dict]:
        """Get historical statistics"""
        cursor = await self.db.execute('''
            SELECT * FROM stats
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = await cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    async def get_recent_attacks(self, hours: int = 24) -> List[Dict]:
        """Get recent attacks"""
        cutoff = datetime.now() - timedelta(hours=hours)

        cursor = await self.db.execute('''
            SELECT * FROM attacks
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (cutoff,))

        rows = await cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    async def close(self):
        """Close database connection"""
        if self.db:
            await self.db.close()
