import pygame, sys, string, multiprocessing, traceback, random
import mud2
from pygame.locals import *

WINDOW = (800, 600)
CAPTION = "Mud"

BROWN = (51, 29, 9, 255)
GREY = (222, 219, 217, 255)
MOON = (103, 100, 112, 255)
BGGREY = (84, 84, 84, 255)
BLUE = (199, 211, 237, 255)
BLACK = (0, 0, 0, 255)
AFTERNOON = (193, 186, 0, 255)
SUNK = (193, 153, 0, 255)
ORANGE = (193, 91, 0, 255)
DARKBLUE = (0, 25, 107, 255)
ABBLACK = (0, 7, 30, 255)
COLDICT = {
"BROWN": BROWN,
"GREY": GREY,
"BGGREY": BGGREY,
"BLUE": BLUE,
"BLACK": BLACK,
"AFTERNOON": AFTERNOON,
"SUNK": SUNK,
"ORANGE": ORANGE,
"DARKBLUE": DARKBLUE,
"ABBLACK": ABBLACK
}

PLANE = "plane"
RIVER = "river"
WHISPERS = "whispers"
BIRDS = "birds"
DARK = "dark"
BELLS = "bells"
SOUNDDICT = {}

TITLE = "basica.ttf", 200
BODY = "vcr.ttf", 20
BG = "bg1.png"
BGTOP = "top6.png"
BGPLANE = "plane5050.png"
FIGURE = "figure.png"
LINES = 22

NONE = 5
UP = 8
MOVE = 4

class Bodytext(object):
	"""The body font"""
	def __init__(self, text, location):
		self.font = BODY
		self.colour = GREY
		self.text = self.font.render(text, False, self.colour)
		self.rect = self.text.get_rect(topleft=location)
	
	def draw(self, surface):
		surface.blit(self.text, self.rect)

class Bodycredits(Bodytext):
	"""The body font for the credits"""
	def __init__(self, text, location):
		self.font = BODY
		self.colour = GREY
		self.text = self.font.render(text, False, self.colour)
		self.rect = self.text.get_rect(center=location)
	
	def draw(self, surface):
		surface.blit(self.text, self.rect)

class TitleText(object):
	"""The title font"""
	def __init__(self, location):
		self.font = TITLE
		self.colour = GREY
		self.text = self.font.render("MUD", False, self.colour)
		self.rect = self.text.get_rect(center=location)
	
	def draw(self, surface):
		surface.blit(self.text, self.rect)

