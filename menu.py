# menu.py
import pygame
import sys
import options  

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)
FONT_SIZE = 50
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro City")

# Загрузка и настройка фона
background = pygame.image.load('textures/menu.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Шрифты
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 40)

# Текст заголовка
title_text = title_font.render("Retro City", True, WHITE)
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 10))

# Кнопки
buttons = ["Play", "Level designer", "Options", "Quit Game"]
button_rects = []

for i, button in enumerate(buttons):
    button_text = button_font.render(button, True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
    button_rect.inflate_ip(BUTTON_WIDTH - button_rect.width, BUTTON_HEIGHT - button_rect.height)
    button_rects.append((button_text, button_rect))


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_rects[0][1].collidepoint(mouse_pos):
                print("Гравець нажав Play")
                # Здесь можно добавить код для перехода к игре
            elif button_rects[1][1].collidepoint(mouse_pos):
                print("Гравець нажав Level designer")
            elif button_rects[2][1].collidepoint(mouse_pos):
                print("Гравець нажав Options")
                options.show_options_menu(screen, WIDTH, HEIGHT)  
            elif button_rects[3][1].collidepoint(mouse_pos):
                print("Гравець нажав Quit Game")
                pygame.quit()
                sys.exit()

    screen.blit(background, (0, 0))
    screen.blit(title_text, title_rect)

    mouse_pos = pygame.mouse.get_pos()
    for button_text, button_rect in button_rects:
        if button_rect.collidepoint(mouse_pos):
            color = HOVER_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    pygame.display.flip()
    clock.tick(FPS)
