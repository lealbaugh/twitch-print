Twitch chat -> thermal printer on Raspi

This uses https://github.com/luopio/py-thermal-printer
and ideas from various tutorials:
http://www.instructables.com/id/Twitchtv-Moderator-Bot/
https://hardmath123.github.io/socket-science-2.html
http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3



Configuration that needs to happen:
`sudo raspi-config` -> Interfacing options -> Serial -> No, I don't want the login shell to be accessible over serial, and Yes, I would like the serial port hardware to be enabled

For the Pi3, remember to swap the UARTs around per http://lea.zone/blog/making-of-fortunes/

If we wanted data *from* the printer to the RasPi, we would need a level shifter.  However, the Pi's 3v3 signal is sufficient to inform the printer.

For the script to run at startup,
https://www.raspberrypi.org/documentation/linux/usage/rc-local.md


Pin setup:
Pin 9 (gnd) to one side of button
Pin 15 (gpio) to other side of button
Pin 6 (gnd) to black wire of printer
Pin 8 (txd) to yellow wire of printer

(Printer power black and red to 5-9V 2A power source.)