class BgImage(object):
	"""The scrolling background and black alpha for light effects"""
	def __init__(self):
		self.bgcomp = pygame.Surface((800, 600))
		self.bg = BG
		self.blackalpha = 255
		self.blackalphatgt = 255
		self.blackground = pygame.Surface((800, 600))
		
		self.ticks = pygame.time.get_ticks()
		self.ticks2 = pygame.time.get_ticks()
		self.xpos = 100
		self.ypos = 0
		self.timecol = TimeFilter()
		
		self.stars = []
		self.starstick = pygame.time.get_ticks()
		self.sunpos = (400, -200)
		self.sun = (MOON, self.sunpos, 100)
		self.suntick = pygame.time.get_ticks()
		self.figure = FIGURE
		
		self.cues = {}
	
	def draw(self, surface, end):
		if end == False:
			self.move()
		else:
			self.movedown()
		self.blackfade()
		self.combine(end)
		surface.blit(self.bgcomp, (0,0))
	
	def combine(self, end):
		if end == True:
			self.blackground.fill(ABBLACK)
			self.blackground.set_alpha(255)
			self.stardraw(self.blackground)
			self.sundraw(self.blackground)
			self.blackground.blit(self.figure, (397, (0 - self.ypos) - 14))
			self.bgcomp.blit(self.blackground, (0,0))
			self.bgcomp.blit(self.bg, (0,0), (self.xpos, self.ypos, 800, 600))
		else:
			self.blackground.fill(BLACK)
			self.blackground.set_alpha(self.blackalpha)
			self.bgcomp.blit(self.bg, (0,0), (self.xpos, self.ypos, 800, 600))
			self.bgcomp.blit(self.blackground, (0,0))
	
	def movedown(self):
		time = pygame.time.get_ticks() - self.ticks
		if time >= 30:
			if self.ypos > -450:
				self.ypos -= 0.5
				self.ticks = pygame.time.get_ticks()
	
	def sundraw(self, surface):
		time = pygame.time.get_ticks()
		
		if time - self.suntick >= 40:
			if self.ypos < -100 and self.sunpos[1] < 390:
				x = self.sunpos[0]
				y = self.sunpos[1] + 1
				self.sunpos = (x, y)
				self.sun = (MOON, self.sunpos, 100)
			self.suntick = pygame.time.get_ticks()
		
		pygame.draw.circle(surface, *self.sun)
	
	def stardraw(self, surface):
		time = pygame.time.get_ticks()
		
		if len(self.stars) < 50:
			if time - self.starstick >= 500:
				x = random.randint(5, 800)
				y = random.randint(5, 600)
				self.stars.append((x,y))
				self.starstick = pygame.time.get_ticks()
		
		if len(self.stars) > 0:
			for i in self.stars:
				rec = (i[0], i[1], 3, 3)
				pygame.draw.rect(surface, GREY, rec)
	
	def move(self):
		if self.xpos <= 0:
			self.xpos = 1594
		time = pygame.time.get_ticks() - self.ticks
		if time >= 30:
			self.xpos -= 0.5
			self.ticks = pygame.time.get_ticks()
	
	def blackfade(self):
		time = pygame.time.get_ticks() - self.ticks2
		if time >= 10:
			if self.blackalpha != self.blackalphatgt:
				if self.blackalpha > self.blackalphatgt:
					if self.blackalpha > self.blackalphatgt + 16:
						self.blackalpha -= 15
					else:
						self.blackalpha -= 1
				elif self.blackalpha < self.blackalphatgt:
					if self.blackalpha < self.blackalphatgt - 16:
						self.blackalpha += 15
					else:
						self.blackalpha += 1
			self.ticks2 = pygame.time.get_ticks()
	
	def cuecheck(self, topline):
		played = ""
		for i in self.cues.keys():
			if i == topline[0][:10]:
				self.blackalphatgt = self.cues[i]
				played = i
		if played != "":
			del self.cues[played]
	
	def alpha(self, alpha, cue):
		self.cues[cue] = alpha

class Reset(object):
	def __init__(self):
		self.cues = {}
	
	def cuecheck(self, topline):
		played = ""
		for i in self.cues.keys():
			if i == topline[0][:10]:
				played = i
				del self.cues[played]
				return "reset"
	
	def addcue(self, cue):
		self.cues[cue] = "reset"

class TimeFilter(object):
	"""The filter for time colour effects. Now only used on title menu"""
	def __init__(self):
		self.sky = pygame.Surface((800, 600))
		self.colourlist = [BLUE, AFTERNOON, SUNK, ORANGE, DARKBLUE, ABBLACK, BLACK]
		self.colour = pygame.Color(*BLUE)
		self.colourtgt = pygame.Color(*AFTERNOON)
		self.ticks = pygame.time.get_ticks()
		self.ticks2 = pygame.time.get_ticks()
		self.ticks2index = 0
		self.sunstart = (1000, -100)
		self.sunpos = (400, 300)
		self.sun = (GREY, self.sunpos, 100)
		self.stars = []
		self.starstick = pygame.time.get_ticks()
	
	def draw(self, surface):
		self.colchange()
		self.sky.fill(self.colour)
		pygame.draw.circle(self.sky, *self.sun)
		self.stardraw(surface)
		self.sky.set_alpha(40)
		surface.blit(self.sky, (0, 0))
	
	def menu(self):
		t = pygame.time.get_ticks() - self.ticks2
		i = t / 10000
		self.sunmove(t)
		if t >= 65000:
			self.ticks2 = pygame.time.get_ticks()
		else:
			if self.colour == self.colourtgt:
				if i != self.ticks2index:
					if i >= len(self.colourlist) - 1:
						self.colmove()
					else:
						self.colmove(self.colourlist[i])
						self.ticks2index = i
	
	def stardraw(self, surface):
		time = pygame.time.get_ticks()
		
		if self.colourtgt == DARKBLUE \
		or self.colourtgt == ABBLACK \
		or self.colourtgt == BLACK:
			if len(self.stars) < 20:
				if time - self.starstick >= 500:
					x = random.randint(5, 800)
					y = random.randint(5, 200)
					self.stars.append((x,y))
					self.starstick = pygame.time.get_ticks()
			
			if len(self.stars) > 0:
				for i in self.stars:
					rec = (i[0], i[1], 3, 3)
					pygame.draw.rect(surface, GREY, rec)
		else:
			del self.stars[:]
	
	def sunmove(self, tick):
		i = int((tick / 12000.0) * 100)
		sunx = self.sunstart[0] - (3 * i)
		suny = self.sunstart[1] + i
		self.sunpos = (sunx, suny)
		self.sun = (GREY, self.sunpos, 100)
	
	def colmove(self, *col):
		if len(col) != 0:
			if col[0] in self.colourlist:
				self.colourtgt = pygame.Color(*col[0])
		else:
			for i, v in enumerate(self.colourlist):
				if self.colour == pygame.Color(*v):
					if i == len(self.colourlist) - 1:
						self.colourtgt = pygame.Color(*self.colourlist[0])
					else:
						self.colourtgt = pygame.Color(*self.colourlist[i + 1])
	
	def colchange(self):
		if self.colour != self.colourtgt:
			if (pygame.time.get_ticks() - self.ticks) >= 10:
				a = self.colour.normalize()
				b = self.colourtgt.normalize()
				newcol = [0, 0, 0, 0]
				for rgb, value in enumerate(a):
					nval = int(value * 255)
					if nval > int(b[rgb] * 255):
						nval -= 1
						newcol[rgb] = nval
					elif nval < int(b[rgb] * 255):
						nval += 1
						newcol[rgb] = nval
					else:
						newcol[rgb] = nval
				x = tuple(newcol)
				self.colour = pygame.Color(*x)
				self.ticks = pygame.time.get_ticks()

