#!/bin/bash

set -e

# Prompt for sudo password
echo "This script requires administrative privileges. Please enter your password."
sudo -v

# Variables
INSTALL_DIR="/opt/vlc_sync_video_looper"
SERVICE_NAME="vlc_sync_video_looper.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

# Stop and disable the systemd service
echo "Stopping and disabling the service..."
sudo systemctl stop "$SERVICE_NAME" || echo "Service not running."
sudo systemctl disable "$SERVICE_NAME" || echo "Service not enabled."

# Remove the systemd service file
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing the systemd service file..."
    sudo rm "$SERVICE_FILE"
else
    echo "Systemd service file not found."
fi

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Remove the installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing the installation directory..."
    sudo rm -rf "$INSTALL_DIR"
else
    echo "Installation directory not found."
fi

echo "Uninstallation complete."
