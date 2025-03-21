# VLC Sync Video Looper

The VLC Sync Video Looper is a Python-based solution for synchronizing and looping videos across multiple devices using VLC Media Player. This project is ideal for creating synchronized video displays, such as multi-screen installations or video walls.

The script can operate in two modes:
- **Master Mode**: Controls playback and synchronization across all connected slave devices.
- **Slave Mode**: Receives commands from the master and plays videos in sync.

The script is installed as a systemd service, ensuring it starts automatically on boot.

---

## Features

- **Multi-Device Synchronization**: Synchronize video playback across multiple devices using VLC's remote control interface.
- **Automatic Startup**: The script runs as a systemd service, starting automatically when the device boots.
- **Flexible Configuration**: Easily configure master and slave devices using a simple configuration file.
- **Looping Playback**: Videos are looped seamlessly for continuous playback.

---

## Installation

To install the VLC Sync Video Looper, run the following command:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/dreerr/vlc_sync_video_looper/main/install.sh)"
```

This command will:
1. Install all required dependencies (Python, pip, git, etc.).
2. Clone the repository to `/opt/vlc_sync_video_looper`.
3. Set up a Python virtual environment and install the necessary Python libraries.
4. Create a systemd service to automatically start the script on boot.

---

## Configuration

The script uses a configuration file (`vlcsync.conf`) to define its behavior. The file should be placed in the same directory as the script or in a specified location.

### Sample Configuration File

```ini
# Mode of operation: "master" or "slave"
MODE=master

# Comma-separated list of slave devices with their IP addresses and RC ports
SLAVES=192.168.1.101:12345,192.168.1.102:12345
```

- **`MODE`**: Set to `master` for the controlling device or `slave` for devices receiving commands.
- **`SLAVES`**: A list of slave devices (IP:port) that the master will control.

---

## Usage

### Starting and Stopping the Service

- **Start the service**:
  ```bash
  sudo systemctl start vlc_sync_video_looper.service
  ```

- **Stop the service**:
  ```bash
  sudo systemctl stop vlc_sync_video_looper.service
  ```

- **Check the service status**:
  ```bash
  sudo systemctl status vlc_sync_video_looper.service
  ```

- **Enable the service to start on boot**:
  ```bash
  sudo systemctl enable vlc_sync_video_looper.service
  ```

- **Disable the service**:
  ```bash
  sudo systemctl disable vlc_sync_video_looper.service
  ```

---

## Requirements

- Raspberry Pi or any Linux-based system
- VLC Media Player installed on all devices
- Python 3.6 or later
- Network connectivity between master and slave devices

---

## Troubleshooting

- **Service not starting**: Check the logs using:
  ```bash
  sudo journalctl -u vlc_sync_video_looper.service
  ```

- **Slaves not reachable**: Ensure the IP addresses and ports in the configuration file are correct and that the devices are on the same network.

- **VLC not installed**: Install VLC using:
  ```bash
  sudo apt-get install -y vlc
  ```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Uninstallation

To completely remove the VLC Sync Video Looper:

1. Stop and disable the service:
   ```bash
   sudo systemctl stop vlc_sync_video_looper.service
   sudo systemctl disable vlc_sync_video_looper.service
   ```

2. Remove the service file:
   ```bash
   sudo rm /etc/systemd/system/vlc_sync_video_looper.service
   sudo systemctl daemon-reload
   ```

3. Delete the installation directory:
   ```bash
   sudo rm -rf /opt/vlc_sync_video_looper
   ```

---

## Acknowledgments

Inspired by the [Adafruit Pi Video Looper](https://github.com/adafruit/pi_video_looper) project.