import settings
import map
from settings import *
import pygame
import options
import logger
import UI

pygame.font.init()

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


def go_to_menu():
    change_scene("menu")


def go_to_next_level(scr):
    settings.next_level()
    logger.log("next lvl")
    return restart_game(scr)


def scenes(scr, plr, world_map, enemies, entities, boosts_group, clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    SCENE = get_scene()
    show_FPS = get_FPS_show()

    if SCENE == "menu":
        scr.blit(background, (0, 0))
        scr.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button_text, button_rect in button_rects:
            if button_rect.collidepoint(mouse_pos):
                color = HOVER_COLOR
            else:
                color = BUTTON_COLOR
            pygame.draw.rect(scr, color, button_rect)
            scr.blit(button_text, button_text.get_rect(center=button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rects[0][1].collidepoint(mouse_pos):
                    logger.log("Гравець нажав Play")
                    change_scene("main")
                    return restart_game(scr)
                elif button_rects[1][1].collidepoint(mouse_pos):
                    logger.log("Гравець нажав Level designer")
                elif button_rects[2][1].collidepoint(mouse_pos):
                    logger.log("Гравець нажав Options")
                    options.show_options_menu(scr, WIDTH, HEIGHT)
                elif button_rects[3][1].collidepoint(mouse_pos):
                    logger.log("Гравець нажав Quit Game")
                    return False

        pygame.display.flip()
        clock.tick(FPS)

    if SCENE == "main":
        if world_map is None or plr is None or enemies is None or entities is None or boosts_group is None:
            world_map, plr, enemies, entities, boosts_group = restart_game(scr)
        
        scr.fill(BACKGROUND)

        for wall in world_map:
            scr.blit(wall.img, wall.rect)

        for boost in boosts_group:
            boost.update(plr, scr)

        if plr.render:
            plr.update(scr, world_map)
            plr.draw(scr)

        for enemy in enemies:
            enemy.update(scr, plr)

        if len(enemies) == 0:
            change_scene("win")

        for bullet in plr.bullets:
            bullet.update(world_map, entities)
            bullet.draw(scr)

        if show_FPS:
            scr.blit(button_font.render(f"{int(clock.get_fps())}", False, WHITE, BLACK), (WIDTH*0.9, 10))

        damage_ui.scr_update(scr)

        pygame.display.flip()
        clock.tick(FPS)

    if SCENE == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        scr.fill(GREEN)
        text = title_font.render("Ти виграв", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        scr.blit(text, text_rect)

        UI.create_button(scr, "В меню", 150, 400, 200, 100, BLACK, BLACK, go_to_menu)
        UI.create_button(scr, "Далі", 450, 400, 200, 100, BLACK, BLACK, lambda: go_to_next_level(scr))

        pygame.display.flip()
        clock.tick(FPS)

        # Перевіряємо, чи була натиснута кнопка "Далі"
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(450, 400, 200, 100).collidepoint(mouse_pos):
                return go_to_next_level(scr)

    if SCENE == 'death':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        scr.fill(RED)
        text = title_font.render("Ти програв", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        scr.blit(text, text_rect)

        UI.create_button(scr, "В меню", 150, 400, 200, 100, BLACK, BLACK, go_to_menu)
        UI.create_button(scr, "Заново", 450, 400, 200, 100, BLACK, BLACK, lambda: restart_game(scr))

        pygame.display.flip()
        clock.tick(FPS)

        # Перевіряємо, чи була натиснута кнопка "Заново"
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect(450, 400, 200, 100).collidepoint(mouse_pos):
                return restart_game(scr)
        
        
def restart_game(scr):
    # Генеруємо нову карту та об'єкти
    world_map = map.generate_map()
    plr = map.generate_player()
    enemies = map.generate_enemy(plr, world_map)
    
    # Оновлюємо групу entities
    entities = pygame.sprite.Group()
    entities.add(plr)
    entities.add(enemies)

    # Генеруємо нові бустери
    boosts_group = map.generate_boosts()

    # Змінюємо сцену на "main"
    change_scene("main")

    logger.log('restart game')

    # Повертаємо нові об'єкти
    return world_map, plr, enemies, entities, boosts_group

    