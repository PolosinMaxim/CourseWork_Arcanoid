# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import sys

BLACK = (0, 0, 0) # Цвета (R, G, B)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
lightRED = (255, 128, 128)
GREEN = (0, 255, 0)
darkGREEN = (0, 190, 0)
BLUE = (0, 0, 255)
lightBLUE = (128, 128, 255)
back_image_filename = '01.jpg'
Screen_Sizes = [(800, 600), (1280, 720), (1366, 768), (1440, 900)]
Size_ID = 1
WIDTH, HEIGHT = Screen_Sizes[Size_ID] #стартовый размер игрового окна
FPS = 60 # частота кадров в секунду
brick_width =  WIDTH // 15 - 2 #16 штук
brick_height =  HEIGHT // 20 - 2
brick_field_start = HEIGHT // 6
brick_border = 2
min_bita_width = brick_width // 2 #25
max_bita_width = brick_width * 4

class Game():
    background_image = pygame.image.load(back_image_filename)
    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
    paused = False
    game_over = False
    need_input = True
    scores = 0
    lives = 3
    screennotchanged = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Parkanoid")
        self.objects = []
        self.bita = None
        self.create_bita()
        self.level = 0
        self.surprises = []
        self.ball = None
        self.newlevel()
        self.create_labels()
    def ChangeScreenSize(self):
        global WIDTH, HEIGHT, brick_width, brick_height, brick_field_start, min_bita_width, max_bita_width, Size_ID, Screen_Sizes
        Size_ID = (Size_ID + 1) % len(Screen_Sizes)
        WIDTH, HEIGHT = Screen_Sizes[Size_ID]
        brick_width =  WIDTH // 15 - 2 #16 штук
        brick_height =  HEIGHT // 20 - 2
        brick_field_start = HEIGHT // 6
        min_bita_width = brick_width // 2 #25
        max_bita_width = brick_width * 4
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_image = pygame.transform.scale(self.background_image,(WIDTH, HEIGHT))
        self.objects = []
        self.bita = None
        self.create_bita()
        self.level = 0
        self.surprises = []
        self.ball = None
        self.newlevel()
        self.create_labels()
        self.bita.resize()
        self.ball.resize()
        self.lives = 3
    def newlevel(self):
        self.bricks = []
        for surp in self.surprises: self.objects.remove(surp)
        self.surprises.clear()
        self.create_bricks()
        if self.ball: self.objects.remove(self.ball)
        self.create_ball()
        self.level += 1
    def create_bita(self):
        self.bita = Bita()
        self.objects.append(self.bita)
    def create_ball(self):
        self.ball = Ball()
        self.ball.ball_x = self.bita.bita_x + self.bita.bita_width / 2
        self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
        self.objects.append(self.ball)
    def create_bricks(self):
        for i in range(15):
            for j in range(8):
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
                                      brick_height)
        self.objects.append(self.score_label)
        self.lives_label = TextObject(WIDTH * 7 // 8,
                                      5,
                                      lambda: f'LIVES: {self.lives}',
                                      GREEN,
                                      'Arial',
                                      brick_height)
        self.objects.append(self.lives_label)
        self.level_label = TextObject((WIDTH - brick_width) // 2,
                                      5,
                                      lambda: f'LEVEL: {self.level}',
                                      GREEN,
                                      'Arial',
                                      brick_height)
        self.objects.append(self.level_label)
        self.tutorial_label1 = TextObject(WIDTH // 2 - int(brick_width * 4),
                                      HEIGHT * 11 // 18,
                                      lambda: f'Move paddle with LEFT & RIGHT, press SPACE to begin',
                                      GREEN,
                                      'Arial',
                                      brick_height)
        self.tutorial_label2 = TextObject(WIDTH // 2 - int(brick_width * 2.5),
                                      HEIGHT * 2 // 3,
                                      lambda: f'For now, press UP to change screen size',
                                      GREEN,
                                      'Arial',
                                      brick_height)
        if self.screennotchanged:
            self.objects.append(self.tutorial_label1)
            self.objects.append(self.tutorial_label2)
        elif self.tutorial_label1 in self.objects and self.tutorial_label2 in self.objects:
            self.objects.remove(self.tutorial_label1)
            self.objects.remove(self.tutorial_label2)
        self.pause_label = TextObject(WIDTH // 2 - int(brick_width * 2.5),
                                      HEIGHT * 23 // 36,
                                      lambda: f'PAUSED, press SPACE to continue',
                                      GREEN,
                                      'Arial',
                                      brick_height)
    def update(self):
        if self.game_over:
            self.gameover_label = TextObject(WIDTH // 2 - brick_width,
                                      brick_height * 2,
                                      lambda: f'GAME OVER',
                                      GREEN,
                                      'Arial',
                                      brick_height)
            self.objects.append(self.gameover_label)
            if self.need_input:
                self.need_input = False
                player_list = [i.split(chr(9)) for i in open("BestRecords.txt", "r")]
                if len(player_list) < 3 or self.scores > int(player_list[2][-1][:-1]):
                    open("BestRecords.txt", "a").write(input("Ваше имя? ")[:12] + chr(9) + str(self.scores) + chr(10))
                    player_list = [i.split(chr(9)) for i in open("BestRecords.txt", "r")]
                    for i in range(len(player_list) - 1):
                        for j in range(i + 1, len(player_list)):
                            if int(player_list[j][-1][:-1]) > int(player_list[i][-1][:-1]):
                                c = player_list[j]
                                player_list[j] = player_list[i]
                                player_list[i] = c
                    newfile = open("BestRecords.txt", "w")
                    for i in player_list: newfile.write(chr(9).join(i))
                print(player_list)
                self.firstbest_label = TextObject(WIDTH // 2 - brick_width,
                                      HEIGHT * 3 // 5,
                                      lambda: player_list[0][0] + "   " + player_list[0][1][:-1],
                                      GREEN,
                                      'Arial',
                                      brick_height)
                self.objects.append(self.firstbest_label)
                if len(player_list) >= 2:
                    self.secondbest_label = TextObject(WIDTH // 2 - brick_width,
                                      HEIGHT * 7 // 10,
                                      lambda: player_list[1][0] + "   " + player_list[1][1][:-1],
                                      GREEN,
                                      'Arial',
                                      brick_height)
                    self.objects.append(self.secondbest_label)
                if len(player_list) >= 3:
                    self.thirdbest_label = TextObject(WIDTH // 2 - brick_width,
                                      HEIGHT * 4 // 5,
                                      lambda: player_list[2][0] + "   " + player_list[2][1][:-1],
                                      GREEN,
                                      'Arial',
                                      brick_height)
                    self.objects.append(self.thirdbest_label)
        else:
            for ob in self.objects:
                ob.update()
            self.check_borders()
            self.check_bricks()
            self.check_surprises()
            if self.ball.attached:
                self.ball.ball_x = self.bita.bita_x + self.bita.bita_width / 2
                self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
    def draw(self):
        for ob in self.objects:
            ob.draw(self.screen)
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: self.bita.toleft = True
                elif event.key == pygame.K_RIGHT: self.bita.toright = True
                elif event.key == pygame.K_UP and self.ball.attached and self.screennotchanged:
                    self.ChangeScreenSize()
                elif event.key == pygame.K_SPACE:
                    self.ball.attached = False
                    self.screennotchanged = False
                    if self.paused:
                        self.paused = False
                        self.objects.remove(self.pause_label)
                elif event.key == pygame.K_ESCAPE:
                    if not self.paused:
                        self.paused = True
                        self.objects.append(self.pause_label)
            elif event.type == pygame.KEYUP:
                self.bita.toleft = False
                self.bita.toright = False
    def run(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.events()
            if not self.paused: self.update()
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
            else:
                self.ball.y_speed *= -1
                self.ball.ball_y = self.bita.bita_y - self.ball.ball_radius
                if self.bita.toright: self.ball.x_speed += 0.5
                elif self.bita.toleft: self.ball.x_speed -= 0.5
        if self.ball.ball_y > HEIGHT - self.ball.ball_radius:
            lost = True
        if lost:
            self.lives -= 1
            self.bita.reset()
            if self.lives < 1: self.game_over = True
            else:
                self.objects.remove(self.ball)
                for surp in self.surprises: self.objects.remove(surp)
                self.surprises = []
                self.create_ball()
    def check_bricks(self):
        for brick in self.bricks:
            result = False
            if abs(brick.x - self.ball.ball_x) > brick_width * 2: continue
            if abs(brick.y - self.ball.ball_y) > brick_height * 2: continue
            coll_vert = self.ball.ball_x + self.ball.ball_radius >= brick.x and self.ball.ball_x - self.ball.ball_radius <= brick.x + brick_width
            coll_horz = self.ball.ball_y + self.ball.ball_radius >= brick.y and self.ball.ball_y - self.ball.ball_radius <= brick.y + brick_height
            brad = self.ball.ball_radius + abs(self.ball.x_speed)
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
                self.scores += 1
                if brick.tipe == 0:
                    self.objects.remove(brick)
                    self.bricks.remove(brick)
                    self.create_surprise(self.ball.ball_x, self.ball.ball_y)
                else: brick.tipe -= 1
                if len(self.bricks) ==0: self.newlevel()
    def check_surprises(self):
        for surp in self.surprises:
            if surp.y >= self.bita.bita_y and surp.y < self.bita.bita_y + self.bita.bita_height and surp.x <= self.bita.bita_x + self.bita.bita_width and surp.x + surp.surp_width >= self.bita.bita_x: #surp.x >= self.bita.bita_x and surp.x =< self.bita.bita_x + self.bita.bita_width:
                if surp.tipe == 0: #доп. жизнь
                    self.lives += 1
                elif surp.tipe == 1: #расширяет биту
                    self.bita.bita_width += brick_width // 2
                    self.bita.bita_width = min(self.bita.bita_width, max_bita_width)
                    if self.bita.bita_width != max_bita_width: self.bita.bita_x -= brick_width // 4
                    if self.bita.bita_x > WIDTH - self.bita.bita_width: self.bita.bita_x = WIDTH - self.bita.bita_width - 1 #доп. проверка на случай, если вылезает за границы
                    elif self.bita.bita_x < 0: self.bita.bita_x = 1
                elif surp.tipe == 2: #сужает биту
                    self.bita.bita_width -= brick_width // 2
                    self.bita.bita_width = max(self.bita.bita_width, min_bita_width)
                    if self.bita.bita_width != min_bita_width: self.bita.bita_x += brick_width // 4
                self.objects.remove(surp)
                self.surprises.remove(surp)
            elif surp.y > (HEIGHT + self.bita.bita_y) // 2:
                self.objects.remove(surp)
                self.surprises.remove(surp)

class Ball():
    ball_radius = brick_width // 5
    color = RED
    attached = True # Если True, то прикреплён к бите
    def __init__(self):
        ball_x = None   # Координаты центра мяча
        ball_y = None
        self.x_speed = self.ball_radius / 5   # Текущая скорость по x
        self.y_speed = self.ball_radius / -5  # Текущая скорость по y
    def resize(self):
        self.ball_radius = brick_width // 5
        self.x_speed = self.ball_radius / 5   # Текущая скорость по x
        self.y_speed = self.ball_radius / -5  # Текущая скорость по y
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.ball_x, self.ball_y), self.ball_radius)
    def update(self):
        if self.attached:
            pass
        else:
            self.ball_x += self.x_speed
            self.ball_y += self.y_speed

