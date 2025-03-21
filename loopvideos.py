#!/usr/bin/env python3

# The script is designed to synchronize and play videos across multiple devices using VLC Media Player. It operates in either "master" or "slave" mode, determined by a configuration file. In master mode, it ensures all slave devices are reachable and running VLC before starting playback and synchronization, while in slave mode, it directly launches VLC with predefined settings.

import os
import time
import socket
import subprocess

CONFIG_FILE = "/media/videos4k/loopvideos.conf"
DEFAULT_MEDIA_DIR = "/media/videos4k/"
DEFAULT_RC_PORT = 12345


def get_first_mp4(directory):
    for file in sorted(os.listdir(directory)):
        if file.lower().endswith(".mp4") and not file.startswith("."):
            return os.path.join(directory, file)
    return None


DEFAULT_MEDIA_PATH = get_first_mp4(DEFAULT_MEDIA_DIR)
if not DEFAULT_MEDIA_PATH:
    print("No .mp4 file found in the directory. Exiting.")
    exit(1)

DEFAULT_SLAVE_COMMAND = [
    "vlc",
    DEFAULT_MEDIA_PATH,
    "--rc-host",
    f"0.0.0.0:{DEFAULT_RC_PORT}",
    "--fullscreen",
    "--loop",
    "--repeat",
    "--no-video-title",
]

# If config file does not exist, assume slave mode
if not os.path.isfile(CONFIG_FILE):
    print("No config found, running in default slave mode...")
    subprocess.run(DEFAULT_SLAVE_COMMAND)
    exit(0)

# Read configuration
config = {}
with open(CONFIG_FILE, "r") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key.strip()] = value.strip()

# Validate config
if "MODE" not in config or config["MODE"].lower() != "master":
    print("Config found, but not master mode. Running as slave...")
    subprocess.run(DEFAULT_SLAVE_COMMAND)
    exit(0)

if "SLAVES" not in config:
    print("No slaves defined in master mode. Exiting.")
    exit(1)

# Extract slave addresses
slave_addresses = config["SLAVES"].split(",")


def check_slave_reachability():
    reachable_slaves = []
    for slave in slave_addresses:
        ip, port = slave.split(":")
        port = int(port)

        try:
            sock = socket.create_connection((ip, port), timeout=2)
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "VLC media player" in response:
                print(f"Slave {ip}:{port} is reachable and running VLC.")
                reachable_slaves.append(slave)
            else:
                print(f"Slave {ip}:{port} is reachable but not running VLC.")
            sock.close()
        except Exception as e:
            print(f"Slave {ip}:{port} is unreachable: {e}")
    return reachable_slaves


# Wait until all slaves are reachable and running VLC
while True:
    reachable_slaves = check_slave_reachability()
    if len(reachable_slaves) == len(slave_addresses):
        break
    print("Not all slaves are reachable or running VLC. Retrying in 5 seconds...")
    time.sleep(5)

# Start master VLC
MASTER_RC_HOST = "127.0.0.42"
MASTER_COMMAND = [
    "vlc",
    DEFAULT_MEDIA_PATH,
    "--rc-host",
    MASTER_RC_HOST,
    "--fullscreen",
    "--loop",
    "--repeat",
    "--no-video-title",
]
print("Starting VLC master...")
subprocess.Popen(MASTER_COMMAND)

# Start vlcsync in background
VLCSYNC_COMMAND = ["/home/pi/vlcsync-venv/bin/vlcsync"]
for slave in reachable_slaves:
    VLCSYNC_COMMAND.extend(["--rc-host", slave])

print("Starting vlcsync...")
subprocess.Popen(VLCSYNC_COMMAND)

# Wait 5 seconds and send seek 0 command to first slave
first_slave_ip, first_slave_port = reachable_slaves[0].split(":")
print(f"Sending seek 0 command to {first_slave_ip}:{first_slave_port}...")
time.sleep(10)
subprocess.run(
    [
        "sh",
        "-c",
        f"{{ echo 'seek 0'; sleep 1; }} | telnet {first_slave_ip} {first_slave_port}",
    ]
)
