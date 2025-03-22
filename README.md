# VLC Sync Video Looper

![Sliver (1993)](https://www.joblo.com/wp-content/uploads/2018/05/sliver-199.jpg)

The VLC Sync Video Looper is a Python-based solution for synchronizing and looping videos across multiple devices using VLC Media Player. This project is ideal for creating synchronized video displays, such as multi-screen installations or video walls.

The script can operate in two modes:
- **Controller Mode**: Controls playback, synchronization across all connected worker devices and plays videos in sync.
- **Worker Mode**: Receives commands from the controller and plays videos in sync.

The script is installed as a systemd service, ensuring it starts automatically on boot.

---

## Features

- **Multi-Device Synchronization**: Synchronize video playback across multiple devices using VLC's remote control interface.
- **Automatic Startup**: The script runs as a systemd service, starting automatically when the device boots.
- **Flexible Configuration**: Easily configure controller and worker devices using a simple configuration file.
- **Looping Playback**: Videos are looped seamlessly for continuous playback.
- **Easy Video Management**: Videos and the configuration file are stored in `/media/videos`, making it simple to update or adjust the setup.

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

The script uses a configuration file (`loopvideos.conf`) to define its behavior. The file should be placed in `/media/videos` along with the video files.

### Sample Configuration File

```ini
# Mode of operation: "controller" or "worker"
MODE=controller

# Comma-separated list of worker devices with their IP addresses and RC ports
WORKERS=192.168.1.101:12345,192.168.1.102:12345
```

- **`MODE`**: Set to `controller` for the controlling device or `worker` for devices receiving commands.
- **`WORKERS`**: A list of worker devices (IP:port) that the controller will control.

---

## Video and Configuration File Management

- **Video File**: Place a single `.mp4` video file in the `/media/videos` directory. The script will automatically loop this file.
- **Configuration File**: The `loopvideos.conf` file should also be placed in `/media/videos`.

### Raspberry Pi Setup with an Additional Partition

For Raspberry Pi installations, you can create an additional **exFAT partition** on the SD card to store videos and the configuration file. This allows you to easily update the videos and configuration by inserting the SD card into a Mac or PC.

1. **Format the Partition**:
   - Use a partitioning tool (e.g., `gparted`) to create an exFAT partition on the SD card.
   - Mount the partition to `/media/videos`.

2. **Mount Automatically**:
   - Add an entry to `/etc/fstab` to ensure the partition is mounted to `/media/videos` on boot:
     ```fstab
     /dev/sdX1 /media/videos exfat defaults 0 0
     ```

---

## Troubleshooting

- **Service not starting**: Check the logs using:
  ```bash
  sudo journalctl -u vlc_sync_video_looper.service
  ```

- **Workers not reachable**: Ensure the IP addresses and ports in the configuration file are correct and that the devices are on the same network.

- **VLC not installed**: Install VLC using:
  ```bash
  sudo apt-get install -y vlc
  ```


