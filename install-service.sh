#!/bin/bash
#
# DDoS Gotchi - Service Installation Script
# Installs DDoS Gotchi as a systemd service
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root or with sudo${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Installing DDoS Gotchi Service...${NC}\n"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create installation directory
INSTALL_DIR="/opt/ddosgotchi"
echo -e "${YELLOW}📁 Creating installation directory: $INSTALL_DIR${NC}"
mkdir -p "$INSTALL_DIR"

# Copy files
echo -e "${YELLOW}📋 Copying application files...${NC}"
cp -r * "$INSTALL_DIR/"

# Create data directory
mkdir -p "$INSTALL_DIR/data"
chmod 755 "$INSTALL_DIR/data"

# Copy systemd service
echo -e "${YELLOW}⚙️  Installing systemd service...${NC}"
cp ddosgotchi.service /etc/systemd/system/

# Reload systemd
echo -e "${YELLOW}🔄 Reloading systemd...${NC}"
systemctl daemon-reload

# Enable service
echo -e "${YELLOW}✅ Enabling service...${NC}"
systemctl enable ddosgotchi.service

echo -e "\n${GREEN}✅ Installation complete!${NC}\n"
echo -e "You can now manage DDoS Gotchi with:"
echo -e "  ${YELLOW}sudo systemctl start ddosgotchi${NC}   - Start the service"
echo -e "  ${YELLOW}sudo systemctl stop ddosgotchi${NC}    - Stop the service"
echo -e "  ${YELLOW}sudo systemctl status ddosgotchi${NC}  - Check status"
echo -e "  ${YELLOW}sudo systemctl restart ddosgotchi${NC} - Restart the service"
echo -e "  ${YELLOW}sudo journalctl -u ddosgotchi -f${NC}  - View logs"
echo -e "\nAccess the dashboard at: ${GREEN}http://localhost:3000${NC}"
echo -e "API documentation at: ${GREEN}http://localhost:8000/docs${NC}\n"

# Ask to start now
read -p "Would you like to start the service now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start ddosgotchi
    echo -e "${GREEN}✅ Service started!${NC}"
fi
