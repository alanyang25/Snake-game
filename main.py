import pygame
from pygame.locals import *
import time
import random

SIZE = 24 # size of each block
WINDOW_SIZE = (600, 600)
BACKGROUND_COLOR = (73, 235, 52)

#=====================================================================
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*5
        self.y = SIZE*5

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * 24
        self.y = random.randint(0, 24) * 24

#=====================================================================
class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/stop-button.png").convert()
        self.x = [SIZE*10]*self.length
        self.y = [SIZE*10]*self.length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(-1) # append a number
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR) # Clear the screen before drawing / RGB color picker
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
            self.draw()
        if self.direction == 'down':
            self.y[0] += SIZE
            self.draw()
        if self.direction == 'right':
            self.x[0] += SIZE
            self.draw()
        if self.direction == 'left':
            self.x[0] -= SIZE
            self.draw()

#=====================================================================
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.surface.fill(BACKGROUND_COLOR) # RGB color picker
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.sleep_time = 0.2

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x2 + SIZE > x1:
            if y1 >= y2 and y2 + SIZE > y1:
                return True

        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("car-lock-sound-effect")
            self.apple.move()
            self.snake.increase_length()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("punch-sound")
                raise "Game over: Hit itself"

        # snake colliding with the boundaries of the window
        if not(0 <= self.snake.x[0] < WINDOW_SIZE[0] and 0 <= self.snake.y[0] < WINDOW_SIZE[1]):
            self.play_sound("punch-sound")
            raise "Game over: Hit the boundary."

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('SF Pro', 34)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}.", True, (255, 255, 255))
        self.surface.blit(line1, (60, 200))
        line2 = font.render(f"To play again press Enter. To exit press Esc.", True, (255, 255, 255))
        self.surface.blit(line2, (60, 260))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('SF Pro', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255)) # score in white color
        self.surface.blit(score, (490, 24))

    def game_reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def sleep(self):
        if self.snake.length < 10:
            self.sleep_time = 0.2
        elif self.snake.length >= 10:
            self.sleep_time = 0.175
            if self.snake.length >= 20:
                self.sleep_time = 0.15
                if self.snake.length >= 30:
                    self.sleep_time = 0.125
                    if self.snake.length >= 40:
                        self.sleep_time = 0.1

        time.sleep(self.sleep_time)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.game_reset()

            self.sleep()

#=====================================================================
if __name__ == "__main__":
    game = Game()
    game.run()
