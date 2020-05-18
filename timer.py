#!/bin/env python3

import pygame
import time
import datetime
from scrambler import scramble

SCREEN_RES = (640, 480)
NUMBER_DATAPOINTS_GRAPHED_MAX = 250

def repr(score):
    minute = score // 60
    seconds = score % 60
    return "{0:n}:{1:.3f}".format(minute, seconds)

def save(score):
    entry = "3x3x3;{};None;{};no;no;None\n".format(repr(score), datetime.datetime.now())
    file = open("save.csv", "a")

    file.write(entry)
    file.close()

def parse(time):
    min, sec = time.split(":", 1)
    return float(min) * 60 + float(sec)

def load():
    times = []
    try:
        file = open("save.csv", "r")
        for line in file.readlines():
            fields = line.split(";", 10)
            times.append(parse(fields[1]))

        file.close()

        return times
    except:
        return []

def avg(array):
    if len(array) == 0:
        return 0

    return sum(array) / len(array)

# The plan is to draw a praph in the background of the progress
def draw_background(screen, times):
    if len(times) < 2:
        return

    minimum = min(times)
    maximum = max(times)

    difference = maximum - minimum
    # go over and under by 10 percent
    low = minimum - difference * 0.1
    high = maximum + difference * 0.1
    difference = high - low

    num = len(times)

    start = SCREEN_RES[0] * 0.05
    end = SCREEN_RES[0] - SCREEN_RES[0] * 0.05

    step = (end - start) / (num - 1)

    last_x = 0
    last_y = 0

    for i, time in enumerate(times):
        x = step * i + start
        y = SCREEN_RES[1] - SCREEN_RES[1] * ((time - low) / difference)
        if last_x != 0 and last_y != 0:
            pygame.draw.line(screen, (50, 50, 50), (x, y), (last_x, last_y), 5)
        
        last_x, last_y = x, y

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RES)
    clock = pygame.time.Clock()

    times = load()

    start_time = 0
    end_time = 0

    ready = False
    going = False
    finishing = False

    scr = scramble()

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
                save(end_time - start_time)
                times.append(end_time - start_time)
                scr = scramble()
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

        draw_background(screen, times[-NUMBER_DATAPOINTS_GRAPHED_MAX:])

        text = pygame.font.Font(None, 150).render("{0:.2f}".format(end_time - start_time),
                                                 1, color)
        screen.blit(text, (int(640 / 2 - 75), int(480 / 2 - 75)))

        if not going:
            text = pygame.font.Font(None, 25).render("{}".format(scr),
                                                     1, (255,255,255))
            screen.blit(text, (0, 0))

        if len(times) > 0 and (not going or ready):
            text = pygame.font.Font(None, 50).render("min: {0:.2f}".format(min(times)),
                                                     1, (255,255,255))
            screen.blit(text, (50, 350))
            
            text = pygame.font.Font(None, 50).render("avg-5: {0:.2f}".format(avg(times[-5:])),
                                                     1, (255,255,255))
            screen.blit(text, (50, 400))
            
            text = pygame.font.Font(None, 50).render("avg-12: {0:.2f}".format(avg(times[-12:])),
                                                     1, (255,255,255))
            screen.blit(text, (350, 350))

            text = pygame.font.Font(None, 50).render("n: {}".format(len(times)),
                                                     1, (255,255,255))
            screen.blit(text, (350, 400))

        clock.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    main()
