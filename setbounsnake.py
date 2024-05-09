import pygame
import time
from random import randint
from pygame.locals import *

class Player:
    def __init__(self):
        self.x = 2
        self.y = 2 
        self.d = 0
        self.positions = []
        self.length = 4

class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0

class Game:
    def __init__(self):
        self.screenWidth = 40
        self.screenHeight = 20
        self.grid_size = 40
        self.snake_speed = 0.1
        self._running = True
        self.player = Player()
        self.apple = Apple()
        self.apple_count = 0
        self.new_apple()

    def isCollision(self, x1, y1, x2, y2, bsize):
        return x2 <= x1 < x2 + bsize and y2 <= y1 < y2 + bsize

    def new_apple(self):
        self.apple.x = randint(0, self.screenWidth - 1) * self.grid_size
        self.apple.y = randint(0, self.screenHeight - 1) * self.grid_size

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.screenWidth * self.grid_size, self.screenHeight * self.grid_size), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame example')
        self._snake_image = pygame.Surface((self.grid_size, self.grid_size))
        self._snake_image.fill((0, 255, 0))
        self._apple_image = pygame.Surface((self.grid_size, self.grid_size))
        self._apple_image.fill((255, 0, 0))

    def on_render(self):
        self._display_surf.fill((0,0,0))
        for pos in self.player.positions:
            self._display_surf.blit(self._snake_image, pos) 
        self._display_surf.blit(self._apple_image, (self.apple.x, self.apple.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    
            keys = pygame.key.get_pressed() 
            
            if keys[K_RIGHT] and self.player.x < self.screenWidth - 1:
                self.player.d = 0

            if keys[K_LEFT] and self.player.x > 0:
                self.player.d = 1

            if keys[K_UP] and self.player.y > 0:
                self.player.d = 2

            if keys[K_DOWN] and self.player.y < self.screenHeight - 1:
                self.player.d = 3

            if self.player.d == 0:
                self.player.x += 1
            elif self.player.d == 1:
                self.player.x -= 1
            elif self.player.d == 2:
                self.player.y -= 1
            elif self.player.d == 3:
                self.player.y += 1

            # Check if the snake's new position exceeds the boundaries
            if self.player.x < 0 or self.player.x >= self.screenWidth or self.player.y < 0 or self.player.y >= self.screenHeight:
                print('GAME OVER')
                exit()

            if len(self.player.positions) < self.player.length:
                self.player.positions.append((self.player.x * self.grid_size, self.player.y * self.grid_size))
            else:
                self.player.positions.pop(0)
                self.player.positions.append((self.player.x * self.grid_size, self.player.y * self.grid_size))

            if self.isCollision(self.player.x, self.player.y, self.apple.x // self.grid_size, self.apple.y // self.grid_size, 1):
                print('collides')
                self.new_apple()
                self.player.length += 1
                self.apple_count += 1
                if self.apple_count > 6:
                    self.snake_speed -= 0.01
                    if self.snake_speed < 0.03:
                        self.snake_speed = 0.03
                    print(f"Snake speed increased! New speed: {self.snake_speed}")
                    self.apple_count = 0

            if len(self.player.positions) > self.player.length-1:
                for i in range(0, self.player.length-1):                    
                    if self.isCollision(self.player.x, self.player.y, self.player.positions[i][0] // self.grid_size, self.player.positions[i][1] // self.grid_size, 1):
                        print('GAME OVER')
                        exit()                      
   
            self.on_render()
            time.sleep(self.snake_speed)
  
        self.on_cleanup()

if __name__ == "__main__":
    game = Game()
    game.on_execute()
