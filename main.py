from funcs import *
import pygame
import sys
from database import get_best, cur, bd

GAMERS_SQL = get_best()


def draw_top():
    font_top = pygame.font.SysFont('simsun', 30)
    font_game = pygame.font.SysFont('simsun', 24)
    text_head = font_top.render('Best tries: ', True, COLOR_TEXT)
    screen.blit(text_head, (250, 0))
    for index, game in enumerate(GAMERS_SQL):
        name, record = game
        s = f'{index + 1}. {name} - {record}'
        text_game = font_game.render(s, True, COLOR_TEXT)
        screen.blit(text_game, (250, 25 + 20 * index))


def draw_ui(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('simsun', 48)
    font_delta = pygame.font.SysFont('simsun', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    if delta > 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (165, 75))
    print(mas)
    for row in range(BLOCKS):
        for col in range(BLOCKS):
            value = mas[row][col]
            text = font.render(f'{value}', True, BlACK)
            w = col * SIZE_BLOCK + (col + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 235, 0),
    256: (255, 235, 0),
    512: (255, 235, 0),
    1024: (255, 235, 0),
    2048: (255, 235, 0),
}
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BlACK = (0, 0, 0)
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


def init_const():
    global score, mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    empty = get_empty(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index(random_num1)
    mas = insert24(mas, x1, y1)
    x2, y2 = get_index(random_num2)
    mas = insert24(mas, x2, y2)
    score = 0


mas = None
score = None
init_const()
USERNAME = None

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')


def draw_intro():
    img_2048 = pygame.image.load('2048.jpg')
    font = pygame.font.SysFont('stxingkai', 70)
    text_welcome = font.render('Welcome', True, WHITE)
    name = 'Enter your name '
    find_name = False

    while not find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Enter your name ':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        find_name = True
                        break

        screen.fill(BlACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img_2048, (200, 200)), (10, 10))
        screen.blit(text_welcome, (230, 60))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BlACK)


def draw_game_over():
    global USERNAME, GAMERS_SQL
    img_2048 = pygame.image.load('2048.jpg')
    font = pygame.font.SysFont('stxingkai', 60)
    text_game_over = font.render('Game Over', True, WHITE)
    text_score = font.render(f'You are typed: {score}', True, WHITE)
    try:
        best_score = GAMERS_SQL[0][1]
    except IndexError:
        best_score = 0

    if score > best_score:
        text = 'Record broken'
    else:
        text = f'Record: {best_score}'
    cur.execute(f'''INSERT INTO records VALUES ('{USERNAME}', {score})''')
    bd.commit()
    text_record = font.render(text, True, WHITE)
    GAMERS_SQL = get_best()
    make_decision = False

    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_decision = True
                    init_const()

        screen.fill(BlACK)
        screen.blit(text_game_over, (230, 80))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        screen.blit(pygame.transform.scale(img_2048, (200, 200)), (10, 10))
        pygame.display.update()
    screen.fill(BlACK)


draw_intro()
draw_ui(score)
draw_top()
pygame.display.update()


def game_loop():
    global score, mas
    mas_move = False
    while zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, mas_move = move_down(mas)
                score += delta
                if zero_in_mas(mas) and mas_move:
                    empty = get_empty(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index(random_num)
                    mas = insert24(mas, x, y)
                    mas_move = False
                draw_ui(score, delta)
                draw_top()
                pygame.display.update()


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
