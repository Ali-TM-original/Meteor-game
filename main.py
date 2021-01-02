import pygame
import sys
import random
from pygame import mixer

shield_range = 6
score = 0


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.shield_surface = pygame.image.load('shield.png')
        # self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.borders()
        self.display_health()

    def borders(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.bottom >= 720:
            self.rect.bottom = 720
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        # spaceship.kill() .kill function used to destroy any sprite on screen

    def display_health(self):
        for index, shield in enumerate(range(shield_range)):  # enumerate gives index in for loop
            screen.blit(self.shield_surface, (index * 40, 10))


class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        if self.rect.centery >= 750:
            self.kill()


class laser_beam(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= 0:
            self.kill()


pygame.init()
clock = pygame.time.Clock()
FONT = pygame.font.Font('LazenbyCompSmooth.ttf', 40)
MAIN_LOOP_FONT = pygame.font.Font('LazenbyCompSmooth.ttf', 40)

HEIGHT = 1280
WIDTH = 720
screen = pygame.display.set_mode((HEIGHT, WIDTH))  # pygame.FULLSCREEN

spaceship = SpaceShip('spaceship.png', 650, 500)
spaceship_group = pygame.sprite.GroupSingle(spaceship)
# spaceship_group.add(spaceship)

x_speed_random = random.randint(0, 6)
y_speed_random = random.randint(0, 6)
x_coordinate_random = random.randint(0, 1280)
y_coordinate_random = random.randint(0, 720)

cool_meteor = Meteor('Meteor1.png', x_coordinate_random, -100, x_speed_random, y_speed_random)
meteor_group = pygame.sprite.Group()
meteor_group.add(cool_meteor)

# mixer.music.load('Goat Scream.mp3')
# mixer.music.play(0)

METEOR_EVENT = pygame.USEREVENT  # custom event
pygame.time.set_timer(METEOR_EVENT, 400)  # timers that triggers on METEOR EVENT 300 miliseconds
# to add more meteors decrease the timer so that more meteors spawn in certain time

laser_group = pygame.sprite.Group()


def main_game():
    global shield_range
    laser_group.draw(screen)
    laser_group.update()

    # giant group of meteors. groups useful for displaying single/multiple sprites on screen
    meteor_group.draw(screen)
    meteor_group.update()  # .update method is from the class so that the position of the sprite change

    spaceship_group.draw(screen)  # contains only 1 sprite that's why used GroupSingle
    spaceship_group.update()

    # meteor_group.draw(screen)
    # meteor_group.update()

    # Collisions
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        mixer.music.load('Goat Scream.mp3')
        mixer.music.play(1)
        shield_range -= 1

    # checking if rocks are beyond y axis
    for big_space_rocks in meteor_group:
        if big_space_rocks.rect.bottom >= 750:
            return -1

    for beams in laser_group:
        if pygame.sprite.spritecollide(beams, meteor_group, True):
            beams.kill()
            return 10
    return 0


def game_over_texts():
    RENDERED_TEXT = FONT.render('Game Over', True, (255, 255, 255))
    TEXT_RECTANGLE = RENDERED_TEXT.get_rect(center=(640, 360))
    screen.blit(RENDERED_TEXT, TEXT_RECTANGLE)

    RENDERED_TEXT_SCORE = FONT.render('Score: ' + str(score), True, (255, 255, 255))
    TEXT_RECTANGLE_SCORE = RENDERED_TEXT.get_rect(center=(640, 400))
    screen.blit(RENDERED_TEXT_SCORE, TEXT_RECTANGLE_SCORE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r and shield_range <= 0:
                shield_range = 5
                score = 0
        if event.type == pygame.MOUSEBUTTONDOWN and shield_range > 0:
            mixer.music.load('laser_sound.mp3')
            mixer.music.play(0)
            new_laser = laser_beam('Laser.png', event.pos, 25)
            laser_group.add(new_laser)
        if event.type == METEOR_EVENT:
            # meteor_image_list = ['Meteor1.png', 'Meteor2.png', 'Meteor3.png']  will not need a list. Reduce space
            meteor_image = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
            random_x_position = random.randrange(0, 1280)
            random_y_position = random.randrange(-500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(2, 8)
            meteor = Meteor(meteor_image, random_x_position, random_y_position, random_x_speed, random_y_speed)
            meteor_group.add(meteor)

    screen.fill((42, 45, 51))

    # if shields are not 0 then run
    if shield_range > 0:
        score += int(main_game())
    else:                       # if shields are 0 then not bring to the ending screen
        game_over_texts()
        meteor_group.empty()

    # font for score

    RENDERED_TEXT_SCORE_GAME = FONT.render('Score: ' + str(score), True, (255, 255, 255))
    TEXT_RECTANGLE_SCORE_GAME = RENDERED_TEXT_SCORE_GAME.get_rect(center=(1150, 50))
    screen.blit(RENDERED_TEXT_SCORE_GAME, TEXT_RECTANGLE_SCORE_GAME)

    pygame.display.update()
    pygame.mouse.set_visible(False)
    clock.tick(120)
