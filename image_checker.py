import pygame
import textures
pygame.init()
clock = pygame.time.Clock()

# image = textures.map_blocks["table1"]
image = textures.battle_enemies["player"][3][0][0]
# print(image.get_size())
# quit()
scalar = 10

time = 0
image = pygame.transform.scale(image, (image.get_size()[0]*scalar, image.get_size()[1]*scalar))
win = pygame.display.set_mode((image.get_size()[0]-1, image.get_size()[1]-1), 0, 32)

selector = []
run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    win.fill((4 * time, 4 * time, 4 * time))
    win.blit(image, (0, 0))
    try:
        pygame.draw.rect(win, (255, 255, 255), (selector[0][0] * scalar, selector[0][1] * scalar, (selector[1][0] - selector[0][0] + 1) * scalar, (selector[1][1] - selector[0][1] + 1) * scalar), 1)
    except IndexError:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selector:
                selector.append([mouse_pos[0] // scalar, mouse_pos[1] // scalar])
                selector.append([mouse_pos[0] // scalar, mouse_pos[1] // scalar])
                continue

            if event.button == 1:
                selector[0] = [mouse_pos[0] // scalar, mouse_pos[1] // scalar]
            if event.button == 3:
                selector[1] = [mouse_pos[0] // scalar, mouse_pos[1] // scalar]

            print("({}, {}, {}, {})".format(selector[0][0], selector[0][1], selector[1][0] - selector[0][0], selector[1][1] - selector[0][1]), selector)

    time += 1
    time %= 10
    pygame.display.update()
    clock.tick(30)
