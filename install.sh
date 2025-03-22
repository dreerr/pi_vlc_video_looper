#!/bin/bash

set -e

# Prompt for sudo password
echo "This script requires administrative privileges. Please enter your password."
sudo -v

# Install required packages
echo "Installing required packages..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip git vlc

# Variables
REPO_URL="https://github.com/dreerr/pi_vlc_video_looper.git"
INSTALL_DIR="/opt/vlc_sync_video_looper"
SCRIPT_NAME="video_looper.py"
SERVICE_NAME="vlc_sync_video_looper.service"
VENV_DIR="$INSTALL_DIR/venv"

# Clone the repository
echo "Cloning the repository..."
sudo git clone "$REPO_URL" "$INSTALL_DIR"
sudo chown -R "$USER":"$USER" "$INSTALL_DIR"

# Create Python virtual environment and install dependencies
echo "Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# Create systemd service file
echo "Creating systemd service file..."
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=VLC Sync Video Looper (Controller/Worker)
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $INSTALL_DIR/$SCRIPT_NAME
WorkingDirectory=$INSTALL_DIR
Restart=always
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo "Installation complete. The service is running."
