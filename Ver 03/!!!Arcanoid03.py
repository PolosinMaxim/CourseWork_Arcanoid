# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import sys

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
lightBLUE = (128, 128, 255)
back_image_filename = '01.jpg'
WIDTH = 800  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 30 # частота кадров в секунду
brick_width =  50 #WIDTH // 15 - 2 - 16 штук
brick_height =  28 #HEIGHT // 20 - 2
brick_field_start = 100
brick_field_end = 400
brick_border = 2


class Game():
    background_image = pygame.image.load(back_image_filename)
    running = True
    game_over = False
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    def __init__(self):
# создаем игру и окно
        pygame.init()
#pygame.mixer.init()  # для звука
        pygame.display.set_caption("Parkanoid")
        self.bita = None
        self.objects = []
        self.ball = None
        self.bricks = []
        self.create_bita()
        self.create_bricks()
        self.create_ball()
    def create_bita(self):
        self.bita = Bita()
        self.objects.append(self.bita)
    def create_ball(self):
        self.ball = Ball()
        self.ball.ball_x = self.bita.bita_x + self.bita.bita_width / 2
        self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
        self.objects.append(self.ball)
    def create_bricks(self):
        for i in range(15): #собственно кирпичи
            for j in range(10):
                #if random.randrange(10) > 2: continue
                brick = Brick()
                brick.x = i * (brick_width + brick_border)
                brick.y = brick_field_start + j * (brick_height + brick_border)
                self.objects.append(brick)
                self.bricks.append(brick)
    def update(self):
        for ob in self.objects:
            ob.update()
        self.check_borders()
        self.check_bricks()
    def draw(self):
        for ob in self.objects:
            ob.draw(self.screen)
    def events(self):
        for event in pygame.event.get(): #можно было бы сделать match case, но более старые версии это не поддерживают
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #self.bita.bita_x -= 10
                    self.bita.toleft = True
                elif event.key == pygame.K_RIGHT:
                    #self.bita.bita_x += 10
                    self.bita.toright = True
                elif event.key == pygame.K_SPACE:
                    self.ball.attached = False
            elif event.type == pygame.KEYUP:
                self.bita.toleft = False
                self.bita.toright = False
    def run(self):
        while not self.game_over:
            self.screen.blit(self.background_image, (0, 0))
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
    def check_borders(self):
        if self.ball.ball_x > WIDTH - self.ball.ball_radius or self.ball.ball_x < self.ball.ball_radius:
            self.ball.x_speed *= -1
        if self.ball.ball_y < self.ball.ball_radius:
            self.ball.y_speed *= -1
        if self.ball.ball_y > self.bita.bita_y - self.ball.ball_radius and self.ball.ball_x in range(self.bita.bita_x, self.bita.bita_x + self.bita.bita_width):
            self.ball.y_speed *= -1
            self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
            if self.bita.toright: self.ball.x_speed += 1
            elif self.bita.toleft: self.ball.x_speed -= 1
        if self.ball.ball_y > HEIGHT - self.ball.ball_radius:
            self.create_ball()
    def check_bricks(self):
        #bx = self.ball.ball_x #+ self.ball.true_rad
        #by = self.ball.ball_y #+ self.ball.true_rad
        for brick in self.bricks:
            result = False
            coll_vert = self.ball.ball_x + self.ball.ball_radius >= brick.x and self.ball.ball_x - self.ball.ball_radius <= brick.x + brick_width
            coll_horz = self.ball.ball_y + self.ball.ball_radius >= brick.y and self.ball.ball_y - self.ball.ball_radius <= brick.y + brick_height
            brad = self.ball.ball_radius + abs(self.ball.x_speed)
            #при верт. коллизии bx не так важен, убрали в отдельную переменную
            #так же и с by при коллизии
            if self.ball.y_speed > 0 and coll_vert and self.ball.ball_y + brad > brick.y and self.ball.ball_y + brad < brick.y + brick_height:
                delta = self.ball.ball_y + self.ball.ball_radius - brick.y
                if delta > 0: self.ball.ball_y -= delta
                self.ball.y_speed *= -1 #top
                result = True
            elif self.ball.y_speed < 0 and coll_vert and self.ball.ball_y - brad > brick.y and self.ball.ball_y - brad < brick.y + brick_height:
                delta = brick.y + brick_height - self.ball.ball_y - self.ball.ball_radius
                if delta > 0: self.ball.ball_y += delta
                self.ball.y_speed *= -1 #bottom
                result = True
            elif self.ball.x_speed > 0 and coll_horz and self.ball.ball_x + brad > brick.x and self.ball.ball_x + brad < brick.x + brick_width:
                delta = self.ball.ball_x + self.ball.ball_radius - brick.x
                if delta > 0: self.ball.ball_x -= delta
                self.ball.x_speed *= -1 #left
                result = True
            elif self.ball.x_speed < 0 and coll_horz and self.ball.ball_x - brad > brick.x and self.ball.ball_x - brad < brick.x + brick_width:
                delta = brick.x + brick_width - self.ball.ball_x - self.ball.ball_radius
                if delta > 0: self.ball.ball_x += delta
                self.ball.x_speed *= -1 #right
                result = True
            if result:
                if brick.tipe == 0:
                    self.objects.remove(brick)
                    self.bricks.remove(brick)
                else: brick.tipe -= 1
            #проверяем результат
            #if result == 'top' or result == 'bottom': self.ball.y_speed *= -1
            #if result == 'left' or result == 'right': self.ball.x_speed *= -1

class Ball():
    ball_radius = 10
    color = RED
    attached = True # Если True, то прикреплён к бите
    #true_rad = ball_radius #// 2
    def __init__(self):
        ball_x = None   # Координаты центра мяча
        ball_y = None
        self.x_speed = 4  # Текущая скорость по x
        self.y_speed = -4  # Текущая скорость по y
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.ball_x, self.ball_y), self.ball_radius)
    def update(self):
        #self.move()
    #def move(self):
        if self.attached:
            pass
            #self.ball_x = bita_x + bita_width / 2
            #self.ball_y = bita_y - ball.ball_radius
        else:
            self.ball_x += self.x_speed
            self.ball_y += self.y_speed

class Bita():
    bita_y = HEIGHT - 100
    bita_height = brick_height
    bita_width = brick_width * 2
    def __init__(self):
        self.bita_x = 300
        self.toleft = False
        self.toright = False
        self.speed = 12
    def update(self):
        if self.toleft:
            #other actions?
            if self.bita_x > 0:
                self.bita_x -= self.speed
        if self.toright:
            #other actions?
            if self.bita_x < WIDTH - self.bita_width:
                self.bita_x += self.speed
    def draw(self,screen):
        pygame.draw.rect(screen, BLUE, (self.bita_x, self.bita_y, self.bita_width, self.bita_height))

class Brick():
    def __init__(self):
        self.tipe = random.randrange(3)
        #self.color = [RED, BLUE, WHITE][self.tipe]
        self.x = None
        self.y = None
    def update(self):
        pass
    def draw(self,screen):
        pygame.draw.rect(screen, [WHITE, lightBLUE, RED][self.tipe], (self.x, self.y, brick_width, brick_height))


#def main():
    #Game().run()

if __name__ == '__main__':
    Game().run()
    #main()

#Sources:
#https://habr.com/ru/articles/588605/
#https://younglinux.info/pygame/draw
#https://riptutorial.com/pygame/example/18046/event-loop
#https://cpp-python-nsu.inp.nsk.su/textbook/sec5/ch1