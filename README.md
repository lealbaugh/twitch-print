# Twitch chat -> thermal printer on Raspi
This is the code that runs on the Raspberry Pi which the streamer carries.  It runs a Twitch bot which reads channel messages and looks for Library of Congress call numbers and Hunt Library locations.  When it sees a valid bit of information, it prints that information and the username of the contributor on the printer and responds to the stream to let the contributor know their message has been passed along. To act as a standalone device, it also implements 1) auto-running the code at system startup, and 2) a small hardware button that quits the program and shuts off the Raspberry Pi so it can be safely powered down without needing a keyboard/monitor or ssh connection.

The main code is in `twitch_bot.py`.  Make sure that `twitch_config.py` has appropriate authentication credentials (username and a corresponding OAuth token, as obtained on https://twitchapps.com/tmi/), then run the code with `python twitch_bot.py`

## Main credits
This uses the thermal printer library from https://github.com/luopio/py-thermal-printer
and ideas from various tutorials:

http://www.instructables.com/id/Twitchtv-Moderator-Bot/

https://hardmath123.github.io/socket-science-2.html

http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

It also incorporates some configuration lessons I learned while building a previous thermal printer project, documented at http://lea.zone/blog/making-of-fortunes/


## Software configuration
This assumes the Pi is running Raspbian Stretch, November 2017 version, as downloaded from https://www.raspberrypi.org/downloads/raspbian/ and installed as an image onto an SD using Etcher, per the instructions at https://www.raspberrypi.org/documentation/installation/installing-images/README.md

### Serial
We use the serial port to communicate with the printer, so we want it to be on and we don't want it cluttered with messages from the shell. To accomplish this: `sudo raspi-config` -> Interfacing options -> Serial -> No, I don't want the login shell to be accessible over serial, and Yes, I would like the serial port hardware to be enabled.  

For the Pi3, we need to re-allocate the UARTs so that we have the reliable hardware UART for our printer communication instead of giving it to the Bluetooth hardware (which we don't use for this project). To do this, add `dtoverlay=pi3-miniuart-bt` to `/boot/config.txt`.

### SSH
Since late 2016, Pis don't automatically support sshing in (presumably for security reasons, because it is very easy to know the default password on a Pi).  Here's a solution, sort of, and an explanation:
https://raspberrypi.stackexchange.com/questions/4444/enabling-ssh-on-rpi-without-screen-keystrokes-for-raspi-config
In summary:  There are two options to enable ssh: add a blank "ssh" document to the boot partition of the SD card (requires either another linux computer or special drivers for Mac to access that partition), or change the ssh settings in `sudo raspi-config` (requires keyboard and monitor to be able to see what you're doing).

### Wifi
To automatically connect to CMU's network without needing keyboard and monitor on campus to set up:
	- Register the device's MAC address with CMU's netreg: https://courses.ideate.cmu.edu/16-223/f2014/registering-your-udoo-with-cmu/
	- Add the "CMU" network to `/etc/wpa_supplicant/wpa_supplicant.conf` (per https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) Note that it doesn't have a password, so the proper configuration is:
```
network={
    ssid="CMU"
    key_mgmt=NONE
}
```

### Auto-run
For the python script to run at startup, add `python -u /home/pi/twitch-print/twitch_bot.py 2>> /var/log/twitch_bot.err >> /var/log/twitch_bot.out &` to the middle of `/etc/rc.local` per https://www.raspberrypi.org/documentation/linux/usage/rc-local.md (assuming this repo has indeed been cloned right into `/home/pi`)

## Hardware configuration
Wire connections:
Pin 9 (gnd) to one side of button
Pin 15 (gpio) to other side of button
Pin 6 (gnd) to black wire of printer
Pin 8 (txd) to yellow wire of printer
Printer power black and red to 5-9V 2A power source


Note: If we wanted data *from* the printer to the Pi, we would need a level shifter.  However, the Pi's 3v3 signal is sufficient to pass messages *to* the printer.  My understanding is that the only message the printer is capable of sending back to the Pi is an "out of paper" warning, which we really didn't care about for this project.



