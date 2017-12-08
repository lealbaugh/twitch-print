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
import twitch_config
import socket
import re
import time
import select

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

# ------ From the Twitchbot Instructable: ------ 
# a regex for parsing the returned message; compile it here and use it in the message receiving bit
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


# Some Twitch channel mod functionality
def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	# IRC protocol does not love newlines inside messages
	msg = msg.replace("\n"," ")
	print("Sending message: "+msg)
	# IRC protocol *does* love a \r\n at the end of a message, and utf-8 encoding
	msg = "PRIVMSG "+twitch_config.CHAN+" :"+msg + "\r\n"
	sock.send(msg.encode('utf-8'))

# The Instructable also implements "ban" and "timeout" functionality, but we will be blissfully not using those

# ------ end of functions from Instructable ------ 


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

# A regex to determine whether something is a Library of Congress call number (or one of the Hunt Library location tags)
# I developed/tested this with the validdator_tester.py code.
dewey_validator=re.compile(r"([a-zA-Z]{1,3}\s*[\d\.]{1,7}\s*\.[a-zA-Z]\d{1,5}\s*[\w]{2,4}\s*\d{0,4}|(STACKS|OVRSZQ)[\-2-4]{0,2})")

# This function processes the messages and sends any regex matches it finds to the printer and back to the chat channel
def maybePrintMessages(message, sender, socket):
	matches = dewey_validator.findall(message)
	if (len(matches)>0):
		text = sender+": \n"
		for match in matches:
			text = text + match[0] + " \n\n"
		printFormatted(text)
		chat(socket, "Received from "+text)

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


# This sets up the button pin as an input.  Since I wired the button between pin and ground, we want a pullup resistor.
# This will hold the signal up unless the button is pressed, at which point the signal will go low.
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# When a falling edge is detected on pin 37, regardless of whatever else is happening in the program, 
# the callback function will be run (in this case, "shutdown")
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=shutdown, bouncetime=300)
# ------ end of hardware functions ------ 

# This function handles the raw responses gathered in the read_loop. If it sees a 'ping', it'll 'pong'.
# If it sees the "welcome", it will print a "connected" message to the printer.  Otherwise, it will 
# send chat messages to be processed by the printer functions above.
def process_response(response, socket):
	# print("RAW:" + response)
	if ("ping" in response.lower()):
		print ("(ping)")
		s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		print("(pong)")
	else:
		username = re.search(r"\w+", response).group(0) # return the entire match
		message = CHAT_MSG.sub("", response)
		if (username == "tmi"):
			print(username + ": " + message)
			if ("Welcome" in message):
				printFormatted("Connected to Twitch.")
		if (username != "tmi" and username != "PING"):
			print(username + ": " + message)
			maybePrintMessages(message, username, socket)

# This function is based on the hardmath123 tutorial.
# It polls the socket and reads out messages when they are ready.
def read_loop(callback, socket):
	data = ""
	CRLF = '\r\n'
	while True:
		messages = []
		time.sleep(5) # prevent CPU hogging
		readables, writables, exceptionals = select.select([s], [s], [s]) 
		if len(readables) == 1:
			data += s.recv(512);
			while CRLF in data:
				message = data[:data.index(CRLF)]
				data = data[data.index(CRLF)+2:]
				callback(message, socket)

# ============ And then make it go =============

# When we first turn on the Pi, send a message to the printer so I know the system is on and the code is running.
print "Starting up."

# Then, wait a little bit. We go at a leisurely pace to allow time to make a wifi connection.
time.sleep(4); 
printFormatted("Computer is awake.")

# And honestly, another 6 seconds can't hurt.  Then attempt a connection to Twitch.
time.sleep(6);
printFormatted("Attempting connection to:\n"+ twitch_config.CHAN)

# initiate the socket connection
s = socket.socket()
s.connect((twitch_config.HOST, twitch_config.PORT))
s.send("PASS {}\r\n".format(twitch_config.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(twitch_config.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(twitch_config.CHAN).encode("utf-8"))

# Okay, hopefully all that went okay.  The message-processing loop will let us know when we get a "welcome"
# message back from Twitch.


# So then start the main process! Just keep running the read loop.
try:
	while True:
		read_loop(process_response, s)
# it is apparently considered good practice to "clean up" the GPIO pins at the end of the program
# I'm not 100% sure what this means -- maybe something about re-setting the pullup/down resistors?
finally:
		GPIO.cleanup()