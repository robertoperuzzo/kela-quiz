#!/usr/bin/env bash
# Run this script INSIDE the LXC as root after first boot.
# It installs Docker, clones the repo, and starts the app.
#
# Usage:
#   bash lxc-setup.sh
set -euo pipefail

REPO_URL="https://github.com/robertoperuzzo/kela-quiz.git"
APP_DIR="/opt/kela-quiz"

echo "==> Updating packages..."
apt-get update -qq && apt-get upgrade -y -qq

echo "==> Installing dependencies..."
apt-get install -y -qq curl git ca-certificates gnupg

echo "==> Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker

echo "==> Cloning repository..."
git clone "$REPO_URL" "$APP_DIR"
cd "$APP_DIR"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy data JSON files to the LXC (run this from your Mac):"
echo "       scp data/*.json root@192.168.1.205:$APP_DIR/data/"
echo ""
echo "  2. Then start the app:"
echo "       cd $APP_DIR && docker compose up -d"
echo ""
echo "  3. App will be available at: http://192.168.1.205:8080"
