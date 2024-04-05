# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import sys

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
lightRED = (255, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
lightBLUE = (128, 128, 255)
back_image_filename = '01.jpg'
WIDTH = 800  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 60 # частота кадров в секунду
brick_width =  50 #WIDTH // 15 - 2 - 16 штук
brick_width2 = brick_width * 2
brick_height =  28 #HEIGHT // 20 - 2
brick_height2 = brick_height * 2
brick_field_start = 100
brick_field_end = 400
brick_border = 2
min_bita_width = 25
max_bita_width = 200


class Game():
    background_image = pygame.image.load(back_image_filename)
    running = True
    game_over = False
    scores = 0
    lives = 3
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    def __init__(self):
# создаем игру и окно
        pygame.init()
#pygame.mixer.init()  # для звука
        pygame.display.set_caption("Parkanoid")
        self.objects = []
        self.bita = None
        self.create_bita()
        self.level = 0
        self.surprises = []
        self.ball = None
        self.newlevel()
        self.create_labels()
    def newlevel(self):
        self.bricks = []
        for surp in self.surprises: self.objects.remove(surp)
        self.surprises.clear()
        self.create_bricks()
        if self.ball: self.objects.remove(self.ball)

        self.create_ball()
        self.level+=1
    def create_bita(self):
        self.bita = Bita()
        self.objects.append(self.bita)
    def create_ball(self):
        self.ball = Ball()
        self.ball.ball_x = self.bita.bita_x + self.bita.bita_width / 2
        self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
        self.objects.append(self.ball)
    def create_bricks(self):
        for i in range(15): #15): #собственно кирпичи
            for j in range(10): #10
                #if random.randrange(10) > 2: continue
                brick = Brick()
                brick.x = i * (brick_width + brick_border)
                brick.y = brick_field_start + j * (brick_height + brick_border)
                self.objects.append(brick)
                self.bricks.append(brick)
    def create_surprise(self, x, y):
        n = random.randrange(10)
        if n < 3:
            surp = Surprises()
            self.objects.append(surp)
            self.surprises.append(surp)
            surp.tipe = n
            surp.x = x
            surp.y = y
    def create_labels(self):
        self.score_label = TextObject(5,
                                      5,
                                      lambda: f'SCORE: {self.scores}',
                                      GREEN,
                                      'Arial',
                                      20)
        self.objects.append(self.score_label)
        self.lives_label = TextObject(WIDTH-100,
                                      5,
                                      lambda: f'LIVES: {self.lives}',
                                      GREEN,
                                      'Arial',
                                      20)
        self.objects.append(self.lives_label)
        self.level_label = TextObject(WIDTH//2,
                                      5,
                                      lambda: f'LEVEL: {self.level}',
                                      GREEN,
                                      'Arial',
                                      20)
        self.objects.append(self.level_label)
    def update(self):
        for ob in self.objects:
            ob.update()
        self.check_borders()
        self.check_bricks()
        self.check_surprises()
    def draw(self):
        for ob in self.objects:
            ob.draw(self.screen)
    def events(self):
        for event in pygame.event.get(): #можно было бы сделать match case, но более старые версии это не поддерживают
            #match event.type:
                #case pygame.QUIT:
                #case pygame.KEYDOWN:
                    #match event.key:
                #case pygame.KEYUP:
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
        lost = False
        if self.ball.ball_x > WIDTH - self.ball.ball_radius or self.ball.ball_x < self.ball.ball_radius:
            self.ball.x_speed *= -1
        if self.ball.ball_y < self.ball.ball_radius:
            self.ball.y_speed *= -1
        if self.ball.ball_y > self.bita.bita_y - self.ball.ball_radius and self.ball.ball_x >= self.bita.bita_x and self.ball.ball_x < self.bita.bita_x + self.bita.bita_width:
            if self.ball.ball_y - self.ball.ball_radius > self.bita.bita_y:
                lost = True
                #lives -= 1
            else:
                self.ball.y_speed *= -1
                self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
                if self.bita.toright: self.ball.x_speed += 0.5
                elif self.bita.toleft: self.ball.x_speed -= 0.5
        if self.ball.ball_y > HEIGHT - self.ball.ball_radius:
            lost = True
        if lost:
            self.lives -= 1
            print("Lives:", self.lives)
            self.bita.reset()
            if self.lives < 1: self.game_over = True
            else:
                self.objects.remove(self.ball)
                for surp in self.surprises: self.objects.remove(surp)
                self.surprises = []
                self.create_ball()
    def check_bricks(self):
        #bx = self.ball.ball_x #+ self.ball.true_rad
        #by = self.ball.ball_y #+ self.ball.true_rad
        for brick in self.bricks:
            result = False
            if abs(brick.x - self.ball.ball_x) > brick_width2: continue
            if abs(brick.y - self.ball.ball_y) > brick_height2: continue
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
                    self.scores += 1
                    print("Scores:", self.scores)
                    self.create_surprise(self.ball.ball_x, self.ball.ball_y)
                else: brick.tipe -= 1
                if len(self.bricks) ==0: self.newlevel()
            #проверяем результат
            #if result == 'top' or result == 'bottom': self.ball.y_speed *= -1
            #if result == 'left' or result == 'right': self.ball.x_speed *= -1
    def check_surprises(self):
        for surp in self.surprises:
            if surp.y >= self.bita.bita_y and surp.y < self.bita.bita_y + self.bita.bita_height and surp.x <= self.bita.bita_x + self.bita.bita_width and surp.x + surp.surp_width >= self.bita.bita_x: #surp.x >= self.bita.bita_x and surp.x =< self.bita.bita_x + self.bita.bita_width:
                if surp.tipe == 0: #доп. жизнь
                    self.lives += 1
                    print("Lives:", self.lives)
                elif surp.tipe == 1: #and self.bita.length_mode < 2: #расширяет биту
                    #self.bita.length_mode += 1
                    #print(["Короткая", "Обычная", "Длинная"][self.bita.length_mode])
                    self.bita.bita_width += brick_width // 2
                    self.bita.bita_width = min(self.bita.bita_width, max_bita_width)
                    if self.bita.bita_width != max_bita_width: self.bita.bita_x -= brick_width // 4
                    print("Ширина:", self.bita.bita_width)
                    if self.bita.bita_x > WIDTH - self.bita.bita_width: self.bita.bita_x = WIDTH - self.bita.bita_width - 1 #доп. проверка на случай, если вылезает за границы
                    elif self.bita.bita_x < 0: self.bita.bita_x = 1
                elif surp.tipe == 2: #and self.bita.length_mode > 0: #сужает биту
                    #self.bita.length_mode -= 1
                    #print(["Короткая", "Обычная", "Длинная"][self.bita.length_mode])
                    self.bita.bita_width -= brick_width // 2
                    self.bita.bita_width = max(self.bita.bita_width, min_bita_width)
                    if self.bita.bita_width != min_bita_width: self.bita.bita_x += brick_width // 4
                    print("Ширина:", self.bita.bita_width)
                self.objects.remove(surp)
                self.surprises.remove(surp)
            elif surp.y > (HEIGHT + self.bita.bita_y) // 2: #self.bita.bita_y + self.bita.bita_height:
                self.objects.remove(surp)
                self.surprises.remove(surp)

class Ball():
    ball_radius = 10
    color = RED
    attached = True # Если True, то прикреплён к бите
    #true_rad = ball_radius #// 2
    def __init__(self):
        ball_x = None   # Координаты центра мяча
        ball_y = None
        self.x_speed = 2.0  # Текущая скорость по x
        self.y_speed = -2.0  # Текущая скорость по y
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
    #length_mode = 1 #ширина биты в зависимости от сюрпризов:
    #0 - короткая, 1 - обычная, 2 - длинная
    speed = 6
    def __init__(self):
        self.bita_x = 300
        self.toleft = False
        self.toright = False
        self.bita_width = brick_width * 2
    def reset(self):
        self.bita_x = 300
        self.toleft = False
        self.toright = False
        self.bita_width = brick_width * 2
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
        self.tipe = 0 #random.randrange(3)
        rr = random.randrange(10)
        if rr<2: self.tipe = 2
        elif rr<5: self.tipe = 1
        #else: self.tipe = 0
        #self.color = [RED, BLUE, WHITE][self.tipe]
        self.x = None
        self.y = None
    def update(self):
        pass
    def draw(self,screen):
        pygame.draw.rect(screen, [WHITE, lightBLUE, RED][self.tipe], (self.x, self.y, brick_width, brick_height))

class Surprises():
    def __init__(self):
        self.x = None
        self.y = None
        self.tipe = 0
        self.surp_width = 0
    def draw(self, screen):
        if self.tipe == 0:
            self.surp_width = 7
            pygame.draw.circle(screen, lightRED, (self.x, self.y), self.surp_width) #доп. жизнь
        elif self.tipe == 1:
            self.surp_width = brick_width
            pygame.draw.rect(screen, lightBLUE, (self.x, self.y, self.surp_width, 5)) #расширяет биту
        elif self.tipe == 2:
            self.surp_width = brick_width // 4
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.surp_width, 5)) #сужает биту
    def update(self):
        self.y += 1
class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

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