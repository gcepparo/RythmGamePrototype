import sys, pygame
import constants as const
from pygame.locals import * #keys
import actors
import mapper

pygame.init()

size = width, height = const.SCREENWIDTH, const.SCREENHEIGHT
screen = pygame.display.set_mode(size)

bgColor = 0, 0, 0 #black

#actor initialization
player = actors.Player()
bullets = mapper.randomMap(30)
collDetect = actors.CollisionDetector()

# Event loop
while 1:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_a:
                player.moveup()
            if event.key == K_s:
                player.movedown()
        # elif event.type == KEYUP:
        #     if event.key == K_a or event.key == K_s:
        #         player.movepos = [0,0]
        #         player.state = "still"

    # Logic 
    player.update()
    for b in bullets:
        b.update()

    collDetect.detectCollisions(player,bullets)

    # Rendering
    screen.fill(bgColor) #blit = copy pixels on the screen
    for b in bullets:
        screen.blit(b.image, b.rect)
    screen.blit(player.image, player.rect)

    # tmp1, tmp2 = collDetect.get_hit_miss_images()
    # screen.blit(tmp1,tmp2)    
    screen.blit(*collDetect.get_hit_miss_images())

    pygame.display.flip()  #displays everything to screen (buffer)