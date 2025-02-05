STILL IN DEVELOPMENT

# Introduction

This is a linux applications session manager.

I initially had the idea for this program after I was frustrated by Gnome's extension application. For the back story I had installed a background slideshow application which caused various bugs, I noticed that it was written in JS and that a lot of other Gnome extensions were too, which I found curious but didn't think too much of it. So I managed to replicate the application without the bugs, by writing it in python, unfortunately when I thought it was time to release my background slideshow gnome application to the world I stumbled upon Gnome's regulation, which requires not only to develop official Gnome extensions in JS but by using GJS too and only created subprocesses when absolutely necessary. Under these conditions, I had no guarantee that I could reproduce my background slideshow application without developing the bugs from the one coming from the official release and plus I found the constraints very annoying. So I built my own Session manager to manage my custom Gnome extensions, hopefully others might use it too.

In the process of building I decided that it shouldn't be only to manage custom Gnome extensions that do not conform official Gnome requirements, because why not make it a session manager to control all types of linux applications.

# Installation

run install.sh in your terminal and answer the prompts.
You will find uninstall.sh inside /appman/ in case you want to remove the program and all of its components.

# CLI USAGE

- appman list
Lists all the applications you have installed and their current status

- appman --activate application_name
activate application
- appman --deactivate application_name
deactivate application

# Adding third party applications to appman

### add your program's binary or entry point script inside of /appman/bin
Create a bash script that serves as an entry point to your program. With a bash script you can define your arguments, flags and compiler as needed for every language.

### Create a metadata.json
The metadata json is crucial for your application to launch and display correctly on the appman GUI.

Components:

run = the script's filename inside appman/bin/ to launch the application and apply settings changes
name = name of the application displayed on the gui
program_name = name of the process running in shell, the main one should be enough
description = short description about the application
settings(optional) = create a .sh settings launcher, input the relative path from your projects directory in app to your settings ".sh" launcher

### Run

The script needs to be able to take arguments --activate and --deactivate, as whenever an application is activated or deactivated on appman, then appman will run this script and pass --activate or --deactivate as argument, the activation and deactivation of the processes can be handled as you wish.

### Settings program [Optional]
To give you the freedom to build your own settings manager program for your application it should be built as a standalone, that can be run by clicking on the settings button on the appman application. I don't want to enforce my own "appman settings page builder module" that would discourage some developers I believe while restricting freedom too.
Here again you create a .sh as launcher for your settings manager application.
<!-- If you want to make it match the design of appman look at the "Design Guide" section in this README -->

## Recommended
Put all your application's necessary dependencies inside of /appman/apps.
Add an uninstall.sh inside of /appman/apps
