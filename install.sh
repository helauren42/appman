path="$HOME/.local/appman"

echo "The appman application will be installed in $HOME/.local/appman is this okay? y/n"
read answer

answered=1
while [[ $answered == 1 ]]; do
    if [[ $answer == "y" || $answer == "Y" || $answer == "yes" || $answer == "Yes" ]]; then
        answered=0
    elif [[ $answer == "n" || $answer == "N" || $answer == "no" || $answer == "No" ]]; then
        answered=0
        validPath=1
        while [[ $validPath != 0 ]]; do
            echo "Type your custom install path: "
            read -r path
            if [[ -d $path ]]; then
                validPath=0
            else
                echo "Invalid path, please try again."
            fi
        done
    else
        echo "wrong answer try again"
        read answer
    fi
done

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

echo "Done"
