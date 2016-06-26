#!/usr/bin/env python
import os
import requests
import argparse
import sys
import ctypes
import platform
import time
import urllib, json


API_KEY = "17715267112b9ce0665cae4b7fd40be0" 
API_SECRET = "9fce0663a667009a2a858023ce74ce9c"

if sys.version_info <= (2, 6):
    import commands as subprocess
else:
    import subprocess


# Get current Desktop Environment
# http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
def detect_desktop_environment():
    environment = {}
    if os.environ.get("KDE_FULL_SESSION") == "true":
        environment["name"] = "kde"
        environment["command"] = """
                    qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
                        var allDesktops = desktops();
                        print (allDesktops);
                        for (i=0;i<allDesktops.length;i++) {{
                            d = allDesktops[i];
                            d.wallpaperPlugin = "org.kde.image";
                            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                            d.writeConfig("Image", "file:///{save_location}")
                        }}
                    '
                """
    elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        environment["name"] = "gnome"
        environment["command"] = "gsettings set org.gnome.desktop.background picture-uri file://{save_location}"
    elif os.environ.get("DESKTOP_SESSION") == "mate":
        environment["name"] = "mate"
        environment["command"] = "gsettings set org.mate.background picture-filename {save_location}"
    else:
        try:
            info = subprocess.getoutput("xprop -root _DT_SAVE_MODE")
            if ' = "xfce4"' in info:
                environment["name"] = "xfce"
        except (OSError, RuntimeError):
            environment = None
            pass
    return environment


if __name__ == '__main__':
	 # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="REQUIRED. Last.fm username to use", required=True)
    parser.add_argument("-p", "--period", type=str, default="overall", help="Time period to get artist data from. Example: overall | 7day | 1month | 3month | 6month | 12month")

    args = parser.parse_args()

    user = args.user 
    limit = '1'
    period = args.period

    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+user+"&api_key="+API_KEY+"&period="+period+"&limit="+limit+"&format=json"
    response = urllib.urlopen(url)
    image_url = json.loads(response.read())
    image_url =  image_url['topartists']['artist'][0]['image'][4]['#text'] 

    supported_linux_desktop_envs = ["gnome", "mate", "kde"]

    # Request image
    response = requests.get(image_url)

    # If image is available, proceed to save
    if response.status_code == requests.codes.ok:
        # Get home directory and location where image will be saved (default location for Ubuntu is used)
        home_dir = os.path.expanduser("~")
        save_location = "{home_dir}/Pictures/Wallpapers/{time}.png".format(home_dir=home_dir, time=time.strftime("%d-%m-%Y-%H-%M-%S"))

        # Create folders if they don't exist
        dir = os.path.dirname(save_location)
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Write to disk
        with open(save_location, "wb") as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

        # Check OS and environments
        platform_name = platform.system()
        if platform_name.startswith("Lin"):

            # Check desktop environments for linux
            desktop_environment = detect_desktop_environment()
            if desktop_environment and desktop_environment["name"] in supported_linux_desktop_envs:
                os.system(desktop_environment["command"].format(save_location=save_location))
            else:
                print("Unsupported desktop environment")

        # Windows
        if platform_name.startswith("Win"):
            # Python 3.x
            if sys.version_info >= (3, 0):
                ctypes.windll.user32.SystemParametersInfoW(20, 0, save_location, 3)
            # Python 2.x
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, save_location, 3)

        # OS X/macOS
        if platform_name.startswith("Darwin"):
            command = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX " \
                      "file \"{save_location}\"'".format(save_location=save_location)
            os.system(command)