class EndMenu(object):
	"""The very final winning screen of the game"""
	def __init__(self):
		self.started = False
	
	def draw(self, surface):
		self.music()
		
	def music(self):
		if self.started == False:
			pygame.mixer.music.stop()
			pygame.mixer.music.load("credits.ogg")
			pygame.mixer.music.play()
		self.started = True

class Smoke(object):
	"""The smoke on the title menu"""
	def __init__(self, pos):
		self.pos = pos
		self.size = (2, 2)
		self.alpha = 240
		self.smokesurface = pygame.Surface(self.size)
		self.collist = [GREY, BGGREY, BLACK, ABBLACK]
		self.smokecol = self.collist[random.randint(0, 3)]
		self.maxx = self.pos[0] + 5 + random.randint(0, 3)
		self.ticks = pygame.time.get_ticks()
		self.done = False
	
	def draw(self, surface):
		if self.done == False:
			self.move()
			self.smokesurface.fill(self.smokecol)
			self.smokesurface.set_alpha(self.alpha)
			surface.blit(self.smokesurface, self.pos)
	
	def move(self):
		time = pygame.time.get_ticks()
		if time - self.ticks >= 50:
			if self.size[0] < 7:
				x = self.size[0] + 1
				y = self.size[1] + 1
				self.size = (x, y)
				self.smokesurface = pygame.Surface(self.size)
			
			if self.pos[0] < self.maxx:
				x1 = self.pos[0] + 1
				y1 = self.pos[1] - 3
				self.pos = (x1, y1)
			else:
				if self.done == False:
					x1 = self.pos[0]
					y1 = self.pos[1] - 2
					self.pos = (x1, y1)
					self.alpha -= 10
					if self.alpha == 0:
						self.done = True
			
			self.ticks = pygame.time.get_ticks()

class TitleMenu(object):
	"""The title menu"""
	def __init__(self):
		self.top = BGTOP
		self.skyboxcol = BLUE
		self.skyboxrec = pygame.Surface((800, 500))
		self.titletext = TitleText((400, 200))
		self.light = TimeFilter()
		self.plane = BGPLANE
		self.smokes = []
		self.ticks = pygame.time.get_ticks()
		self.text = "Press [SPACE] to play"
		self.textprint = Bodycredits(self.text, (400, 560))
		self.ticks2 = pygame.time.get_ticks()
	
	def draw(self, surface):
		self.skyboxrec.fill(self.skyboxcol)
		self.skyboxrec.set_alpha(30)
		surface.blit(self.skyboxrec, (0, 0))
		surface.blit(self.top, (0, 230))
		surface.blit(self.plane, (300, 480))
		self.smokedraw(surface)
		self.titletext.draw(surface)
		if pygame.time.get_ticks() - self.ticks2 > 15000:
			self.textprint.draw(surface)
		self.light.draw(surface)
		self.light.menu()
	
	def smokedraw(self, surface):
		time = pygame.time.get_ticks()
		smokes = self.smokes
		
		for i, v in enumerate(smokes):
			if v.done == True:
				del self.smokes[i]
		
		if len(smokes) < 15:
			if time - self.ticks >= 100:
				x = Smoke((340, 500))
				self.smokes.append(x)
				self.ticks = pygame.time.get_ticks()
			
		for i in self.smokes:
			i.draw(surface)

