==================
-------MUD--------
-By Will Langdale-
==================

==================
------v1.0--------
==================

==================
------INTRO-------
==================

Mud is a text adventure inspired by the experiences of people faced with 
problems so unfathomably life-changing that it's all they can do to keep 
living in the shadow of them. Its exact genesis came from someone who 
cared for their adult son who had suffered a traumatic brain injury. I 
felt that the medium of a game was an excellent fit for repeatedly 
attempting to surmount an insurmountable goal, and a text adventure in 
particular was germane to the sense of limitation in perception and 
potential action that I wanted to create.

Stylistically I was inspired by the work of Adam Cadre and Nick Montfort, 
both of whom expanded my idea of what a text adventure could be.

Music and sound effects are begged and borrowed from free to cheap 
libraries. Apologies to Daedelus and Aphex Twin, who I admittedly didn't 
look into licensing for this personal project, but whose music I love 
dearly.

Fonts are Basica by Qbotype and VCR OSD Mono by mrmanet, both from dafont.

Pixel "art" is all me.

===================
------RUNNING------
===================

NON COMPUTER LITERATES: Install the MSI in the "WindowsInstaller" folder. 
Double click the shortcut on the Desktop.

COMPUTER LITERATES: If you don't want to or can't install an MSI then you 
need to run it in Python. Python 2.7 comes with Macs, I believe, and should 
be pretty easy to install on Linux.

You'll need Python 2.7 and Pygame 1.9.1 for Python 2.7.

Download the repository and all the associated files, obviously.

Regardless of OS open the console window, navigate to the main dir and 
type "python mudpygame.py" to run the game.

===================
-----CONTROLS------
===================

Forget your mouse, it's all keyboard. Watch for when the top box lights up 
as that's your cue to enter some words.

SPACE generally moves the displayed text along. You can hold it down if 
you get bored.

ENTER will enter whatever you've typed.

Other than that it's all typed words and phrases that the game will 
interpret. Some important ones:

HELP will show you some basic commands.

QUIT will let you close the game after a YES/NO prompt.

WALK or GO will move you around, but just entering a direction is just as 
good. Game accepts NORTH/SOUTH/EAST/WEST as well as a few other options, 
but the quickest way to do it this just type one of N/E/S/W. "N" means the 
same as "WALK NORTH", for example.

THINK will let you know context-specific things you can do. It lists all 
the things you can do in an area, plus anything you can do with items you 
hold. Note that unless it's all you can do, it will omit LOOK and SEARCH 
commands.

LOOK can be done in general to see what's around, in a direction ("LOOK 
WEST") to see where stuff is, or on an item ("LOOK SCARF") to, well, look 
at it.

SEARCH can be done in general to search an area, or on a particular item 
to see if there's anything concealed within it.

And that's the basics! Context-specific commands will crop up, and THINK 
will be your friend in working them out. There's also some hidden ones 
that I didn't think it made sense not to handle - try WAIT a few times 
and see where it gets you.

===================
--TROUBLESHOOTING--
===================

The basic rule is: email me with what you did as best you can.

This was my first project in Python - or any programming language - so 
error handling is very rudimentary. There's an "errorlog.txt" in both the 
"dist" and "python" folder that error outputs should write to, so email me 
that file. Handled errors print something like [[Error]] to the game 
screen then restart the current traverse of the game.

As a first project this is very, very messy. If anyone dares look at my 
code I think you'll pretty easily see how my work gets more sophisticated 
as time goes on, but this has left some very messy interactions that seem 
to hang together for now. Added to this is how much of a bodge job it was 
to get it run as a standalone exe. Sorry if it errors, I'm a beginner.

===================
-----TECHNICAL-----
===================

I thought I'd write a brief section about how the game actually works and 
was built.

Mud2.py was the original script, and was a loose collection of functions 
and classes that encapsulated moving from room to room. When you type 
stuff in it checks your input against a couple of Python dictionaries and 
works out what you probably want to do from there. Each room and item is 
a class that returns text based on being look at or searched. There's also 
some loops that handle status ailments and time passing. Some of the bloat 
comes from my dislike of repetition - there's about 25 different ways you 
can move from one room to another. Another is what was at the time some 
very challenging code for very minor functions. The flare item had me 
attempting a poorly executed Dijkstra's algorithm.

Mudpygame.py is essentially a wrapper built on the Pygame module, and 
although I learned more writing the Mud script, my most hard-fought 
victories came here. Two concurrent processes are started, mud2 and the 
Pygame wrapper, with the multiprocessing module used to pass information 
between them. It was as I wrote this that the elements of what 
"object-oriented" programming really meant finally came together, and the 
result is a much more coherant (though not perfect) class-based script.

From here my greatest desire is to learn how to write "pythonic" code. 
Looking back on the project my work is rudimentary, unplanned and messy, 
and while this is to be expected from a learning project, I understand 
that neat, comprehensible, efficient code is at the heart of Python. I 
can't wait to plan my next project ahead of building it now that I know 
what I know.
