#!/bin/sh
# One-time setup of a fresh Ubuntu EC2 instance: Docker Engine, Compose
# plugin and Git. Adds swap on instances with less than 3 GB of RAM so the
# dlib build does not run out of memory.
#
# Usage (on the EC2):  sh scripts/ec2-setup.sh   then log out and back in.
set -eu

sudo apt-get update
sudo apt-get install -y ca-certificates curl git

if ! command -v docker >/dev/null 2>&1; then
    curl -fsSL https://get.docker.com | sudo sh
fi
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

mem_mb=$(awk '/MemTotal/ {print int($2 / 1024)}' /proc/meminfo)
if [ "$mem_mb" -lt 3000 ] && [ ! -f /swapfile ]; then
    echo "RAM is ${mem_mb} MB: adding a 2 GB swap file for the dlib build."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

docker --version || true
sudo docker compose version
git --version
echo "Done. Log out and back in so the docker group applies to $USER."