class EndCredits(object):
	"""Final credits"""
	def __init__(self, artifacts):
		self.bgcol = BLACK
		self.bgrec = (0, 0, 800, 600)
		self.credtext = "MUD. By Will Langdale."
		self.credprint = Bodycredits(self.credtext, (400, 200))
		self.artifacts = artifacts
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.bgcol, self.bgrec)
		if self.artifacts == [False, False, False]:
			self.credtext = "Find them in the earth."
			self.credprint = Bodycredits(self.credtext, (400, 200))
			self.credprint.draw(surface)
		elif self.artifacts == [True, False, False]:
			self.credtext = "Alone amongst the stone."
			self.credprint = Bodycredits(self.credtext, (400, 200))
			self.credprint.draw(surface)
		elif self.artifacts == [True, True, False]:
			self.credtext = "Lost beneath the endless mud."
			self.credprint = Bodycredits(self.credtext, (400, 200))
			self.credprint.draw(surface)
		elif self.artifacts == [True, True, True]:
			self.credtext = ["MUD", "By Will Langdale", " ", "Created Summer/Autumn 2014 in Python and Pygame", " ", " ", "MUSIC", " ", "Aphex Twin - aisatsana [102] (2014)", "Daedelus - Country of Conquest (2014)", " ", " ", "Thankyou for playing. Please let me know what you think."]
			lineh = BODY.get_linesize()
			for i, v in enumerate(self.credtext):
				line = Bodycredits(v, (400, 100 + lineh * i))
				line.draw(surface)
		else:
			self.credtext = "MUD"
			self.credprint = Bodycredits(self.credtext, (400, 200))
			self.credprint.draw(surface)

class SFXPlay(object):
	"""Handles sound cues"""
	def __init__(self):
		self.cues = {}
		self.dict = SOUNDDICT
	
	def play(self, sound):
		sound.play()
	
	def cuecheck(self, topline):
		played = ""
		for i in self.cues.keys():
			if self.cues[i] == topline[0][:10]:
				self.play(i)
				played = i
		if played != "":
			del self.cues[played]
	
	def addsound(self, sound, cue):
		self.cues[self.dict[sound]] = cue

class Music(object):
	def __init__(self):
		self.menu = "menu.ogg"
		self.credits = "credits.ogg"
		self.main = "main.ogg"
		self.cave = "cave.ogg"
		self.musiclib = {
			self.menu: "menu",
			self.credits: "credits",
			self.cave: "cave",
			self.main: "main"
			}
		
		self.cues = {}
	
	def change(self, music, rep):
		pygame.mixer.music.stop()
		for i in self.musiclib.keys():
			if music == self.musiclib[i]:
				pygame.mixer.music.load(i)
		if rep == 0:
			pygame.mixer.music.play()
		else:
			pygame.mixer.music.play(rep)
	
	def cuecheck(self, topline):
		played = ""
		for i in self.cues.keys():
			if self.cues[i] == topline[0][:10]:
				self.change(*i)
				played = i
		if played != "":
			del self.cues[played]
	
	def addmusic(self, name, cue):
		music = name[0]
		rep = name[1]
		
		for i in self.musiclib.keys():
			if music == self.musiclib[i]:
				self.cues[name] = cue

class TextBox(object):
	"""Text box at top of input"""
	def __init__(self):
		self.lineh = BODY.get_linesize()
		self.boxheight = self.lineh * 2
		self.box = pygame.Surface((700, self.boxheight))
		self.currentalpha = 0
		self.ticks = pygame.time.get_ticks()
	
	def draw(self, surface, alpha, display):
		self.box.fill(BGGREY)
		
		if alpha != self.currentalpha:
			if alpha > self.currentalpha:
				if (pygame.time.get_ticks() - self.ticks) >= 10:
					self.currentalpha += 5
					self.ticks = pygame.time.get_ticks()
					self.box.set_alpha(self.currentalpha)
			elif alpha < self.currentalpha:
				if (pygame.time.get_ticks() - self.ticks) >= 10:
					self.currentalpha -= 5
					self.ticks = pygame.time.get_ticks()
					self.box.set_alpha(self.currentalpha)
		else:
			self.box.set_alpha(self.currentalpha)
		
		if display == True:
			space = Bodytext("[SPACE]", (5, self.lineh / 2))
			space.draw(self.box)
		
		surface.blit(self.box, (50, 50))

