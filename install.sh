#!/bin/bash

APP_PATH="$HOME/.local/appman"

echo "The appman application will be installed in $HOME/.local/appman"
echo "The binary will be installed in $HOME/.local/bin/appman"
echo "The appman_api service will be installed in $HOME/.config/systemd/user/appman_api.service"

echo "creating app root directory"
mkdir $APP_PATH

echo "creating logger directory"
mkdir $APP_PATH/logger

echo "adding python environment"
cp ./requirements.txt $APP_PATH/requirements.txt
python3 -m venv $APP_PATH/venv

echo "adding appman binary"
cp ./bin/appman $HOME/.local/bin/appman
chmod u+x $HOME/.local/bin/appman

echo "adding appman_api files"
mkdir $APP_PATH/api
cp ./api/appman_api.sh $APP_PATH/api/appman_api.sh
cp -r backend/ $APP_PATH/backend

echo "adding appman CLI files"
cp -r ./client/ $APP_PATH/client

echo "building appman_api service file"
echo "[Unit]" > service/appman_api.service
echo "Description=The API for appman" >> service/appman_api.service

echo "[Service]" >> service/appman_api.service
echo "ExecStart=$HOME/.local/appman/api/appman_api.sh" >> service/appman_api.service
echo "WorkingDirectory=$HOME/.local/appman/api" >> service/appman_api.service
echo "Restart=always" >> service/appman_api.service

echo "[Install]" >> service/appman_api.service
echo "WantedBy=default.target" >> service/appman_api.service
cp ./service/appman_api.service $HOME/.config/systemd/user/appman_api.service

echo "adding appman_api service"
mkdir -p $HOME/.config/systemd/
mkdir -p $HOME/.config/systemd/user/

echo "starting appman_api as a user service"
systemctl --user daemon-reload
systemctl --user enable appman_api.service
systemctl --user start appman_api.service

echo 'Run "systemctl --user status appman_api.service" and "systemctl --user is-enabled appman_api.service" to make sure the appman_api service is running'
echo 'in case of issues run "journalctl --user -xe appman_api.service"'
echo "If appman_api.service is runnig but you can't launch appman and connect to the api, waiting a few more seconds should resolve it"

echo "Installation complete"

