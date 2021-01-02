todo:
To check - add try catch to read/write functions
To check - create new file if error during reading file
To check - average values are 0 if engine isn't started
- update screen settings from raspberry code

App requirements:
* Python 3.7
* pygame v2.0.1 https://www.pygame.org/news
* obd v0.7.1 https://github.com/brendan-w/python-OBD

This app is checked on Toyota Corolla E120 2005 year.

Raspberry Pi 3 Model B+ used as hardware platform with 

Raspberry Pi OS Release date: December 2nd 2020 used as OS.


<h3> Installation process:</h3>

install obd library in python 3:

$ sudo pip3 install obd

Add the following strings in the end of rc.local file but before "exit 0" to auto start the app

$ sudo nano /etc/rc.local

 - printf "start run_obd_pygame.sh"

 - sh /home/pi/./run_obd_pygame.sh

create run_obd_pygame.sh file

-

make it executable

-





