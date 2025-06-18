import pygame as pg
from random import randrange

Window = 750
Tile = 50
RANGE = (Tile // 2 , Window  - Tile // 2,Tile)
get_random_pos = lambda: (randrange(*RANGE), randrange(*RANGE))
snake = pg.Rect([0,0, Tile - 2, Tile - 2])
snake.center = get_random_pos()
length = 1
segments = [snake.copy()]
snake_direction = (0,0)
time, time_step = 0, 250
food = snake.copy()
food.center = get_random_pos()
screen = pg.display.set_mode((Window, Window))
clock = pg.time.Clock()
dictdir = {
    pg.K_z: 1,
    pg.K_s: 1,
    pg.K_q: 1,
    pg.K_d: 1
}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_z and dictdir[pg.K_z]:
                snake_direction = (0, -Tile)
                dictdir = {pg.K_z: 1, pg.K_s: 0, pg.K_q: 1, pg.K_d: 1}
            elif event.key == pg.K_s and dictdir[pg.K_s]:
                snake_direction = (0, Tile)
                dictdir = {pg.K_z: 0, pg.K_s: 1, pg.K_q: 1, pg.K_d: 1}
            elif event.key == pg.K_q and dictdir[pg.K_q]:
                snake_direction = (-Tile, 0)
                dictdir = {pg.K_z: 1, pg.K_s: 1, pg.K_q: 1, pg.K_d: 0}
            elif event.key == pg.K_d and dictdir[pg.K_d]:
                snake_direction = (Tile, 0)
                dictdir = {pg.K_z: 1, pg.K_s: 1, pg.K_q: 0, pg.K_d: 1}
        screen.fill('black')
        # Check for collisions with the walls and self eating
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if not (0 <= snake.left < Window and 0 <= snake.top < Window) or self_eating:
            snake.center = get_random_pos()
            food.center = get_random_pos()
            lenght, snake_direction = 1, (0, 0)
            segments = [snake.copy()]
        # Check if the snake has eaten the food
        if snake.center == food.center:
            length += 1
            food.center = get_random_pos()
        # Draw the food
        pg.draw.rect(screen, 'red', food)
        # Draw the snake
        [pg.draw.rect(screen, 'green', segment) for segment in segments]
        # Move the snake
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_direction)
            segments.append(snake.copy())
            segments = segments[-length:]
        pg.display.flip()
        clock.tick(60)