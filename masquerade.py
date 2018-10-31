# bot.py
# Primarily cobbled together from cormac-obrien's Instructable at 
# http://www.instructables.com/id/Twitchtv-Moderator-Bot/
# and Hardmath123's IRC socket-reading tutorial at
# https://hardmath123.github.io/socket-science-2.html

# Also integrates button interrupts as explained by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

# There's lots of system setup to do to get this to work! Check out the README.
# At a minimum, make sure you have a valid username/auth token in the config file.

# Major pieces:
#   gather messages from Twitch
#   look for library call numbers and locations
#   send messages to printer
#	respond to the chat channel to let them know you've sent a message
#	shut down the system if the power off button is pressed

# imports for reading twitch channel
# import twitch_config
# import socket
import random
import time
import positives
# import select

# imports for printing -- note that the GPIO import will fail in a non-Pi context
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

import printer
p = printer.ThermalPrinter()
from textwrap import wrap

# import for interfacing with the Pi system for powering off, as in https://www.raspberrypi.org/forums/viewtopic.php?t=133665
from subprocess import call

# A little flag that I can flip if I want it to not actually shut the system down on button press
reallyShutDown = True

# The button is attached to pin 37 in the "Board" numbering scheme, as I set above
button_pin = 37

fortune_pin = 33


# ------ hardware-related functions ------ 
# This function adds linebreaks to format the text nicely for the printer, then sends the job to the printer
# It also puts the printer out of and back into its low-power mode because I was worried about excessive power consumption
# for a battery-powered device. This adds a wee bit of lag, but like, the game already has a massive amount of lag in the system.
def printFormatted(text, characters=30):
	p.wake()
	# p.linefeed(2)
	p.bold()
	lines = ['\n'.join(wrap(block, width=characters)) for block in text.splitlines()]
	for line in lines:
		p.print_text(line+"\n")
	p.linefeed(4)
	p.sleep()

# This function is called whenever the GPIO system detects a falling edge on the button pin (see line 120)
def shutdown(whatever):
	print "falling edge on pin "+str(button_pin)
	# hardware buttons often see little stray signals, but since this button is literally turning the whole computer off,
	# we'll check if the button is still pressed a hald second later.
	# this particular slightly hacky solution was suggested by https://www.raspberrypi.org/forums/viewtopic.php?t=134394
	time.sleep(0.5) # debounce for 0.5s
	if GPIO.input(button_pin) == 0:
		# sending a shutdown message to the printer is just good UX :)
		printFormatted("~*goodnight*~")
		if (reallyShutDown):
			print "shutting down"
			# send a message to the Pi to quit all its processes and shut down
			call("sudo shutdown -h now", shell=True)
		else:
			# this was for debugging
			print "I would be shutting down now"

# ------ grab & print a fortune ------ 
def printFortune(whatever):
	fortune = random.choice(fortunes)
	printFormatted(fortune)


# This sets up the button pin as an input.  Since I wired the button between pin and ground, we want a pullup resistor.
# This will hold the signal up unless the button is pressed, at which point the signal will go low.
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# When a falling edge is detected on pin 37, regardless of whatever else is happening in the program, 
# the callback function will be run (in this case, "shutdown")
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=shutdown, bouncetime=300)


# duplicate that for the request button
GPIO.setup(fortune_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(fortune_pin, GPIO.FALLING, callback=printFortune, bouncetime=300)




# ============ And then make it go =============

# When we first turn on the Pi, send a message to the printer so I know the system is on and the code is running.
print "Starting up."

# Then, wait a little bit. We go at a leisurely pace to allow time to make a wifi connection.
time.sleep(3); 
printFormatted("Computer is awake.")

# So then start the main process! Just keep running the read loop.
try:
	while True:
		# read_loop(process_response, s)
		time.sleep(0.5);
# it is apparently considered good practice to "clean up" the GPIO pins at the end of the program
# I'm not 100% sure what this means -- maybe something about re-setting the pullup/down resistors?
finally:
		GPIO.cleanup()