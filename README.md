# Twitch chat -> thermal printer on Raspi###

This uses https://github.com/luopio/py-thermal-printer
and ideas from various tutorials:
http://www.instructables.com/id/Twitchtv-Moderator-Bot/
https://hardmath123.github.io/socket-science-2.html
http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3


## Software configuration

### Serial support
`sudo raspi-config` -> Interfacing options -> Serial -> No, I don't want the login shell to be accessible over serial, and Yes, I would like the serial port hardware to be enabled.  We use the serial port to communicate with the printer, so we want it to be on, and we don't want it cluttered with messages from the shell.

For the Pi3, we need to re-allocate the UARTs so that we have the reliable hardware UART for our printer communication instead of giving it to the Bluetooth hardware (which we don't use for this project). More details from the previous printer project, at http://lea.zone/blog/making-of-fortunes/

### SSH
Since late 2016, raspis don't automatically support sshing in (presumably for security reasons, because it is very easy to know the default password on a raspi).  Here's a solution, sort of, and an explanation:
https://raspberrypi.stackexchange.com/questions/4444/enabling-ssh-on-rpi-without-screen-keystrokes-for-raspi-config
In summary:  There are two options to enable ssh: add a blank "ssh" document to the boot partition of the SD card (requires either another linux computer or special drivers for Mac to access that partition), or change the ssh settings in `sudo raspi-config` (requires keyboard and monitor to be able to see what you're doing).

### Wifi
To automatically connect to CMU's network without needing keyboard and monitor on campus to set up:
-Register the device's MAC address with CMU's netreg: https://courses.ideate.cmu.edu/16-223/f2014/registering-your-udoo-with-cmu/
-Add the "CMU" network to `/etc/wpa_supplicant/wpa_supplicant.conf` (per https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) Note that it doesn't have a password, so the proper configuration is:
```
network={
    ssid="CMU"
    key_mgmt=NONE
}
```

### Auto-run
For the python script to run at startup,
https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
(Add `python -u /home/pi/twitch-print/twitch_bot.py 2>> /var/log/twitch_bot.err >> /var/log/twitch_bot.out &` to the middle of `/etc/rc.local`)

## Hardware configuration
Wire connections:
Pin 9 (gnd) to one side of button
Pin 15 (gpio) to other side of button
Pin 6 (gnd) to black wire of printer
Pin 8 (txd) to yellow wire of printer
Printer power black and red to 5-9V 2A power source


Note: If we wanted data *from* the printer to the RasPi, we would need a level shifter.  However, the Pi's 3v3 signal is sufficient to pass messages *to* the printer.  The only message the printer is capable of sending back to the Pi is an "out of paper" warning, which we really didn't care about for this project.


