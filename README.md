# Introduction

I'm building this linux app manager application because I always have ideas for customizations and creating applications to improve my linux experience and there is always this one obstacle, of I need it to start this application when I login. And instead of just enabling into systemclt every individual apps I may create so that it launches at startup. Having an app manager handle this to seamlessly activate/deactivate/install/uninstall apps and tweak app settings, in a centralized manner to have more control, will be very convenient.
Also I run Gnome and I am not a fan of the current official extension model, forcing every application to be built in JS is very self limiting, plus JS is not known for being reliable and stable. With appman we shall finally be free to manager all the custom extensions we want that do not conform to Gnome's extension standards.

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
