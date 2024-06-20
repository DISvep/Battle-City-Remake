# options.py
import pygame
import sys
import settings


def show_options_menu(screen, width, height):
    font = pygame.font.Font(None, 40)
    background_image = pygame.image.load('textures/menu.png')
    background_image = pygame.transform.scale(background_image, (width, height))
    volume = 0.5
    slider_rect = pygame.Rect(300, 200, 200, 20)
    slider_knob_rect = pygame.Rect(300 + int(volume * 200), 195, 10, 30)
    show_fps = False
    checkbox_image = pygame.transform.scale(pygame.image.load('textures/check_mark.png'), (20, 20)) # pygame.Rect(300, 300, 20, 20)
    checkbox_rect = checkbox_image.get_rect(x=300, y=300)
    
    def draw_slider():
        pygame.draw.rect(screen, (255, 255, 255), slider_rect)
        pygame.draw.rect(screen, (0, 255, 0), slider_knob_rect)

    def draw_checkbox():
        pygame.draw.rect(screen, (255, 255, 255), checkbox_rect, 2)
        if show_fps:
            screen.blit(checkbox_image, checkbox_rect)

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    running = True
    dragging_slider = False

    while running:
        screen.blit(background_image, (0, 0))

        draw_text("Options", font, (255, 255, 255), screen, 350, 50)

        draw_text("Volume", font, (255, 255, 255), screen, 150, 195)
        draw_slider()

        draw_text("Show FPS", font, (255, 255, 255), screen, 150, 295)
        draw_checkbox()

        draw_text("Back", font, (255, 255, 255), screen, 10, height - 50)  # Текст в левом нижнем углу
        back_text_rect = pygame.Rect(10, height - 50, 100, 50)  # Область текста "Назад"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_knob_rect.collidepoint(event.pos):
                    dragging_slider = True
                elif checkbox_rect.collidepoint(event.pos):
                    show_fps = not show_fps
                    settings.change_FPS_show(show_fps)
                elif back_text_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_slider:
                    slider_knob_rect.x = min(max(event.pos[0], 300), 500)
                    volume = (slider_knob_rect.x - 300) / 200
                    settings.change_volume(volume)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

