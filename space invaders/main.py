import pygame,random,keyboard
from pygame import mixer
pygame.init()
#==============================CONSTANTS==================================
W,H = 600,800
win = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
FPS = 30
score = 0
lives = 7
shootLoop = 0
lost = False
start = True

asteroidList = [pygame.image.load('asteroid1.png'),pygame.image.load('asteroid2.png')]
ufoList = [pygame.image.load('ufo.png'),pygame.image.load('ufo1.png')]
spsh = pygame.image.load('spaceship.png')
bg = pygame.image.load('bg.png')
game_over = pygame.image.load('gameover.png')
laser = pygame.image.load('laser.png')

mixer.music.load('background.wav')
mixer.music.play(-1)
laser_sound = mixer.Sound('laser.wav')
collision_sound = mixer.Sound('explosion.wav')
game_over_sound = mixer.Sound('gameoversound.wav')
#================================CLASSES==================================
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = spsh.convert_alpha()
		self.rect = self.surf.get_rect(center=(300,750))
		self.mask = pygame.mask.from_surface(spsh)
		self.speed = 20
	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] and self.rect.top > 5:
			self.rect.move_ip(0,-self.speed)
		if keys[pygame.K_s]and self.rect.bottom < 800:
			self.rect.move_ip(0,self.speed)
		if keys[pygame.K_a] and self.rect.left > 20:
			self.rect.move_ip(-self.speed,0)
		if keys[pygame.K_d]and self.rect.right < 580:
			self.rect.move_ip(self.speed,0)
	

class Rocks(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = random.choice(asteroidList).convert_alpha()
		self.rect = self.surf.get_rect(center = (
				random.randrange(50,550,30),
				random.randrange(-800,-100,50)

			))
		self.mask = pygame.mask.from_surface(random.choice(asteroidList))
		self.speed = random.randint(5,10)
	def update(self):
		global score
		self.rect.move_ip(0,self.speed)
		if self.rect.top > 800:
			self.kill()
			score += 1

class Ufo(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = random.choice(ufoList).convert_alpha()
		self.rect = self.surf.get_rect(center = (
				random.randrange(50,550,30),
				random.randrange(-200,-100,2)

			))
		self.mask = pygame.mask.from_surface(random.choice(ufoList))
		self.speed = random.randint(5,10)
	def update(self):
		global score,lives
		self.rect.move_ip(0,self.speed)
		if self.rect.top > 800:
			self.kill()
			if score >= 0:
				score -= 5
			lives -= 1

class Laser(pygame.sprite.Sprite):
	def __init__(self,i):
		super().__init__()
		self.surf = laser.convert_alpha()
		self.rect = self.surf.get_rect(center = (mainPlayer.rect.centerx,mainPlayer.rect.centery))
		self.mask = pygame.mask.from_surface(laser)
		self.speed = 15
		self.i = i
	def update(self):
		self.rect.move_ip(0,self.speed*self.i)
		if self.rect.bottom < 0:
			self.kill()
	def collide(self,obj):
		if collision(self,obj):
			self.kill()
			obj.kill()
			score+=3

#=======================STUFF=============================================

add_obstacle = pygame.USEREVENT + 1
pygame.time.set_timer(add_obstacle, random.randint(2000, 3000))

mainFont = pygame.font.SysFont('comicsans',50)

mainPlayer = Player()
ufos = pygame.sprite.Group()
rocks = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(mainPlayer)
#================================FUNCTIONS=================================
def drawGame(win):
	score_text = mainFont.render(f"Score: {score}", True, (255,255,255))
	lives_text = mainFont.render(f"Lives: {lives}", True, (255,255,255))
	win.blit(bg,(0,0))
	for sprite in all_sprites:
		win.blit(sprite.surf,sprite.rect)
		sprite.update()
	win.blit(score_text,(440,5))
	win.blit(lives_text,(5,5)) 
	if lost:
		win.blit(game_over,(0,0))
	pygame.display.flip()
def collision(sprite1,sprite2):
	if (pygame.sprite.collide_mask(sprite1,sprite2)) != None:
		return True
	else:
		return False
x = 0
#================================GAME LOOP=================================
run = True
while run:
	clock.tick(FPS)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == add_obstacle:
			new_ufo = Ufo()
			all_sprites.add(new_ufo)
			ufos.add(new_ufo)
			new_rock = Rocks()
			rocks.add(new_rock)
			all_sprites.add(new_rock)

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 7:
		shootLoop = 0

	keys = pygame.key.get_pressed()
	if keys[pygame.K_SPACE] and shootLoop == 0:
		if len(lasers.sprites())<3:
			laser_sound.play()
			new_laser = Laser(-1)
			lasers.add(new_laser)
			all_sprites.add(new_laser)
			shootLoop = 1

	for i,j in zip(rocks,ufos):
		if collision(i,mainPlayer):
			i.kill()
			lives-=1
			collision_sound.play()
		if collision(j,mainPlayer):
			collision_sound.play()
			j.kill()
			lives-=1
		for obj in lasers:
			if collision(obj,j):
				collision_sound.play()
				j.kill()
				obj.kill()
				score+=3

	if lives == 0:
		lost = True
		
	drawGame(win)

	if lost:
		pygame.mixer.music.pause()
		game_over_sound.play()
		pygame.time.delay(3000)
		run = False

pygame.quit()