class Control(object):
	"""Runs the game"""
	def __init__(self, pyg_event, pyg_out, pyg_in, pyg_queue):
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.done = False
		self.keys = pygame.key.get_pressed()
		self.textline = ""
		self.lineh = BODY.get_linesize()
		self.text = Bodytext(self.textline, (55, 50 + (self.lineh / 2)))
		self.status = "menu" # prompt / display / menu / credits / end
		self.complete = False
		self.listin = []
		self.listtrunc = []
		self.listdisplay = []
		self.displaytick = pygame.time.get_ticks()
		self.pyg_event = pyg_event
		self.pyg_out = pyg_out
		self.pyg_in = pyg_in
		self.pyg_queue = pyg_queue
		self.textbox = TextBox()
		self.titlemenu = TitleMenu()
		self.artifacts = []
		self.credits = ""
		self.bg = BgImage()
		self.sfx = SFXPlay()
		self.reset = Reset()
		self.end = EndMenu()
		self.music = Music()
		self.music.change("menu", -1)
	
	def events(self):
		"""Handles keyboard input"""
		for e in pygame.event.get():
			self.keys = pygame.event.get()
			if e.type == QUIT:
				self.done = True
			if e.type == KEYDOWN:
				if pygame.key.name(e.key) in (string.letters + string.digits):
					if self.status == "prompt":
						if BODY.size(self.textline)[0] < 680:
							self.textline += pygame.key.name(e.key)
					elif self.status == "menu":
						PLANE.play()
						self.status = "display"
				#elif e.key == K_F1:
				#	# Just for debugging the end
				#	self.complete = True
				#	self.status = "end"
				elif e.key == K_BACKSPACE:
					if self.status == "prompt":
						self.textline = self.textline[:-1]
					elif self.status == "menu":
						PLANE.play()
						self.status = "display"
				elif e.key == K_SPACE:
					if self.status == "display":
						self.scroll(self.listtrunc.pop(0))
						self.displaytick = pygame.time.get_ticks()
						if len(self.listtrunc) == 0:
							self.status = "prompt"
					elif self.status == "prompt":
						self.textline += " "
					elif self.status == "menu":
						PLANE.play()
						self.status = "display"
					elif self.status == "credits":
						self.done = True
					elif self.status == "end":
						self.scroll(self.listtrunc.pop(0))
						self.displaytick = pygame.time.get_ticks()
						if len(self.listtrunc) == 0:
							self.status = "credits"
				elif e.key == K_RETURN:
					if self.status == "prompt":
						del self.listin[:]
						del self.listtrunc[:]
						self.scroll([self.textline.upper().lstrip()])
						self.displaytick = pygame.time.get_ticks()
						self.pyg_in.send(self.textline)
						self.textline = ""
					elif self.status == "menu":
						PLANE.play()
						self.status = "display"
				self.text = Bodytext(self.textline.lstrip(), (55, 50 + (self.lineh / 2)))
	
	def draw(self):
		"""Draws everything"""
		if self.status == "menu":
			self.titlemenu.draw(self.screen)
		elif self.status == "credits":
			if self.credits == "":
				self.credits = EndCredits(self.artifacts)
			self.credits.draw(self.screen)
		elif self.status == "end":
			self.screen.fill(BLUE)
			self.end.draw(self.screen)
			self.bg.draw(self.screen, True)
			self.focus()
			self.printtext2()
			self.text.draw(self.screen)
		else:
			self.screen.fill(BROWN)
			self.bg.draw(self.screen, False)
			self.focus()
			self.printtext2()
			if self.listdisplay != []:
				self.sfx.cuecheck(self.listdisplay[0])
				self.bg.cuecheck(self.listdisplay[0])
				self.music.cuecheck(self.listdisplay[0])
				reset = self.reset.cuecheck(self.listdisplay[0])
				if reset == "reset":
					del self.listdisplay[:]
			self.text.draw(self.screen)
	
	def focus(self):
		"""Changes text entry box based on prompt status"""
		if self.status == "prompt":
			self.textbox.draw(self.screen, 120, False)
		elif self.status == "display":
			self.textbox.draw(self.screen, 50, True)
		else:
			pass
	
	def recieve(self):
		"""Gets info from mud2"""
		if self.status == "display" or self.status == "prompt":
			while not self.pyg_queue.empty():
				self.listin.append(self.pyg_queue.get())
				listintest = self.listin
				for index, value in enumerate(listintest):
					if isinstance(value, mud2.MediaEvent):
						if value.type == "sound":
							sound = self.listin.pop(index)
							cue = listintest[index - 1][:10]
							self.sfx.addsound(sound.name, cue)
						elif value.type == "bg":
							bgfx = self.listin.pop(index)
							try:
								cue = listintest[index - 1][:10]
								self.bg.alpha(bgfx.name, cue)
							except IndexError:
								self.bg.blackalphatgt = bgfx.name
						elif value.type == "music":
							music = self.listin.pop(index)
							try:
								cue = listintest[index - 1][:10]
								self.music.addmusic(music.name, cue)
							except IndexError:
								self.music.change(*music.name)
						elif value.type == "reset":
							self.listin.pop(index)
							cue = listintest[index - 1][:10]
							self.reset.addcue(cue)
						elif value.type == "end":
							self.listin.pop(index)
							self.complete = True
						else:
							self.listin.pop(index)
					elif isinstance(value, Artifacts):
						self.listin.pop(index)
						self.artifacts = value.artifacts
				self.listtrunc = self.linetrunc(self.listin)
				self.status = "display"
	
	def linetrunc(self, text):
		"""Breaks text into manageable lines"""
		toreturn = []
		for i in text:
			phrase = []
			line = ""
			word = ""
			for x in i:
				if BODY.size(line + word)[0] < 700:
					if x != " ":
						word += x
					else:
						word += x
						line += word
						word = ""
					if x == "." or x == "?" or x == "~":
						line += word
						phrase.append(line.lstrip())
						toreturn.append(phrase)
						phrase = []
						line = ""
						word = ""
				else:
					word += x
					phrase.append(line.lstrip())
					line = ""
					if x == "." or x == "?" or x == "~":
						line += word
						phrase.append(line.lstrip())
						toreturn.append(phrase)
						phrase = []
						line = ""
						word = ""
			else:
				if line == " ":
					phrase.append(" ")
			toreturn.append(phrase)
		
		toreturnclean = []
		for i in toreturn:
			if i != []:
				toreturnclean.append(i)
		return toreturnclean
	
	def scroll(self, newline):
		"""Moves the entered text by a line, entering a new one"""
		self.listdisplay.insert(0, newline)
		linestest = self.listdisplay
		linesa = 0
		for i, v in enumerate(linestest):
			for w in v:
				linesa += 1
				if linesa > LINES:
					self.listdisplay[i].remove(w)
		self.listdisplay = [x for x in self.listdisplay if x != []]
	
	def printtext2(self):
		"""Prints the lines to be displayed"""
		time = (pygame.time.get_ticks() - self.displaytick)/10
		count = 0
		for index, text in enumerate(self.listdisplay):
			if count < LINES:
				if len(text) == 1:
					if index == 0:
						Bodytext(text[0][:time], (50, (50 + (2.5 * self.lineh) + (self.lineh * count)))).draw(self.screen)
					else:
						Bodytext(text[0], (50, (50 + (2.5 * self.lineh) + (self.lineh * count)))).draw(self.screen)
					count += 1
				else:
					if index == 0:
						for i, item in enumerate(text):
							if i > 0:
								previt = 0
								for p in text[i - 1::-1]:
									previt += len(p)
								if time > previt:
									Bodytext(item[:time - previt], (50, (50 + (2.5 * self.lineh) + (self.lineh * count)))).draw(self.screen)
								count += 1
							else:
								Bodytext(item[:time], (50, (50 + (2.5 * self.lineh) + (self.lineh * count)))).draw(self.screen)
								count += 1
					else:
						for item in text:
							Bodytext(item, (50, (50 + (2.5 * self.lineh) + (self.lineh * count)))).draw(self.screen)
							count += 1
	
	def gamequit(self):
		"""Checks if the script has quit"""
		if self.pyg_event.is_set() == True:
			self.status = "credits"
	
	def loop(self):
		"""Game loop"""
		while not self.done:
			self.clock.tick(60)
			self.events()
			self.recieve()
			self.draw()
			self.gamequit()
			if self.complete == True:
				if len(self.listdisplay) > 0:
					if self.listdisplay[0] == ["Endless filth."]:
						self.status = "end"
			pygame.display.update()

