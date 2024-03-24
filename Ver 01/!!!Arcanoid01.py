# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 800  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 30 # частота кадров в секунду
brick_width =  WIDTH // 15 - 2
brick_height =  HEIGHT // 20 - 2
brick_field_start = 100
brick_field_end = 400

# создаем игру и окно
pygame.init()
#pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen.fill(BLACK)
pygame.draw.rect(screen, (255, 255, 255), (1, 1, WIDTH - 2, HEIGHT - 2), 2) #граница окна
pygame.draw.rect(screen, GREEN, (0, brick_field_start, WIDTH - 2, brick_field_end - brick_field_start), 2) #граница поля крипичей
for i in range(15): #собственно кирпичи
    for j in range(10):
        pygame.draw.rect(screen, random.choice([RED, BLUE, WHITE]), (i * (brick_width + 2), brick_field_start + j * (brick_height + 2), brick_width, brick_height))

class Ball():
    ball_x = None   # Координаты центра мяча
    ball_y = None
    ball_radius = 10
    
    attached = True # Если True, то прикреплён к бите
        
    #ball_speed = 2  # Скорость мяча
    x_speed = 2  # Текущая скорость по x
    y_speed = 2  # Текущая скорость по y
    
    
 



# Цикл игры
running = True
bita_x = 300
bita_y = HEIGHT - 100
bita_height = brick_height
bita_width = brick_width * 2

ball = Ball()
ball.ball_x = bita_x + bita_width / 2
ball.ball_y = bita_y - ball.ball_radius



while running:
    # Рендеринг
    # держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    
    pygame.draw.rect(screen, BLACK, (bita_x, bita_y, bita_width, bita_height)) #бита
    pygame.draw.rect(screen, BLACK, (ball.ball_x, ball.ball_y, ball.ball_radius, ball.ball_radius)) 
    
    if ball.ball_x == WIDTH - ball.ball_radius or ball.ball_x == 0: ball.x_speed *= -1  # WDTH- не раб., 0 нет
    if ball.ball_y == HEIGHT - ball.ball_radius or ball.ball_y == 0: ball.y_speed *= -1 # HGHT- работает, 0 нет
    
    if Ball.attached:
        ball.ball_x = bita_x + bita_width / 2
        ball.ball_y = bita_y - ball.ball_radius
    else:
        ball.ball_x += ball.x_speed
        ball.ball_y -= ball.y_speed
    
    
    
    pygame.draw.rect(screen, WHITE,(ball.ball_x, ball.ball_y, ball.ball_radius, ball.ball_radius))
    # Обновление
    # Визуализация (сборка)
    for event in pygame.event.get():
        # check for closing window
        match event.type:
            case pygame.QUIT: running = False
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a: bita_x -= 10
                    case pygame.K_d: bita_x += 10
                    case pygame.K_SPACE: Ball.attached = False
    pygame.draw.rect(screen, BLUE, (bita_x, bita_y, bita_width, bita_height)) #бита
    
    pygame.display.flip()

#Sources:
#https://habr.com/ru/articles/588605/
#https://younglinux.info/pygame/draw
#https://riptutorial.com/pygame/example/18046/event-loop