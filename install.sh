path="$HOME/.local/appman"

echo "The appman application will be installed in $HOME/.local/appman"

echo "Do you want a cli application? y/n"
answered=1
while [[ $answered == 1 ]]; do
    if [[ $answer == "y" || $answer == "Y" || $answer == "yes" || $answer == "Yes" ]]; then
        answered=0
        createCli=0
elif [[ $answer == "n" || $answer == "N" || $answer == "no" || $answer == "No" ]]; then
        answered=0
        createCli=1
done

if [[ $createCli == 0 ]]; then
    # install cli
fi

echo "Do you want a desktop application? y/n"

answered=1
while [[ $answered == 1 ]]; do
    if [[ $answer == "y" || $answer == "Y" || $answer == "yes" || $answer == "Yes" ]]; then
        answered=0
        createDesktopApp=0
    elif [[ $answer == "n" || $answer == "N" || $answer == "no" || $answer == "No" ]]; then
        answered=0
        createDesktopApp=1
done

if [[ $createDesktopApp == 0 ]]; then
    mv appman.desktop ./
fi

echo "adding ~/.config/systemd/user/appman_api.service"
mkdir -p $HOME/.config/systemd/
mkdir -p $HOME/.config/systemd/user/
mv ./servicectl/appman_api.service $HOME/.config/systemd/user/appman_api.service

echo "starting appman_api as a user service"
systemctl --user daemon-reload
systemctl --user start myapp.service

echo "make sure appman_api is active"
sleep 3

systemctl --user status myapp.service

echo "Done"
