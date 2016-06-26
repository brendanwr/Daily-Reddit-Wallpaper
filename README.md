# Last.fm Top Artist Wallpaper (on startup)
This script changes your wallpaper to the top artist from your last.fm library 


*Supported: Linux (gnome, kde, mate, lxde), Windows and OS X*

Dependencies
=======
Make sure you have Python installed and PATH variable set.

Ubuntu
------
If you don't have ```pip ``` for Python:
```
sudo apt-get install python-pip
```

You will need the module ```requests```  installed, which are in requirements.txt:

```
pip install -r requirements.txt
```

Windows
------
Follow [this guide](https://pip.pypa.io/en/stable/installing/) to install  ```pip```  and configure PATH variable.
The rest is the same.

Using script
=======

Simply run (a username is required):
```
python /home/silvio/Scripts/change_wallpaper_lastfm.py --user USERNAME
```

If you wanna use other time periods, include one of the following arguments: overall | 7day | 1month | 3month | 6month | 12month. Defaults to overall
```
python /home/silvio/Scripts/change_wallpaper_lastfm.py --period 6month
```
python /home/silvio/Scripts/change_wallpaper_lastfm.py --time week 
```

On OS X, you can specify display number with option ```--display```. Use 0 for all display (default), 1 for main display and so on.


Running on startup
=======
Ubuntu
------
To make managment of the script simple, we can accomplish this using built-in Startup Applications.

![Startup Applications](http://i.imgur.com/NDFmFd9.png)


Click on Add.

![Add new startup command](http://i.imgur.com/uFqQ8ky.png)

Note: you can use ```--period``` arguments here aswell.


Windows
------
We will be using Task Scheduler for this. You can find it in Windows search.
Once you open it, click on ```Create Basic Task```
Follow the procedure.

![Procedure](http://i.imgur.com/1uZMpyc.png)

![Procedure](http://i.imgur.com/3ApvF6W.png)

![Procedure](http://i.imgur.com/fPdwcyg.png)

![Procedure](http://i.imgur.com/zOCCfQI.png)

In ```Add arguments``` field type the location of the script. Example

```
"D:\change_wallpaper_lastfm.py" 
```

or 

```
"D:\change_wallpaper_lastfm.py" --period 7day 
```

Running every minute or hour
=======

Look into using cronjobs on Linux or Task Scheduler on Windows for performing this.
