#!/bin/bash

set -e

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root. Use sudo to run it."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
apt-get update
apt-get install -y python3 python3-venv python3-pip git

# Variables
REPO_URL="https://github.com/dreerr/pi_vlc_video_looper.git"
INSTALL_DIR="/opt/vlc_sync_video_looper"
SCRIPT_NAME="loopvideos.py"
SERVICE_NAME="vlc_sync_video_looper.service"
VENV_DIR="$INSTALL_DIR/venv"

# Clone the repository
echo "Cloning the repository..."
rm -rf "$INSTALL_DIR"
git clone "$REPO_URL" "$INSTALL_DIR"
chown -R "$USER":"$USER" "$INSTALL_DIR"

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
cat > "$SERVICE_FILE" <<EOL
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
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo "Installation complete. The service is running."