sfondo = "sfondo.jpg"
import pygame
from pygame.locals import*
from sys import exit
import random
from random import randint
import time
from colors import rgb, hsv, hex

WINDOW_X_SIZE = 700
WINDOW_Y_SIZE = 500

def messagetoscreen(msg, position, color):
	text = font.render(msg, True, color)
	screen.blit(text, position)

def movimento(oggetto):
	oggetto[X] += oggetto[VX]
	oggetto[Y] += oggetto[VY]

def rimbalzo(pippo):
	if pippo[Y]+pippo[HEIGHT]>WINDOW_Y_SIZE:
		pippo[VY] = -pippo[VY]
	if pippo[X]+pippo[WIDTH]>WINDOW_X_SIZE:
		pippo[VX] = -pippo[VX]
	if pippo[X]<0:
		pippo[VX] = -pippo[VX]
	if pippo[Y]<0:
		pippo[VY] = -pippo[VY]

def rimbalzo2(pippo):
	if pippo[Y]+pippo[HEIGHT]>WINDOW_Y_SIZE:
		pippo[VY] = -pippo[VY]
	if pippo[Y]<0:
		pippo[VY] = -pippo[VY]

def bordi_sabbie_mobili(oggetto):
	if oggetto[X] < oggetto[VX]:
		oggetto[X] = oggetto[VX]

	if oggetto[Y] < oggetto[VY]:
		oggetto[Y] = oggetto[VY]

	if oggetto[Y] > WINDOW_Y_SIZE - oggetto[HEIGHT] + oggetto[VY]:
		oggetto[Y] = WINDOW_Y_SIZE - oggetto[HEIGHT] + oggetto[VY]

	if oggetto[X] > WINDOW_X_SIZE - oggetto[WIDTH] + oggetto[VX]:
		oggetto[X] = WINDOW_X_SIZE - oggetto[WIDTH] + oggetto[VX]

def a_on_b(a, b):
	a_center = (
			a[X] + a[WIDTH]/2,
			a[Y] + a[HEIGHT]/2
			)

	return a_center[X] > b[X] and\
		   a_center[X] < b[X] + b[WIDTH] and\
		   a_center[Y] > b[Y] and\
		   a_center[Y] < b[Y] + b[HEIGHT]

def render_time(time):
	print "mancano", time, "secondi", velocita[0]
def render_points(points):
	print points

screen = pygame.display.set_mode((WINDOW_X_SIZE, WINDOW_Y_SIZE), DOUBLEBUF | HWSURFACE, 32)
pygame.display.set_caption("Flying Mario")

velocita = [0.5, 0.05]

sfondo = pygame.image.load(sfondo)
sfondo = pygame.transform.scale(sfondo, (WINDOW_X_SIZE, WINDOW_Y_SIZE))
mario_image = pygame.image.load("./mario.png")
mario_image = pygame.transform.scale(mario_image, (100, 100))
mario = [70, 305, 0, 0, 100, 100, mario_image]
coin_image = pygame.image.load("./coin.png")
coin_image = pygame.transform.scale(coin_image, (65, 45))
coin = [705, random.randint(0, WINDOW_Y_SIZE), -4, 0, 100, 100, coin_image]
rainbowcoin_image = pygame.image.load("./RainbowCoin.png")
rainbowcoin_image = pygame.transform.scale(rainbowcoin_image, (120, 100))
rainbowcoin = [WINDOW_X_SIZE+50, random.randint(0, WINDOW_Y_SIZE - 80), -6, 8, 80, 80, rainbowcoin_image]
r = [WINDOW_X_SIZE/5, WINDOW_Y_SIZE/5, WINDOW_X_SIZE/1.5, WINDOW_Y_SIZE/1.5]



pygame.font.init()
font = pygame.font.SysFont(None, 35)

pygame.mixer.init()
suono = pygame.mixer.music.load("./suonocoin.mp3")

pygame.init()

trigger_pressed = False
done = False
score = 0
coinblit = True
x = 0
X, Y, VX, VY, WIDTH, HEIGHT, IMAGE = 0, 1, 2, 3, 4, 5, 6

blue = (26,35,126)

orologio = pygame.time.Clock()

