#!/bin/bash

echo "Uninstalling appman..."

echo "Stopping appman_api service..."
systemctl --user stop appman_api.service
systemctl --user disable appman_api.service

echo "Removing service file..."
rm -f $HOME/.config/systemd/user/appman_api.service

echo "Reloading systemd daemon..."
systemctl --user daemon-reload

echo "Removing installed files..."

APP_PATH="$HOME/.local/appman/"

if [[ -d "$APP_PATH" ]]; then
  rm -rf "$APP_PATH"
fi

echo "Killing any remaining appman_api processes (if any)..."
pkill -f "appman_api.sh"
pkill -f "$APP_PATH"

echo "removing appman binary"
rm -f $HOME/.local/bin/appman

echo "Uninstall complete."