def main(pyg_event, pyg_out, pyg_in, pyg_queue):
	"""Pygame's wrapper - starts game, loop, etc"""
	global TITLE
	global BODY
	global BG
	global BGTOP
	global BGMOUNT
	global BGPLANE
	global FIGURE
	
	global PLANE
	global RIVER
	global WHISPERS
	global BIRDS
	global DARK
	global BELLS
	global SOUNDDICT
	
	pygame.init()
	
	pygame.display.set_caption(CAPTION)
	pygame.display.set_mode(WINDOW)
	pygame.key.set_repeat(500, 50)
	
	TITLE = pygame.font.Font("basica.ttf", 200)
	BODY = pygame.font.Font("vcr.ttf", 20)
	
	BG = pygame.image.load("bg1.png")
	BGTOP = pygame.image.load("top6.png").convert_alpha()
	BGPLANE = pygame.image.load("plane5050.png").convert_alpha()
	FIGURE = pygame.image.load("figure.png").convert_alpha()
	
	PLANE = pygame.mixer.Sound("plane.ogg")
	RIVER = pygame.mixer.Sound("river.ogg")
	WHISPERS = pygame.mixer.Sound("whispers.ogg")
	BIRDS = pygame.mixer.Sound("birds.ogg")
	DARK = pygame.mixer.Sound("dark.ogg")
	BELLS = pygame.mixer.Sound("bells.ogg")
	SOUNDDICT["PLANE"] = PLANE
	SOUNDDICT["RIVER"] = RIVER
	SOUNDDICT["WHISPERS"] = WHISPERS
	SOUNDDICT["BIRDS"] = BIRDS
	SOUNDDICT["DARK"] = DARK
	SOUNDDICT["BELLS"] = BELLS
	
	Control(pyg_event, pyg_out, pyg_in, pyg_queue).loop()
	
	pygame.quit()
	sys.exit()

