#!/usr/bin/env python3

# The script is designed to synchronize and play videos across multiple devices using VLC Media Player. It operates in either "controller" or "worker" mode, determined by a configuration file. In controller mode, it ensures all worker devices are reachable and running VLC before starting playback and synchronization, while in worker mode, it directly launches VLC with predefined settings.

import os
import time
import socket
import subprocess
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="VLC Sync Video Looper")
parser.add_argument(
    "--media-dir",
    type=str,
    default="/media/videos/",
    help="Directory containing video files (default: /media/videos/)",
)
parser.add_argument(
    "--rc-port",
    type=int,
    default=12345,
    help="Default RC port for VLC (default: 12345)",
)
args = parser.parse_args()

DEFAULT_MEDIA_DIR = args.media_dir
DEFAULT_RC_PORT = args.rc_port
CONFIG_FILE = os.path.join(DEFAULT_MEDIA_DIR, "video_looper.conf")


def get_first_mp4(directory):
    for file in sorted(os.listdir(directory)):
        if file.lower().endswith(".mp4") and not file.startswith("."):
            return os.path.join(directory, file)
    return None


# Update DEFAULT_MEDIA_PATH to use the new DEFAULT_MEDIA_DIR
DEFAULT_MEDIA_PATH = get_first_mp4(DEFAULT_MEDIA_DIR)
if not DEFAULT_MEDIA_PATH:
    print("No .mp4 file found in the directory. Exiting.")
    exit(1)

DEFAULT_WORKER_COMMAND = [
    "vlc",
    DEFAULT_MEDIA_PATH,
    "--rc-host",
    f"0.0.0.0:{DEFAULT_RC_PORT}",
    "--fullscreen",
    "--loop",
    "--repeat",
    "--no-video-title",
]

# If config file does not exist, assume worker mode
if not os.path.isfile(CONFIG_FILE):
    print("No config found, running in default worker mode...")
    subprocess.run(DEFAULT_WORKER_COMMAND)
    exit(0)

# Read configuration
config = {}
with open(CONFIG_FILE, "r") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key.strip()] = value.strip()

# Extract VLC flags if provided
vlc_flags = config.get("VLC_FLAGS", "").split()

DEFAULT_WORKER_COMMAND = DEFAULT_WORKER_COMMAND + vlc_flags

# Validate config
if "MODE" not in config or config["MODE"].lower() != "controller":
    print("Config found, but not controller mode. Running as worker...")
    subprocess.run(DEFAULT_WORKER_COMMAND)
    exit(0)

if "WORKERS" not in config:
    print("No workers defined in controller mode. Exiting.")
    exit(1)

# Extract worker addresses
worker_addresses = config["WORKERS"].split(",")


def check_worker_reachability():
    reachable_workers = []
    for worker in worker_addresses:
        ip, port = worker.split(":")
        port = int(port)

        try:
            sock = socket.create_connection((ip, port), timeout=2)
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "VLC media player" in response:
                print(f"Worker {ip}:{port} is reachable and running VLC.")
                reachable_workers.append(worker)
            else:
                print(f"Worker {ip}:{port} is reachable but not running VLC.")
            sock.close()
        except Exception as e:
            print(f"Worker {ip}:{port} is unreachable: {e}")
    return reachable_workers


# Wait until all workers are reachable and running VLC
while True:
    reachable_workers = check_worker_reachability()
    if len(reachable_workers) == len(worker_addresses):
        break
    print("Not all workers are reachable or running VLC. Retrying in 5 seconds...")
    time.sleep(5)

# Start controller VLC
CONTROLLER_RC_HOST = "127.0.0.42"
CONTROLLER_COMMAND = [
    "vlc",
    DEFAULT_MEDIA_PATH,
    "--rc-host",
    f"{CONTROLLER_RC_HOST}:{DEFAULT_RC_PORT}",
    "--fullscreen",
    "--loop",
    "--repeat",
    "--no-video-title",
] + vlc_flags
print("Starting VLC controller...")
subprocess.Popen(CONTROLLER_COMMAND)

# Start vlcsync in background
VLCSYNC_COMMAND = ["/opt/vlc_sync_video_looper/venv/bin/vlcsync"]
for worker in reachable_workers:
    VLCSYNC_COMMAND.extend(["--rc-host", worker])

print("Starting vlcsync...")
subprocess.Popen(VLCSYNC_COMMAND)

# Wait 5 seconds and send seek 0 command to first worker
first_worker_ip, first_worker_port = reachable_workers[0].split(":")
print(f"Sending seek 0 command to {first_worker_ip}:{first_worker_port}...")
time.sleep(10)
subprocess.run(
    [
        "sh",
        "-c",
        f"{{ echo 'seek 0'; sleep 1; }} | telnet {first_worker_ip} {first_worker_port}",
    ]
)
