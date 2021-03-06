# bot.py
# Primarily cobbled together from cormac-obrien's Instructable at 
# http://www.instructables.com/id/Twitchtv-Moderator-Bot/
# and Hardmath123's IRC socket-reading tutorial at
# https://hardmath123.github.io/socket-science-2.html

# Also integrates button interrupts as explained by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

# There's lots of system setup to do to get this to work! Check out the README.
# At a minimum, make sure you have a valid username/auth token in the config file.


fortunes = ["Freeing yourself from limitation", "Expressing joy and youthful vigor", "Being open-minded", "Taking a leap of faith", "Attuning yourself to your instincts", "Being eager or curious", "Exploring your potential", "Embracing innovation and change","Taking appropriate action", "Receiving guidance from a higher power", "Becoming a channel of divine will", "Expressing masculine energy in appropriate and constructive ways", "Being yourself in every way","Listening to your feelings and intuitions", "Exploring unconventional spirituality", "Keeping secrets", "Being receptive", "Reflecting instead of acting", "Observing others", "Preserving purity","Nurturing yourself and others", "Bearing fruit", "Celebrating your body", "Bearing (literal or figurative) children", "Reveling in luxury", "Mothering those around you in positive ways", "Enjoying your sexuality", "Getting things done","Exercising authority", "Defining limits", "Directing the flow of work", "Communicating clear guidelines", "Being in control of yourself and others", "Tempering aggressive masculinity with wisdom and experience","Teaching or guiding others", "Searching for the truth", "Asking for guidance from a higher power", "Acknowledging the wisdom and experience of others", "Taking vows", "Engaging in heartfelt rituals", "Volunteering","Being in love", "Showing your love to others", "Expressing passion or romantic feelings", "Aligning yourself with groups or like-minded others", "Bringing people together", "Making well-informed decisions","Breaking through barriers", "Moving forward with confidence and authority", "Reaching the pinnacle of success", "Basking in the glory of achievement", "Guiding an effort to total victory", "Establishing yourself as a worthy leader","Imposing restrictions on yourself for your own benefit", "Bringing your passions under the control of reason", "Resisting impulses that work against your best interests", "Taking bold action","Becoming or seeking out a guru", "Going on a retreat", "Recharging spiritual or creative batteries", "Lighting the way for those with less experience", "Stepping back to gain perspective","Allowing events to unfold", "Seeing the larger pattern in everyday events", "Trusting your luck", "Watching for cycles", "Believing that \"what goes around, comes around\"","Making an objective decision", "Weighing an issue carefully before taking action", "Appropriately scaling your reaction to a situation", "Getting all the facts", "Considering evidence", "Deliberating","Seeing growth opportunities in unpleasant events", "Experiencing a dramatic change in personal perspective", "Making the best of an unforeseen change in your life or work", "Suspending disbelief", "Making sacrifices","Bringing an unpleasant phase of life to an end", "Recognizing and celebrating the conclusion of something", "Putting bad habits to rest", "Becoming a new person", "Leaving one person, place, or thing for another", "Letting go","Bringing opposites together", "Moderating your actions or emotions", "Finding middle ground", "Reaching compromises", "Synthesizing solutions that please everyone involved", "Using the old to make something new","Appreciating the luxuries that life has to offer", "Being comfortable in your own skin", "Enjoying your sexuality", "Splurging on an expensive personal item", "Embracing the fact that everyone has a darker side", "Dealing with unhealthy impulses in healthy ways","Breaking out of old, confining habits and mindsets", "Clearing the way for new growth", "Dispelling the influence of an inflated ego", "Getting back to basics", "Stripping away harmful illusions", "Receiving sudden insight","Hoping for the best", "Believing good things happen to good people", "Seeing events in the best possible light", "Adopting a generous spirit", "Seeking guidance from above", "Embracing possibility over probability","Enjoying healthy fantasies and daydreams", "Using your imagination", "Practicing magic or celebrating the magic of everyday life", "Attuning yourself to the cycles of nature", "Embracing the unknown","Seeing things clearly", "Experiencing intense joy", "Celebrating your own successes", "Knowing you're good at what you do", "Gaining recognition for your personal genius","Receiving a wake-up call", "Discovering a new purpose in life", "Becoming totally and completely yourself", "Receiving a well-deserved reward", "Passing an evaluation or examination", "Welcoming the start of a new phase of life","Having it all", "Knowing and loving yourself as completely as possible", "Seeing the interconnection of all things and people", "Enhancing your perspective", "Living life to its fullest", "Understanding the meaning of life","Being inspired", "Identifying an important goal", "Being given the opportunity to do whatever you want to do", "Giving or receiving direction", "Seeing a solution", "Creating something new", "Being aroused, sexually or creatively","Having a choice", "Offering or being offered an option", "Seeing the value of another person's approach", "Understanding there's more than one way to \"skin a cat\"","Successfully doing more than one thing at a time", "Being empowered to make a choice","Putting a plan into motion", "Taking that critical first step", "Making good things happen", "Going beyond your limits", "Blazing new trails", "Hitting the ground running", "Seeing your plans come to fruition","Sharing in a great celebration", "Sharing in a communal sense of achievement and success", "Preparing for a party", "Working together toward a common goal", "Giving or winning awards","Calmly expressing a dissenting opinion", "Allowing someone to use his or her own methods to get a job done", "Opening the floor for discussion or debate", "Comparing progress made so far to standards set earlier","Outperforming your peers", "Winning a competition", "Being recognized as a capable person", "Having your \"moment in the spotlight\"","Being cheered on by the crowd", "Getting an award", "Earning the admiration of others", "Telling someone, \"Good job!\"","Refusing to be silenced through fear or intimidation", "Continuing a fight against all odds", "Being fierce", "Defending yourself against physical and emotional attacks", "Refusing to put up with abuse", "Clinging to your values despite all pressure to abandon them","Taking swift action", "Moving forward with a plan as quickly as possible", "Energizing yourself", "Adapting to sudden changes", "Taking setbacks in stride", "Embracing the idea that nothing stays the same forever", "Reacting quickly and appropriately to unforeseen problems","Sticking with it for the duration", "Fulfilling your promises and obligations", "Bearing up under incredible duress", "Dragging yourself across the finish line", "Picking yourself up by your own bootstraps", "Refusing to quit", "Going as far as you can go and being satisfied with your performance","Holding your own in extreme circumstances", "Helping others carry their burdens", "Coming to the aid of the oppressed", "Knowing and being honest about your own limits", "Recognizing when you are not well-suited for a particular task","Leaping at a new opportunity", "Being a cheerleader or ardent advocate for your cause", "Being a True Believer", "Taking first steps toward independence", "Trusting in your own abilities", "Asking for feedback","Charging ahead", "Making rapid progress", "Refusing limits", "Dazzling those around you with your wit and charm", "Convincing others of your right to leadership", "Convincing others to follow you", "Being a catalyst for change","Paying close attention", "Helping others focus on the issue at hand", "Getting everyone to work together", "Identifying common ground", "Bringing people together, despite their differences", "Using reverse psychology","Putting old things together in new and exciting ways", "Coming up with unexpected solutions", "Using your experience to solve puzzles and problems", "Doing what you set out to do", "Directing the efforts of others","Trusting your feelings", "Opening yourself to spirit", "Accepting and returning affection", "Getting in touch with what motivates you", "Taking advantage of an opportunity to express love to others", "Listening to the still, small voice","Being drawn to someone", "Longing for someone or something", "Acting on your desires", "Discovering a feeling is mutual", "Doing what makes you feel good", "Merging", "Healing broken ties", "Admitting two people feel differently about each other and moving on","Celebrating your feelings or connections with others", "Expressing joy through song, dance, or physical affection", "Working together with others who share your feelings", "Performing acts of service as a way of saying, \"I love you\"","Embracing unconventional romantic arrangements","Maintaining your emotional stability", "Refusing to give in to overwhelming emotions", "Appreciating what you have and refusing to take it for granted", "Seeing the value of long-term commitments","Acknowledging loss and moving on", "Focusing on how the glass remains \"half-full\"","Finding the silver lining in a dark cloud", "Recognizing that loss is a natural part of life", "Embracing healthy grief", "Learning lessons from harsh consequences","Donating your time and talents to others", "Taking satisfaction in knowing how your efforts will aid others", "Creating a \"win-win\" scenario", "Giving even when you know repayment is not possible", "Being motivated to do a good deed","Motivating yourself with images of future success", "Using visualization to encourage progress", "Taking an imaginative or creative approach to problem solving", "Making dreams come true", "Gleaning insight from personal visions","Wanting something better", "Blazing your own trail", "Realizing there must be more to life", "Leaving an unhealthy situation behind", "Starting your own business", "Going on a retreat", "Seeking the \"still, small voice\"","Being delighted with your own achievements", "Recognizing your own talents and abilities", "Reveling in the good things life has to offer", "Indulging yourself", "Relaxing and unwinding", "Having everything you need in order to feel complete","Having more than you ever dreamed", "Being deeply thankful for all you've been given", "Recognizing the Hand of God in the gifts the Universe brings your way", "Experiencing transcendent joy", "Achieving domestic bliss","Showing your emotions freely", "Throwing yourself into romance", "Nursing a secret crush", "Indulging in romantic fantasy", "Starting a new relationship", "Recalling your first love", "Experiencing love for the first time", "Converting to a new religion","Being deeply committed to a cause", "Giving in to strong emotions, from excitement to depression", "Acting on intuition alone", "Solving problems intuitively", "Believing in and basing decisions on ideals instead of realities", "Bringing intuition or passion to the table","Allowing yourself to be moved by the plight of others", "Feeling strong emotions", "Possessing unusual sympathy or empathy", "Trusting your feelings to guide you", "Calling on psychic abilities", "Achieving unity with Spirit","Keeping a stiff upper lip", "Being brave and clear in the face of adverse circumstances", "Sharing experience as a way of comforting others", "Making fair and empathetic decisions", "Honoring the spirit, not just the letter, of the law","Making objective decisions", "Applying logic", "Reasoning your way out of a difficult situation", "Solving puzzles", "Thinking things through", "Emphasizing the facts", "Clearing your mind", "Seeking clarity","Refusing to make a decision without getting the facts", "Exploring both sides of an argument", "Arguing passionately for what you believe in", "Weighing the issues", "Encouraging the open exchange of ideas", "Discussing political or religious issues without getting \"hot under the collar\"","Being brave enough to see things as they really are", "Exercising your critical eye", "Being your own best critic", "Acknowledging that things don't always turn out as planned", "Moving past heartbreak to embrace a painful truth","Thinking over your plans before putting them into action", "Pausing to meditate or clear your mind", "Taking time to understand someone or something before criticizing it", "Resting", "Occupying your thoughts with a healthy distraction","Acting in your own best interest", "Choosing to stand up for yourself", "Not backing down from disagreement and discord", "Taking a stand", "Refusing to go along with an unethical plan", "Knowing when to bend the rules","Making the best of a bad situation", "Recovering from defeat", "Resetting expectations", "Making allowances for unexpected circumstances", "Helping others who find themselves in dire circumstances", "Changing the way you see the world", "Broadening your perspective through study or travel","Refusing to do something dishonest, even when there's no chance of ever being caught", "Handling a difficult situation with finesse", "Pointing out assumptions", "Acting ethically in public and in private", "Living a life that is beyond reproach","Honoring limits", "Respecting the rules", "Deciding to go on a diet for your health's sake", "Recognizing you cannot always be in control", "Identifying obstacles to further progress", "Refusing to think about unhealthy or unethical options", "Asking for assistance","Refusing to worry about what you cannot control", "Rejecting anxiety", "Judging your own performance with kindness and gentleness", "Using meditation to quiet a troubled mind", "Confronting nightmares and fears", "Drawing a conclusion and putting an issue out of your mind","Seeing the signs that you've reached your limits", "Paying attention to what your body is trying to tell you", "Giving in to the need for rest and renewal", "Acknowledging that you've hit bottom", "Committing to a turnaround", "Knowing the worst is over","Pursuing a course of study", "Asking good questions", "Investing time in study and practice", "Doing research", "Making a habit of learning new things", "Starting an investigation", "Outlining what you need to know", "Finding a mentor or teacher","Speaking your mind", "Making your opinions known", "Offering constructive criticism", "Sharing your knowledge", "Making insightful observations", "Pinpointing the problem", "Clarifying what others have said", "Giving clear direction to others", "Uncovering the truth","Exercising tact or using diplomacy", "Defusing a tense situation", "Knowing what to say and how to say it", "Making others feel comfortable and confident", "Bringing out the best in everyone", "Having a way with words", "Telling jokes", "Possessing a knack for music, math, art, or science","Expressing yourself with firmness and authority", "Rendering a final decision", "Consulting an expert", "Calling in advisors and consultants", "Coming to a final conclusion", "Reaching a beneficial agreement based on sound information","Outlining a plan for achieving prosperity", "Becoming aware of opportunities to improve income or health", "Realizing you have everything you need", "Appreciating everything the Universe has given you", "Receiving the perfect gift at the perfect time","Weighing options", "Comparing prices", "Determining the value of one option over another", "Juggling resources to make ends meet", "Making difficult choices based on what's best for your body or your bankbook", "Looking at the bottom line", "Asking for a second opinion on health issues","Finishing a project", "Setting and meeting standards", "Performing according to specifications", "Making something others value", "Creating something new", "Doing your part in a group project", "Delivering exactly what others have asked for","Saving for a rainy day", "Fasting as part of a spiritual practice", "Dieting in an effort to improve your body", "Abstaining from sex as a way of honoring a spiritual tradition or personal promise", "Being financially conservative", "Establishing a trust fund", "Opening a savings account","Recognizing your needs and taking action to fulfill them", "Doing as much as you can do with what little you have", "Admitting you need help", "Embracing the aid that comes your way", "Focusing on what you have versus what you don't", "Looking for the light at the end of the tunnel","Giving time, money, or effort to a charity", "Taking part in a group effort", "Lending your resources to others without expecting anything in return", "Making sure everyone is treated equally", "Working together toward a common goal", "Redistributing wealth, time, or attention", "Tithing", "Sharing credit for your success","Measuring progress toward your goal", "Looking at results with an eye toward improving performance", "Asking, \"How happy am I?\"","Coming up with ideas for improving your health or prosperity", "Deciding it's time for a change", "Expressing an honest opinion","Doing your best", "Bringing enthusiasm and zeal to your work", "Making an effort to be the best you can be", "Finding the work that is right for you", "Taking care of the small details", "Becoming a finely skilled craftsperson", "Building something with your hands", "Making a handmade gift","Investing time in learning or teaching a difficult task", "Restraining yourself from physical or financial extremes", "Making sacrifices as a way of achieving larger goals", "Breaking a complex task down into simple steps", "Wanting what you have", "Knowing the difference between needs and wants","Celebrating your physical and financial blessings", "Realizing how lucky or how blessed you are", "Being satisfied with your physical and financial achievements", "Taking best advantage of \"times of plenty\"","Enjoying a feast", "Showering friends or family with gifts","Learning the value of a dollar", "Starting a savings plan", "Taking the first steps toward getting out of debt", "Learning new physical tasks", "Discovering your sexuality", "Launching a diet, a weight-lifting program, or a health-related effort", "Learning by doing","Spending money wisely", "Saving for a rainy day", "Paying close attention to physical or financial details", "Knowing where every dollar goes", "Having safe sex", "Preferring facts to \"good feelings\"","Finding creative ways to \"make do\" with resources on hand", "Completing a new invention","Appreciating fine food, fine wine, beautiful art, beautiful bodies, or any of the better things in life", "Reveling in healthy sexuality", "Treating yourself", "Splurging on the occasional \"nice to have\" item", "Rewarding someone with compensation above and beyond expectations", "Having it all","Becoming debt-free", "Having more than enough to get by", "Making contributions to a savings plan", "Taking a new job with an eye toward advancing your career", "Buying life or health insurance", "Being confident in the bedroom", "Taking on the role of enforcer when called upon to do so"]


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

possibleStars = ["*", "*", "*", "*", "*", "*", ".",".",".",".", ":", "~", ",", "`", "'", "-"]
def starfield():
  stars = ""
  for i in range(4):
      for j in range(30):
          if (random.randint(0,20) <=1):
              stars = stars + random.sample(possibleStars, 1)[0]
          else:
              stars = stars + " "
      stars = stars + "\n"
  return stars

# This function adds linebreaks to format the text nicely for the printer, then sends the job to the printer
# It also puts the printer out of and back into its low-power mode because I was worried about excessive power consumption
# for a battery-powered device. This adds a wee bit of lag, but like, the game already has a massive amount of lag in the system.
def printFormatted(text, characters=30):
	p.wake()
	# p.linefeed(2)
	p.bold()
	lines = ['\n'.join(wrap(block, width=characters)) for block in text.splitlines()]
	p.print_text(starfield())
	for line in lines:
		p.print_text(line+"\n")
	p.print_text(starfield())
	p.linefeed(4)
	p.sleep()

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