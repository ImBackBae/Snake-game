import pygame
from random import randint
import os
import keyboard

class Snake():
	def __init__(self, side, screen):
		self.body_part = 3
		self.snake_coord = [WIDTH//side//2, HEIGHT//side//2]
		self.snake_coords = []
		self.side = side
		self.screen = screen
		self.point = 0

	def create_snake(self):
		self.snake_coords.append(tuple(self.snake_coord))
		pygame.draw.rect(self.screen, WHITE, (self.side*self.snake_coord[0], self.side*self.snake_coord[1], self.side-1, self.side-1))
		if len(self.snake_coords) > self.body_part:
			pygame.draw.rect(self.screen, BLACK, (self.side*self.snake_coords[0][0], self.side*self.snake_coords[0][1], self.side-1, self.side-1))
			del self.snake_coords[0]
			
	def move(self, direction):
		if direction == "left":
			self.snake_coord[0] -= 1
		elif direction == "right":
			self.snake_coord[0] += 1
		elif direction == "up":
			self.snake_coord[1] -= 1
		elif direction == "down":
			self.snake_coord[1] += 1

	def create_food(self):
		self.food_coord = [randint(0, WIDTH//self.side-1), randint(0, HEIGHT//self.side-2)]
		if tuple(self.food_coord) in self.snake_coords:
			self.create_food()

	def draw_food(self):
		pygame.draw.circle(self.screen, WHITE, (self.side*self.food_coord[0]+self.side//2, self.side*self.food_coord[1]+self.side//2), self.side//2)

	def eat(self):
		if self.snake_coord == self.food_coord:
			self.body_part = self.body_part + 1
			pygame.draw.circle(self.screen, BLACK, (self.side*self.food_coord[0]+self.side//2, self.side*self.food_coord[1]+self.side//2), self.side//2)
			self.create_food()
			self.point += 1

	def turn(self):
		if self.snake_coord[0] >= WIDTH//self.side:
			self.snake_coord = [0, self.snake_coord[1]]
		if self.snake_coord[1] >= HEIGHT//self.side:
			self.snake_coord = [self.snake_coord[0], 0]
		if self.snake_coord[0] == -1:
			self.snake_coord = [WIDTH//self.side - 1, self.snake_coord[1]]
		if self.snake_coord[1] == -1:
			self.snake_coord = [self.snake_coord[0], HEIGHT//self.side - 1]
		

	def game_over(self):
		x, y = self.snake_coords[-1]
		for body_part in self.snake_coords[:-1]:
			if x == body_part[0] and y == body_part[1]:
				return True
		return False

	def run(self, direction):
		self.create_snake()
		self.move(direction)
		self.draw_food()
		self.turn()
		self.eat()

def start(snake):
	snake.screen.fill(BLACK)
	snake.snake_coords = []
	snake.snake_coord = []
	snake.body_part = 3
	snake.snake_coord = [WIDTH//snake.side//2, HEIGHT//snake.side//2]
	snake.point = 0
	snake.create_food()

	for i in range(snake.body_part):
		snake.snake_coords.append(tuple(snake.snake_coord))
		pygame.draw.rect(snake.screen, WHITE, (snake.side*snake.snake_coord[0], snake.side*snake.snake_coord[1], snake.side-1, snake.side-1))
		snake.move("left")

def main():
	pygame.init()
	global WIDTH
	global HEIGHT
	global WHITE
	global BLACK

	WHITE = (255,255,255)
	BLACK = (0,0,0)
	WIDTH = 1280
	HEIGHT = 800
	side = 60
	running = True
	pause = False
	direction = "left"

	screen = pygame.display.set_mode((WIDTH,HEIGHT), flags=pygame.SHOWN)
	snake = Snake(side, screen)
	clock = pygame.time.Clock()
	
	font_point = pygame.font.SysFont('arial', side)
	font2 = pygame.font.SysFont('arial', 100)

	start(snake)
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if keyboard.is_pressed("p"):
			if pause == False:
				pause = True
			elif pause == True:
				pause = False

		if pause == False:
			if keyboard.is_pressed('left') and direction != "right":
				direction = "left"
			elif keyboard.is_pressed('right') and direction != "left":
				direction = "right"
			elif keyboard.is_pressed('up') and direction != "down":
				direction = "up"
			elif keyboard.is_pressed('down') and direction != "up":
				direction = "down"

		if keyboard.is_pressed("r"):
			direction = "left"
			start(snake)
		
		if pause == True:
			pass
		elif snake.game_over():
			die = font2.render('Game over', True, WHITE)
			die_rect = die.get_rect(center=(WIDTH/2/2, HEIGHT/2))
			pygame.draw.rect(screen, BLACK, die_rect)
			pygame.draw.rect(screen, WHITE, die_rect, 2)

			restart = font2.render('Restart(r)', True, WHITE)
			restart_rect = restart.get_rect(center=(WIDTH/2 + WIDTH/2/2, HEIGHT/2))
			pygame.draw.rect(screen, BLACK, restart_rect)
			pygame.draw.rect(screen, WHITE, restart_rect, 2)

			screen.blit(restart, restart_rect)
			screen.blit(die, die_rect)
		else:
			snake.run(direction)

		show_point = font_point.render('POINTS: ' + str(snake.point), True, WHITE)
		pygame.draw.rect(screen,BLACK, (WIDTH-show_point.get_rect()[2],0,show_point.get_rect()[2],show_point.get_rect()[3]))
		screen.blit(show_point, (WIDTH-show_point.get_rect()[2],0))

		clock.tick(10)
		pygame.display.flip()
main()