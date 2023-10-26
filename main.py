import random, os, sys
import pygame as pg

selected_modifiers = {'Double speed': False, 'Low Gravity': False}
pg.init()
class Character():
    def __init__(self, x, y):
        self.movex = 0
        self.movey = 1
        self.rect = pg.Rect((x, y, 36, 26))
        self.birdimg = pg.image.load(os.path.relpath('bird.png'))

    def move(self, y):
        self.rect = self.rect.move(0,y)
    def move2(self, y):
        self.rect.y = self.rect.y + y
    def display(self,screen):
        screen.blit(self.birdimg, self.rect)
    def collide(self, first_wall_pair):
        return self.rect.colliderect(first_wall_pair.top_wall) or self.rect.colliderect(first_wall_pair.bottom_wall)


class PillarPair():
    def __init__(self,width, height, xcoord, screen):
        self.width = width
        self.height = height
        self.xcoord = xcoord
        self.screen = screen
        self.wall_width = 15
        self.gen_wall(xcoord)
        self.asset_loader(width, height)

    def gen_wall(self, xcoord):
        self.top_rect_length = random.randint(50, 300)
        self.bottom_rect_length = self.height - self.top_rect_length - 200
        self.top_wall = pg.Rect(xcoord, 0, self.wall_width, self.top_rect_length)
        self.bottom_wall = pg.Rect(xcoord, self.height - self.bottom_rect_length, self.wall_width, self.bottom_rect_length)

    def asset_loader(self, width, height):
        self.pillar_top = pg.image.load(os.path.relpath('tube_top.png'))
        self.pillar_bottom = pg.image.load(os.path.relpath('tube_bottom.png'))
        self.pillar_top_transformed = pg.transform.scale(self.pillar_top, (self.wall_width, self.top_wall.height))
        self.pillar_bottom_transformed = pg.transform.scale(self.pillar_bottom, (self.wall_width, self.bottom_wall.height))

    def draw_pillars(self):
        self.screen.blit(self.pillar_top_transformed, self.top_wall)
        self.screen.blit(self.pillar_bottom_transformed, self.bottom_wall)

    def move(self, x):
        self.top_wall = self.top_wall.move(x, 0)
        self.bottom_wall = self.bottom_wall.move(x, 0)

    def copy(self, other):
        self.top_wall = other.top_wall
        self.bottom_wall = other.bottom_wall

def play():
    width = 300
    height = 510
    size = width, height
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Flappy Bird ECE198 F23")
    x = 10
    y = height / 2
    move_y = 4
    bird = Character(x, y)
    clock = pg.time.Clock()

    score = 0
    frame = 0
    acceleration = 0
    up_acceleration = 0
    move_yes = 0
    collision_processed = 1
    set_yes = 1
    first_wall_x = 200
    second_wall_x = 350
    third_wall_x = 500
    total_time_since_event = 0
    initialize = 0

    background = pg.image.load(os.path.relpath('bg.png'))
    background = pg.transform.scale(background, (width, height))
    first_wall_pair = PillarPair(width, height, first_wall_x, screen)
    second_wall_pair = PillarPair(width, height, second_wall_x, screen)
    third_wall_pair = PillarPair(width, height, third_wall_x, screen)



    while True:

        a = clock.tick_busy_loop(120)
        total_time_since_event += a
        if initialize == 0:
            total_time_since_event = 8
            initialize = 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                move_y = 1
                move_yes = 1
                total_time_since_event = 0
                frame = 0

        if bird.collide(first_wall_pair):
            score_card_disp = collided(score, width, height)
            display_score(score)
        elif bird.rect.left > first_wall_pair.top_wall.right and collision_processed == 1:
            score += 1
            collision_processed = 0

        frame += 1



        first_wall_pair.move(-1)
        second_wall_pair.move(-1)
        third_wall_pair.move(-1)
        if first_wall_pair.top_wall.left  == -first_wall_pair.wall_width:
            first_wall_pair.copy(second_wall_pair)
            second_wall_pair.copy(third_wall_pair)
            temp_wall_x = third_wall_pair.top_wall.x
            third_wall_pair.gen_wall(temp_wall_x + 150)
            first_wall_pair.asset_loader(width, height)
            second_wall_pair.asset_loader(width, height)
            third_wall_pair.asset_loader(width, height)
            collision_processed = 1

        if bird.rect.bottom >= height:
            bird.rect.bottom = height
        if bird.rect.top <= 0:
            bird.rect.top = 0

        if move_yes == 0:
            if frame <= 15:
                move_y = 1
                bird.move2(move_y)
                if frame == 15:
                    move_y = 4
                    bird.move2(move_y)
                    move_y = 1
                    acceleration = 0
            else:
                acceleration += 1
                if acceleration == 46:
                    if move_y < 10:
                        move_y += 1
                    acceleration = 0
                bird.move2(move_y)

        else:
            up_acceleration += 1
            if up_acceleration == 1:
                if move_y > -6:
                    move_y -= 0.5
                    if move_y <= -6:
                        move_yes = 0

                bird.move2(move_y)
                up_acceleration = 0


        screen.fill((0,0,0))
        screen.blit(background, (0,0))
        first_wall_pair.draw_pillars()
        second_wall_pair.draw_pillars()
        third_wall_pair.draw_pillars()
        bird.display(screen)

        pg.display.flip()


def collided(score, width, height):
    score_font = pg.font.get_default_font()
    score_card  = pg.font.Font(score_font, 50)
    score_card_disp = score_card.render(str(score), False, (0, 0, 0))
    return score_card_disp

"""
def another_draw(score_card_disp, width, height, first_wall_pair, second_wall_pair, bird, background):
    screen = pg.display.set_mode((width, height))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    play()

        screen.blit(background, (0,0))

        first_wall_pair.draw_pillars()
        second_wall_pair.draw_pillars()

        bird.display(screen)
        screen.blit(score_card_disp, (width / 2, height / 2))
        pg.display.flip()
"""

def display_score(score):
    score_width, score_height = 200, 100  # Set the size for the score window
    score_screen = pg.display.set_mode((score_width, score_height))
    pg.display.set_caption("Display Score")

    score_font = pg.font.Font(None, 36)
    score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        score_screen.fill((0, 0, 0))
        score_screen.blit(score_text, (score_width // 2 - score_text.get_width() // 2, score_height // 2 - score_text.get_height() // 2))
        pg.display.flip()


play()