rm -rf $HOME/.local/appman/api
rm -rf $HOME/.local/appman/client
rm -rf $HOME/.local/appman/backend
rm -rf $HOME/.local/appman/venv
rm -rf $HOME/.local/appman/requirements.txt

systemctl --user stop appman_api
systemctl --user disable appman_api

./install.sh

