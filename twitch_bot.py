# bot.py
# modified from cormac-obrien's Instructable at 
# http://www.instructables.com/id/Twitchtv-Moderator-Bot/
# and Hardmath123's IRC socket-reading tutorial at
# https://hardmath123.github.io/socket-science-2.html

# Also integrates button interrupts by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

# relies on a config file (for authentication to Twitch) that you can ask Lea for

# Necessary pieces:
#   gather messages from Twitch
#   strip out Dewey decimal numbers
#   send messages to printer

# imports for reading twitch channel
import twitch_config
import socket
import re
import time
import select

# imports for printing
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

import printer
p = printer.ThermalPrinter()
from textwrap import wrap

# import for powering off, as in https://www.raspberrypi.org/forums/viewtopic.php?t=133665
from subprocess import call

reallyShutDown = True
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
	sock.send("PRIVMSG #{} :{}".format(twitch_config.CHAN, msg))

def ban(sock, user):
	"""
	Ban a user from the current channel.
	Keyword arguments:
	sock -- the socket over which to send the ban command
	user -- the user to be banned
	"""
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
	"""
	Time out a user for a set period of time.
	Keyword arguments:
	sock -- the socket over which to send the timeout command
	user -- the user to be timed out
	secs -- the length of the timeout in seconds (default 600)
	"""
	chat(sock, ".timeout {}".format(user, secs))

# ------ end of functions from Instructable ------ 


# ------ hardware-related functions ------ 
def printFormatted(text, characters=30):
	p.wake()
	# p.linefeed(2)
	p.bold()
	lines = ['\n'.join(wrap(block, width=characters)) for block in text.splitlines()]
	for line in lines:
		p.print_text(line+"\n")
	p.linefeed(4)
	p.sleep()

dewey_validator=re.compile(r"([a-zA-Z]{1,3}\s*[\d\.]{1,7}\s*\.[a-zA-Z]\d{1,5}\s*[\w]{2,4}\s*\d{0,4}|(STACKS|OVRSZQ)[\-2-4]{0,2})")
def maybePrintMessages(message):
	matches = dewey_validator.findall(message)
	if (len(matches)>0):
		text = ""
		for match in matches:
			text = text + match[0] + " "
		printFormatted(text)

# uses a hacky deglitch as suggested by https://www.raspberrypi.org/forums/viewtopic.php?t=134394
def shutdown(whatever):
	print "falling edge on pin "+button_pin
	sleep(0.5) # debounce for 0.5s
	if GPIO.input(button_pin) == 0:
		printFormatted("~*goodnight*~")
		if (reallyShutDown):
			print "shutting down"
			call("sudo shutdown -h now", shell=True)
		else:
			print "I would be shutting down now"


# Paying attention to buttons (from fortune machine code -- we're using this for shutdown)
# On the edge
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# when a falling edge is detected on pin 37, regardless of whatever
# else is happening in the program, the callback function will be run
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=shutdown, bouncetime=300)
# ------ end of hardware functions ------ 

def process_response(response):
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
			maybePrintMessages(message)

# Current main process loop; polls the socket and reads out messages when they are ready
# Based on the hardmath123 tutorial.
def read_loop(callback):
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
				callback(message)

# ============ And then make it go =============

# read_loop(process_response)

print "Starting up."
time.sleep(4); # go at a leisurely pace to allow wifi connection
printFormatted("Computer is awake.")
time.sleep(6); # pause a bit more
printFormatted("Attempting connection to:\n"+ twitch_config.CHAN)

# initiate the socket connection
s = socket.socket()
s.connect((twitch_config.HOST, twitch_config.PORT))
s.send("PASS {}\r\n".format(twitch_config.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(twitch_config.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(twitch_config.CHAN).encode("utf-8"))


try:
	while True:
		read_loop(process_response)
finally:
		GPIO.cleanup()