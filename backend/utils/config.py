"""
Configuration settings using Pydantic
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Database
    database_url: str = "sqlite:///./ddosgotchi.db"

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]

    # Monitoring
    monitor_interval: int = 2  # seconds
    history_size: int = 60

    # Thresholds
    threshold_happy_latency: float = 10.0
    threshold_happy_packet_loss: float = 1.0
    threshold_alert_latency: float = 50.0
    threshold_alert_packet_loss: float = 5.0
    threshold_attack_latency: float = 200.0
    threshold_attack_packet_loss: float = 20.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
