#!/usr/bin/env bash
# Run this from your Mac to copy data files and trigger a redeploy on the Proxmox VM.
#
# Usage:
#   bash scripts/deploy.sh
set -euo pipefail

LXC_HOST="root@192.168.1.205"
APP_DIR="/opt/kela-quiz"

echo "==> Copying data files to LXC..."
scp data/*.json "${LXC_HOST}:${APP_DIR}/data/"

echo "==> Pulling latest code on LXC..."
ssh "$LXC_HOST" "cd ${APP_DIR} && git pull"

echo "==> Rebuilding and restarting app on LXC..."
ssh "$LXC_HOST" "cd ${APP_DIR} && docker compose up -d --build"

echo ""
echo "Deployed! App available at: http://192.168.1.205:8080"
