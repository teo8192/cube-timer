import pygame
import time

SCREEN_RES = (640, 480)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    clock = pygame.time.Clock()

    start_time = 0
    end_time = 0

    ready = False
    going = False
    finishing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_SPACE]:
            if not ready and not going and not finishing:
                ready = True
            elif going:
                going = False
                finishing = True
        elif ready:
            ready = False
            going = True
            start_time = time.time()
        elif finishing:
            finishing = False

        if going:
            end_time = time.time()

        color = (255, 255, 255)
        if ready:
            color = (255, 0, 0)
        elif going:
            color = (0, 255, 0)
        elif finishing:
            color = (0, 0, 255)

        pygame.draw.rect(screen, (0,0,0), (0,0,screen.get_width(), screen.get_height()))

        text = pygame.font.Font(None, 150).render("{0:.2f}".format(end_time - start_time),
                                                 1, color)
        screen.blit(text, (640 / 2 - 75, 480 / 2 - 75))

        clock.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    main()