def gameloop():

	done = False
	gameover = False
	time_remained = 30*60
	score = 0
	coinblit = True
	rainbowcoinblit = False
	X, Y, VX, VY, WIDTH, HEIGHT, IMAGE = 0, 1, 2, 3, 4, 5, 6
	x = 0
	speed = 200

	while not done:
		if gameover == True:
			while gameover == True:
				screen.fill((255, 255, 255))
				screen.blit(mario[IMAGE], (0, WINDOW_Y_SIZE-mario[HEIGHT]))
				pygame.draw.rect(screen, Color("#d50000"), (r[X], r[Y], r[2], r[3]), 3)
				messagetoscreen("Time's up!", (r[X] + 10, r[Y] + 30), (blue))
				messagetoscreen("Press SPACE to replay", (r[X] + 10, r[Y] + 90), (blue))
				messagetoscreen("ESC to exit", (r[X] + 10, r[Y] + 150), (blue))
				messagetoscreen("Your score:", (r[X] + r[2] - 230, r[Y] + r[3] - 70), (0, 0, 100))
				messagetoscreen(str(score), (r[X] + r[2] - 90, r[Y] + r[3] - 70), (13, 71, 161))
				if score > 29:
					messagetoscreen("Highscore!!!", (r[X] + r[2] - 230, r[Y] + r[3] - 40), (255, 50, 50))
				else:
					messagetoscreen("Not the Highscore...", (r[X] + r[2] - 230, r[Y] + r[3] - 40), Color("#737373"))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							exit()
						if event.key == pygame.K_SPACE:
							coin[X] = 705
							coin[Y] = random.randint(0 + coin[HEIGHT], WINDOW_Y_SIZE - coin[HEIGHT])
							coin[VX] = -4
							mario[X] = 10
							mario[Y] = 290
							mario[VX] = 0
							mario[VY] = 0
							gameloop()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit()
				if event.key == pygame.K_f:
					gameover = True

		time_remained -= 1
		if time_remained % 60 == 0:
			render_time(time_remained/60)
		if time_remained < 0:
			pygame.mixer.music.load("./game over.mp3")
			pygame.mixer.music.play(loops = 0, start = 0.0)
			gameover = True

		movimento(mario)
		movimento(coin)
		bordi_sabbie_mobili(mario)
		rimbalzo2(rainbowcoin)

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]:
			mario[VY] -= velocita[0]
		if pressed[pygame.K_DOWN]:
			mario[VY] += velocita[0]
		if pressed[pygame.K_RIGHT]:
			mario[VX] += velocita[0]
		if pressed[pygame.K_LEFT]:
			mario[VX] -= velocita[0]

		if a_on_b(mario, coin):
			coinblit = False
			pygame.mixer.music.load("./suonocoin.mp3")
			pygame.mixer.music.play(loops = 0, start = 0.0)
			score += 1
			coin[VX] -= 0.5
			velocita[0] += velocita[1]
			print score

		if coin[X] < 0 - coin[WIDTH] :
			coinblit = False

		if coinblit == False:
			coin[X] = WINDOW_X_SIZE + 10
			coin[Y] = random.randint(0 + coin[HEIGHT], WINDOW_Y_SIZE - coin[HEIGHT])
			coinblit = True

		if score == 3:
			rainbowcoinblit = True
			coinblit = False
		else:
			rainbowcoinblit = False

		if rainbowcoinblit == True:
			screen.blit(rainbowcoin[IMAGE], (rainbowcoin[X], rainbowcoin[Y]))
			movimento(rainbowcoin)
			messagetoscreen("Catch the Rainbow Coin!", (250, 15), (blue))
			messagetoscreen("+3", (rainbowcoin[X] + rainbowcoin[WIDTH]/2, rainbowcoin[Y] + rainbowcoin[HEIGHT]/2), (254, 255, 255))
			pygame.display.update()
			if a_on_b(mario, rainbowcoin):
				score += 3
				print score
				coin[VX] -= 0.7
				
				coinblit = True
				rainbowcoinblit = False
			if rainbowcoin[X] < 0:
				coinblit = True
				rainbowcoinblit = False
				#messagetoscreen("Oh no, you missed it!", (250, 15), (144, 44, 244))
				pygame.display.update()

		# movimento sfondo
		tempo_passato = orologio.tick(60)
		tempo_passato_sec = tempo_passato / 1000.0
		distanza_spostamento = tempo_passato_sec * speed

		if x < 0:
		  x = WINDOW_X_SIZE
		x -= distanza_spostamento

		screen.blit(sfondo,(x, 0))
		screen.blit(sfondo,(x - WINDOW_X_SIZE, 0))
		screen.blit(mario[IMAGE], (mario[X], mario[Y]))
		screen.blit(coin[IMAGE], (coin[X], coin[Y]))

		scores = font.render(str(score), True, (0, 0, 102))
		screen.blit(scores, (5, 5))
		tempo = font.render(str(time_remained/60), True, (0, 255, 255))
		screen.blit(tempo, (670, 5))
		pygame.display.update()

def start():
	start = False
	while not start:
		screen.fill((255, 255, 255))
		messagetoscreen("Move Mario with the arrows to collect all the coins!", (30, 50), (blue))
		messagetoscreen("Press SPACE to start", (30, 80), (blue))
		messagetoscreen("High score: 28 coins", (400, 400), (255, 50, 50))

		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					gameloop()
				elif event.key == pygame.K_ESCAPE:
					exit()

start()
