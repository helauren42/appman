# AppMan - Linux Application Session Manager

STILL IN DEVELOPMENT

## Introduction

This is a linux applications session manager.

I initially had the idea for this program after I was frustrated by Gnome's extension application. For the back story I had installed a background slideshow application which caused various bugs, I noticed that it was written in JS and that a lot of other Gnome extensions were too, which I found curious but didn't think too much of it. So I managed to replicate the application without the bugs, by writing it in python, unfortunately when I thought it was time to release my background slideshow gnome application to the world I stumbled upon Gnome's regulation, which requires not only to develop official Gnome extensions in JS but by using GJS too and only created subprocesses when absolutely necessary. Under these conditions, I had no guarantee that I could reproduce my background slideshow application without developing the bugs from the one coming from the official release and plus I found the constraints very annoying. So I built my own Session manager to manage my custom Gnome extensions, hopefully others might use it too.

In the process of building I decided that it shouldn't be only to manage custom Gnome extensions that do not conform official Gnome requirements, because why not make it a session manager to control all types of linux applications.

## Features

CLI and API Support: Control applications via a command-line interface shell or a REST API.<br>
Application Management: Start, stop, and manage Linux applications with ease.<br>
Custom Gnome Extensions: Run custom Gnome extensions without adhering to Gnome's strict requirements.<br>
Third-Party Integration: Easily integrate third-party applications into AppMan.<br>
Settings Management: Optional support for custom settings managers for each application.<br>

## Installation

Clone the repository or download the source code.<br>
<br>
Run the install.sh script in your terminal:<br>
Follow the prompts to complete the installation.<br>
<br>
The installation script will:<br>
Create the necessary directories in ~/.local/appman.<br>
Install the AppMan binary in ~/.local/bin/appman.<br>
Set up the AppMan API as a user service using systemd.<br>

## Uninstallation

To uninstall AppMan, run the uninstall.sh script, during the installation it is copied over to your appman directory:<br>
~/.local/appman/uninstall.sh<br>

## CLI SHELL USAGE

To start the appman shell type "appman" in your terminal. A prompt "appman$>" will present itself to you.<br>
In case appman command does not work make sure you have "$HOME/.local/bin" in your environment with "echo $PATH".

### Running an executable

If no management options are specified, appman assumes you want to run an executable.<br><br>

appman$> program.sh [arguments...]<br><br>

program.sh represents the name of the program inside appman/run/<br>

### Application Management Commands

These commands allow you to manage registered applications.<br>
<br>
1. List Registered Applications<br>
Lists all registered applications along with their status (active/inactive).<br>
<br>
appman$> list<br>
<br>
Example output:<br>
--------------------------------------------------------------------------------<br>
APP: MyApp<br>
Run: myapp.sh<br>
Program Name: MyApp<br>
Status: active<br>
Description: A sample application<br>
--------------------------------------------------------------------------------<br>
<br>
2. Refresh Application List<br>
Reloads the list of registered applications.<br>

appman$> refresh<br>

3. Activating and Deactivating applications

Starts or stops application. If application set to active, appman will launch it at login.<br>

Activating:<br>
appman$> activate <program1> <program2> ...<br>
<br>
Deactivating:<br>
appman$> deactivate <program1> <program2> ...<br>
<br>

4. Clearing terminal

You can call the clear command through appman.

### add your program's binary or entry point script inside of /appman/bin

Create a bash script that serves as an entry point to your program. With a bash script you can define your arguments, flags and compiler as needed for every language.<br>

### Create a metadata.json

The metadata json is crucial for your application to launch and display correctly on the appman GUI.<br>

Components:<br>
<br>
run = the script's filename inside appman/bin/ to launch the application and apply settings changes<br>
name = name of the application displayed on the gui<br>
program_name = The name of the process running in the shell. If multiple processes exist, provide the one that always runs while the application is active.<br>
description = short description about the application<br>
settings(optional) = create a .sh settings launcher, input the relative path from your projects directory in app to your settings ".sh" launcher<br>

### Run

The script needs to be able to take arguments --activate and --deactivate, as whenever an application is activated or deactivated on appman, then appman will run this script and pass --activate or --deactivate as argument, the activation and deactivation of the processes can be handled as you wish.<br>

### Settings program [Optional]
To give you the freedom to build your own settings manager program for your application it should be built as a standalone, that can be run by clicking on the settings button on the appman application. I don't want to enforce my own "appman settings page builder module" that would discourage some developers I believe while restricting freedom too.<br>
Here again you create a .sh as launcher for your settings manager application.<br>
<!-- If you want to make it match the design of appman look at the "Design Guide" section in this README --><br>

## Recommended
Put all your application's necessary dependencies inside of /appman/apps.
Copy your an uninstall.sh inside of /appman/apps/your_application_name, make it terminate active processes if any

