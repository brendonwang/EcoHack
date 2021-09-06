import sys
import time
import pygame
pygame.init()

clock = pygame.time.Clock()
clock.tick(30)

screen_width = 1000
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('EcoHack')

# # define font
font_size = 40
font = pygame.font.Font("Font.ttf", font_size)


tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
black = pygame.image.load("Black.png")
row = 0

tile_list = []


def main(tiles):
    row_count = 0
    for row in tiles:
        col = 0
        for tile in row:
            if tile == 1:
                img = pygame.transform.scale(black, (50, 50))
                rect = img.get_rect()
                rect.x = col * 40
                rect.y = row_count * 40
                tile = (img, rect)
                tile_list.append(tile)
            if tile == 2:
                trash_sprite = Trash(col*40, row_count * 40)
                trash_group.add(trash_sprite)
            if tile == 3:
                bag_sprite = Bag(col*40, row_count * 40)
                bag_group.add(bag_sprite)
            col += 1
        row_count += 1
def draw():
    for tile in tile_list:
        screen.blit(tile[0], tile[1])
tile_size = 40
class Player():
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.img = pygame.image.load("PlayerRight.png")
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.jumped = False
        self.speed = 1
        self.rect.x = x
        self.rect.y = y
        self.v = 0
        self.vel_y = 0

    def update(self):
        dx = 0
        dy = 0
        F = 1 / 2 * 1 * 6 ** 2
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumped:
            self.vel_y = -F
            self.jumped = True
        if key[pygame.K_LEFT]:
            dx -= 5
            self.img = pygame.image.load("Player.png")
        if key[pygame.K_RIGHT]:
            dx += 5
            self.img = pygame.image.load("PlayerRight.png")
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        for tile in tile_list:
            # check for collision in x axis
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                # check if below the ground i.e jumping
                dx = 0
            # check for collision in y axis
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if below the ground i.e falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom >= 560:
            self.rect.bottom = 560
            self.jumped = False
        self.in_air = True

        # Draw the player
        screen.blit(self.img, self.rect)

class Trash(pygame.sprite.Sprite):
    def __init__(self,  x, y):
        super(Trash, self).__init__()
        self.image = pygame.transform.scale(trash, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x-40
        self.rect.y  = y - 40
class Bag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bag, self).__init__()
        self.image = pygame.transform.scale(bag, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x - 40
        self.rect.y  = y - 40
class Bunny(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Bunny, self).__init__()
        self.direction = -1
        self.img = pygame.image.load("BunnyRight.png")
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.jumped = False
        self.speed = 1
        self.rect.x = 500
        self.rect.y = 280
        self.v = 0
        self.vel_y = 0

    def update(self):
        dx = 0
        dy = 0

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        if not pygame.sprite.collide_rect(self, player):

            self.rect.x += 5*self.direction
            if self.rect.left <=0:
                self.direction = 1
                self.img = pygame.image.load("Bunny.png")
            elif self.rect.right >= 1000:
                self.direction = -1
                self.img = pygame.image.load("BunnyRight.png")

        for tile in tile_list:
            # check for collision in x axis
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                # check if below the ground i.e jumping
                dx = 0
            # check for collision in y axis
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if below the ground i.e falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom >= 560:
            self.rect.bottom = 560
            self.jumped = False
        self.in_air = True

        # Draw the player
        screen.blit(self.img, self.rect)


class Text:
    def __init__(self, text, font, x, y, fsize):

        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.fsize = fsize
        self.img = 0
        self.rect = 0

    def draw_text(self):
        lines = self.text.splitlines()
        for i, l in enumerate(lines):
            self.img = font.render(l, False, (255, 255, 255))
            self.rect = self.img.get_rect()
            self.rect.center = (self.x, self.y)
            screen.blit(self.img, (self.rect.x, self.rect.y + self.fsize * (i - (len(lines) - 2))))



class Button:
    def __init__(self, x, y, image):
        self.img = pygame.image.load(image).convert()
        # self.img = pygame.transform.scale(self.img, (72, 48))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(3)[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed(3)[0] == 0:
            self.clicked = False
        # draw button
        screen.blit(self.img, self.rect)
        return action
def level1():
    tiles = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    main(tiles)
    draw()


text = Text("People all around the have thrown\n"
            "trash around the  Animals all around\n"
            "the have died and the is in \n"
            "A state of emergency.", font, 500, 280, 40)

text.draw_text()

pygame.display.update()
time.sleep(9)
player = Player(120, 20)
bunny = Bunny(player)
bunny_group = pygame.sprite.Group()
bunny_group.add(bunny)
background = pygame.image.load("Background.png")
trash = pygame.image.load("Trash.png")
bag = pygame.image.load("Bag.png")
main(tiles)
help_btn = Button(230, 180, "Help.png")
ignore_btn = Button(560, 180, "Ignore.png")
health = 3
health_img = pygame.transform.scale(pygame.image.load("health.png"), (39, 30))
bag_group = pygame.sprite.Group()
trash_group = pygame.sprite.Group()
bunny_hit = False
coin = pygame.image.load("Coin.png")
coin = pygame.transform.scale(coin, (40, 40))
coin_rect = coin.get_rect()
coin_rect.x = 900
coin_rect.y = 10
score = 0
while True:
    screen.blit(background, (0, 0))
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.update()
    for index, _ in enumerate(range(health)):
        screen.blit(health_img, (10 + index * (tile_size+10), 10))
    bunny_group.update()
    if pygame.sprite.collide_rect(bunny, player) and (not bunny_hit):
        text = Text("Please help me clean up my land, \n"
                    "it has trash strewn everywhere!", font, 500, 100, 40)
        text.draw_text()
        if help_btn.draw():
            level1()
            bunny.kill()
            bunny_hit = True
        if ignore_btn.draw():
            health-=1
            bunny.kill()
            bunny_hit = True

    trash_group.draw(screen)
    bag_group.draw(screen)
    if pygame.sprite.spritecollide(player, trash_group, True):
        score += 1
    if pygame.sprite.spritecollide(player, bag_group, True):
        score += 2
    if health==0:
        text = Text("You died", font, 500, 280, font_size)
        time.sleep(5)
        break
    if score == 6:
        screen.fill((0, 0, 0))
        while True:
            text = Text("You Beat Level One!\n"
                        "You have to buy level 2 and 3\n"
                        "but that feature hasn't been\n"
                        "added yet!\n", font, 500, 280, font_size)
            text.draw_text()
            pygame.display.update()
    text = font.render(f"X{score}", False, (255, 255, 255))
    screen.blit(text, (940, 15))
    screen.blit(coin, coin_rect)
    pygame.display.update()