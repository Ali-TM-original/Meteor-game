def main_logic():
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

    for beams in laser_group:
        if pygame.sprite.spritecollide(beams, meteor_group, True):
            beams.kill()