"""The wrap for the mud script"""

class Artifacts(object):
	def __init__(self, artifacts):
		self.artifacts = artifacts

deaths = 0
alive = True
artifacts = [False, False, False]
errornum = 0

def container(pyg_event, pyg_out, pyg_in, pyg_queue):
	global alive
	
	while alive == True:
		mud(pyg_event, pyg_out, pyg_in, pyg_queue)

def mud(pyg_event, pyg_out, pyg_in, pyg_queue):
	global deaths
	global artifacts
	global errornum
	
	try:
		mud2.start(deaths, False, False, artifacts, True, pyg_event, pyg_out, pyg_in, pyg_queue)
	except mud2.DeathError as why:
		pyg_queue.put(str(why.value))
		artifacts = why.art
		artisend = Artifacts(why.art)
		pyg_queue.put(artisend)
		reload(mud2)
		deaths += 1
	except (SystemExit, KeyboardInterrupt):
		sys.exit()
	except:
		errorlog = open("errorlog.txt", "a")
		errorlog.write("ERROR " + str(errornum) + "\n")
		errorlog.write("-------" + "\n\n")
		errorlog.write(str(sys.exc_info()) + "\n")
		errorlog.write(traceback.format_exc() + "\n")
		errorlog.write(str(mud2.textrecord) + "\n\n")
		errorlog.close()
		errornum += 1
		mud2.tensetext("[[Error]]. Your input has been recorded for debugging. Your current traverse has restarted.")
		reload(mud2)

if __name__ == '__main__':
	pyg_event = multiprocessing.Event()
	pyg_in, pyg_out = multiprocessing.Pipe()
	pyg_queue = multiprocessing.Queue()
	
	pyg_wrap = multiprocessing.Process(
	name = "Pygame interpreter", 
	target = main, 
	args = (pyg_event, pyg_out, pyg_in, pyg_queue))
	
	pyg_game = multiprocessing.Process(
	name = "Mud script", 
	target = container, 
	args = (pyg_event, pyg_out, pyg_in, pyg_queue))
	
	pyg_wrap.start()
	pyg_game.start()