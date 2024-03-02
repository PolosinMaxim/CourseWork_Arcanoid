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

# Цикл игры
running = True
bita_x = 300
while running:
    # Рендеринг
    # держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    pygame.draw.rect(screen, BLACK, (bita_x, HEIGHT - 100, brick_width * 2, brick_height)) #бита
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
    pygame.draw.rect(screen, BLUE, (bita_x, HEIGHT - 100, brick_width * 2, brick_height)) #бита
    pygame.display.flip()

#Sources:
#https://habr.com/ru/articles/588605/
#https://younglinux.info/pygame/draw
#https://riptutorial.com/pygame/example/18046/event-loop