class Bita():
    bita_y = HEIGHT - 100
    bita_height = brick_height
    speed = brick_height // 4
    def __init__(self):
        self.bita_x = WIDTH // 2 - brick_width
        self.toleft = False
        self.toright = False
        self.bita_width = brick_width * 2
    def resize(self):
        self.bita_y = HEIGHT - 100
        self.bita_height = brick_height
        self.bita_x = WIDTH // 2 - brick_width
        self.bita_width = brick_width * 2
    def reset(self):
        self.bita_x = WIDTH // 2 - brick_width
        self.toleft = False
        self.toright = False
        self.bita_width = brick_width * 2
    def update(self):
        if self.toleft:
            if self.bita_x > 0:
                self.bita_x -= self.speed
        if self.toright:
            if self.bita_x < WIDTH - self.bita_width:
                self.bita_x += self.speed
    def draw(self,screen):
        pygame.draw.rect(screen, BLUE, (self.bita_x, self.bita_y, self.bita_width, self.bita_height))

class Brick():
    def __init__(self):
        self.tipe = 0
        rr = random.randrange(10)
        if rr<2: self.tipe = 2
        elif rr<5: self.tipe = 1
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
            self.surp_width = brick_height // 4
            pygame.draw.circle(screen, lightRED, (self.x, self.y), self.surp_width) #доп. жизнь
        elif self.tipe == 1:
            self.surp_width = brick_width
            pygame.draw.rect(screen, lightBLUE, (self.x, self.y, self.surp_width, 5)) #расширяет биту
        elif self.tipe == 2:
            self.surp_width = brick_width // 4
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.surp_width, 5)) #сужает биту
    def update(self):
        self.y += brick_height // 30 + 1

class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size): #, NameEnter = False):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())
    def draw(self, surface, centralized = False):
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
        #if NameEnter: continue
        pass

'''class NameEnter(TextObject):
    def __init__(self, x, y, text_func, color, font_name, font_size):
        super().__init__(x, y, text_func, color, font_name, font_size)
    def update(self):
        pass'''

if __name__ == '__main__':
    Game().run()

#Sources:
#https://habr.com/ru/articles/588605/
#https://younglinux.info/pygame/draw
#https://riptutorial.com/pygame/example/18046/event-loop
#https://cpp-python-nsu.inp.nsk.su/textbook/sec5/ch1
#https://ru.stackoverflow.com/questions/1357843/%D0%9A%D0%B0%D0%BA-%D1%81%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C-%D1%87%D1%82%D0%BE%D0%B1%D1%8B-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE%D0%B4%D1%81%D1%82%D1%80%D0%B0%D0%B8%D0%B2%D0%B0%D0%BB%D0%BE%D1%81%D1%8C-%D0%BF%D0%BE%D0%B4-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0
#https://code-basics.com/ru/languages/python/lessons/default-parameters
#https://www.youtube.com/watch?v=Xyfd2QBuPdo
#https://dzen.ru/a/Y4Swlyu-kDD5k5rS