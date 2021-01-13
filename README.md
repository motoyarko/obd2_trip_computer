**TODO:**
- To check - add try catch to read/write functions
- To check - create new file if error during reading file
- To check - average values are 0 if engine isn't started
- DONE - update screen settings from raspberry code
- add multiple screens with sensors data
- switching between screens by pressing on button on IO port
- reset log file data by press and hold on button on IO port
- recreate log file if error reading from it. save old file with .old extention
- To check - rpm can be != 0 after shutting down the engine ???
added check with set values to 0.0 if response is None
- DONE- Add settings from config.txt in raspberry
- check if the query request is supported by ECU
- long delay before quit if connection with ECU not established ?


**App requirements:**
- Python 3.7
- pygame v2.0.1 https://www.pygame.org/news
- obd v0.7.1 https://github.com/brendan-w/python-OBD
- gpiozero 1.5.1 https://github.com/gpiozero/gpiozero

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

#!bin/sh
cd /
cd home/pi/obd_pygame
sudo python3 main.py

make it executable

chmod ... blablabla **TBU**


fonts https://fonts.google.com/specimen/Audiowide?preview.text=Almost%20before%20we%20knew%20it,%20we%20had%20left%20the%20ground.%20km%2Fh%20&preview.text_type=custom&selection.family=Montserrat#standard-styles




