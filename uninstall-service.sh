#!/bin/bash
#
# DDoS Gotchi - Service Uninstallation Script
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root or with sudo${NC}"
    exit 1
fi

echo -e "${YELLOW}🗑️  Uninstalling DDoS Gotchi Service...${NC}\n"

# Stop service
if systemctl is-active --quiet ddosgotchi; then
    echo -e "${YELLOW}⏹️  Stopping service...${NC}"
    systemctl stop ddosgotchi
fi

# Disable service
if systemctl is-enabled --quiet ddosgotchi; then
    echo -e "${YELLOW}❌ Disabling service...${NC}"
    systemctl disable ddosgotchi
fi

# Remove systemd service
if [ -f /etc/systemd/system/ddosgotchi.service ]; then
    echo -e "${YELLOW}🗑️  Removing systemd service...${NC}"
    rm /etc/systemd/system/ddosgotchi.service
fi

# Reload systemd
echo -e "${YELLOW}🔄 Reloading systemd...${NC}"
systemctl daemon-reload

# Ask to remove installation directory
INSTALL_DIR="/opt/ddosgotchi"
if [ -d "$INSTALL_DIR" ]; then
    read -p "Remove installation directory $INSTALL_DIR? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  Removing $INSTALL_DIR...${NC}"
        rm -rf "$INSTALL_DIR"
    fi
fi

echo -e "\n${GREEN}✅ Uninstallation complete!${NC}\n"
