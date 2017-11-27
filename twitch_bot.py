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
# p = printer.ThermalPrinter()
from textwrap import wrap

# import for powering off, as in https://www.raspberrypi.org/forums/viewtopic.php?t=133665
from subprocess import call


messages = []

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
		lines = ['\n'.join(wrap(block, width=characters)) for block in text.splitlines()]
		for line in lines:
				p.print_text(line+"\n")

on = false
def shutdown():
	if (on):
		call("sudo shutdown -h now", shell=True)
		on = false
	else:
		print "I would be shutting down now"


# Paying attention to buttons (from fortune machine code -- we're using this for shutdown)
# On the edge
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the callback function will be run
GPIO.add_event_detect(15, GPIO.FALLING, callback=shutdown, bouncetime=300)
# ------ end of hardware functions ------ 

def process_response(response):
	if response == "PING :tmi.twitch.tv\r\n":
		s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		print("(pong)")
	else:
		username = re.search(r"\w+", response).group(0) # return the entire match
		message = CHAT_MSG.sub("", response)
		if (username != "tmi" and username != "PING"):
			messages.append(message)
		# actually should store message in a dict by username (so only one vote person)
		# but that will be harder to debug right now
		print(username + ": " + message)
		# printFormatted(message)
			


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

# time.sleep(20); # when we have the code running on startup, this will allow wifi connection

# initiate the socket connection
s = socket.socket()
s.connect((twitch_config.HOST, twitch_config.PORT))
s.send("PASS {}\r\n".format(twitch_config.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(twitch_config.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(twitch_config.CHAN).encode("utf-8"))

# p.linefeed(5)
# p.font_b()
# p.print_text("Alive and connecting to channel: "+ twitch_config.CHAN)
# p.linefeed(5)

try:
	while True:
		read_loop(process_response)
finally:
		GPIO.cleanup()
