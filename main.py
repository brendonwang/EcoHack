import sys
import time
import pygame
import os

pygame.init()

clock = pygame.time.Clock()
clock.tick(30)

screen_width = 1000
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('EcoHack')


def asset_path(file_name):
    file_name = os.path.join('asset', file_name)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        file_name = os.path.join(getattr(sys, '_MEIPASS'), file_name)
    return file_name


# # define font
font_size = 40
font = pygame.font.Font(asset_path("Font.ttf"), font_size)

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
black = pygame.image.load(asset_path("Black.png"))
dirt = pygame.image.load(asset_path("Dirt.png"))
row = 0

tile_list = []


def main(tiles):
    row_count = 0
    for row in tiles:
        col = 0
        for tile in row:
            if tile == 1:
                img = pygame.transform.scale(black, (40, 40))
                rect = img.get_rect()
                rect.x = col * 40
                rect.y = row_count * 40
                tile = (img, rect)
                tile_list.append(tile)
            if tile == 2:
                trash_sprite = Trash(col * 40, row_count * 40)
                trash_group.add(trash_sprite)
            if tile == 3:
                bag_sprite = Bag(col * 40, row_count * 40)
                bag_group.add(bag_sprite)
            if tile == 4:
                img = pygame.transform.scale(dirt, (40, 40))
                rect = img.get_rect()
                rect.x = col * 40
                rect.y = row_count * 40
                tile = (img, rect)
                tile_list.append(tile)
            col += 1
        row_count += 1


def draw():
    for tile in tile_list:
        screen.blit(tile[0], tile[1])


tile_size = 40


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.img = pygame.image.load(asset_path("PlayerRight.png"))
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
            self.img = pygame.image.load(asset_path("Player.png"))
        if key[pygame.K_RIGHT]:
            dx += 5
            self.img = pygame.image.load(asset_path("PlayerRight.png"))
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
    def __init__(self, x, y):
        super(Trash, self).__init__()
        self.image = pygame.transform.scale(trash, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x - 40
        self.rect.y = y - 40


class Bag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bag, self).__init__()
        self.image = pygame.transform.scale(bag, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x - 40
        self.rect.y = y - 40


class Bunny(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Bunny, self).__init__()
        self.direction = -1
        self.img = pygame.image.load(asset_path("BunnyRight.png"))
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

            self.rect.x += 5 * self.direction
            if self.rect.left <= 0:
                self.direction = 1
                self.img = pygame.image.load(asset_path("Bunny.png"))
            elif self.rect.right >= 1000:
                self.direction = -1
                self.img = pygame.image.load(asset_path("BunnyRight.png"))

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


white = (255, 255, 255)


class Text:
    def __init__(self, text, font, x, y, fsize, color = (255, 255, 255)):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.fsize = fsize
        self.img = 0
        self.rect = 0
        self.color = color

    def draw_text(self):
        lines = self.text.splitlines()
        for i, l in enumerate(lines):
            self.img = font.render(l, False, self.color)
            self.rect = self.img.get_rect()
            self.rect.center = (self.x, self.y)
            screen.blit(self.img, (self.rect.x, self.rect.y + self.fsize * (i - (len(lines) - 2))))


class Poster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Poster, self).__init__()
        self.img = pygame.image.load(asset_path("Poster.png"))
        self.img = pygame.transform.scale(self.img, (90, 100))
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect.centerx = x
        self.rect.centery = y
    def update(self):
        screen.blit(self.img, self.rect)


class Button:
    def __init__(self, x, y, image):
        self.img = pygame.image.load(image)
        self.data = image
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
            self.img = pygame.image.load((self.data.replace(".png", "") + "_Animation.png"))
        else:
            self.img = pygame.image.load(self.data)
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
def level2():
    player.rect.x = 120
    player.rect.y = 20
    screen.fill((0, 0, 0))
    text = Text("\nThe next day\n", font, 500, screen_height / 2, font_size)
    text.draw_text()
    pygame.display.update()
    time.sleep(5)
    tiles = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    ]
    main(tiles)


text = Text("People all around the have thrown\n"
            "trash around the world. Animals all around\n"
            "the world have died and the world is in \n"
            "a state of emergency.", font, 500, 280, 40)

text.draw_text()

pygame.display.update()
time.sleep(9)
player = Player(120, 20)
bunny = Bunny(player)
bunny_group = pygame.sprite.Group()
bunny_group.add(bunny)
background = pygame.image.load(asset_path("Background.png"))
trash = pygame.image.load(asset_path("Trash.png"))
bag = pygame.image.load(asset_path("Bag.png"))
main(tiles)
help_btn = Button(230, 180, asset_path("Help.png"))
ignore_btn = Button(560, 180, asset_path("Ignore.png"))
health = 3
health_img = pygame.transform.scale(pygame.image.load(asset_path("Health.png")), (39, 30))
bag_group = pygame.sprite.Group()
trash_group = pygame.sprite.Group()
bunny_hit = False
coin = pygame.image.load(asset_path("Coin.png"))
coin = pygame.transform.scale(coin, (40, 40))
coin_rect = coin.get_rect()
coin_rect.x = 900
coin_rect.y = 10
player_group = pygame.sprite.Group(player)
score = 0
poster = Poster(500, 280)
day = 1
no = Button
clicked = False
background_day = 0
raw_score = 0
show = False
yes_btn = Button(300, 460, asset_path("Yes.png"))
no_btn = Button(600, 460, asset_path("No.png"))
first = True

while True:
    screen.blit(background, (0, 0))
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for index, _ in enumerate(range(health)):
        screen.blit(health_img, (10 + index * (tile_size + 10), 10))
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
            health -= 1
            bunny.kill()
            bunny_hit = True
            tile_list = []
            level2()
            day = 2
            raw_score = 7
    if raw_score == 6:
        tile_list = []
        level2()
        raw_score = 7
        day = 2
    if day == 1 or day == 3:
        trash_group.draw(screen)
        bag_group.draw(screen)
    if pygame.sprite.spritecollide(player, trash_group, True):
        score += 1
        raw_score += 1
    if pygame.sprite.spritecollide(player, bag_group, True):
        score += 2
        raw_score += 2
    if health == 0:
        screen.fill((0, 0, 0))
        text = Text("You died", font, 500, 280, font_size)
        time.sleep(5)
        pygame.display.update()
        break
    if day == 3 and first:
        first = False
        player.rect.x = 120
        player.rect.y = 20
        background = pygame.image.load(asset_path("Background.png"))
        tile_list = []
        tiles = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        main(tiles)
        show = False
    if raw_score == 20:
        raw_score = 21
        screen.fill((0, 0, 0))
        text = Text(f"You WON with a score of {score}", font, 500, 280, font_size)
        text.draw_text()
        pygame.display.flip()
        time.sleep(5)
        sys.exit(0)
    if day == 2:
        background = pygame.image.load(asset_path("Wall.png"))
        if pygame.sprite.spritecollide(poster, player_group, False):
            text = Text("Click Space to Look at Poster", font, 500, 100, font_size)
            text.draw_text()
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                poster.img = pygame.image.load(asset_path("Blank_Poster.png"))
                poster.img = pygame.transform.scale(poster.img, (540, 580))
                poster.rect.x = 230
                poster.rect.y = 0
                show = True
            else:
                poster.img = pygame.image.load(asset_path("Poster.png"))
                poster.img = pygame.transform.scale(poster.img, (90, 100))
                poster.rect.centerx = 500
                poster.rect.centery = 280
                show = False

        poster.update()
        if show:
            text = Text("Recently, the world has \n"
                        "become polluted.\n"
                        " The environment and \n"
                        "homes of animals are \n"
                        "being destroyed, so we\n"
                        " will try to stop this\n"
                        "Would you like to help \n"
                        "make the world a better, \n"
                        "cleaner place? \n"
                        "Join EcoSave today!", font, 500, 400, font_size)
            text.draw_text()
            if yes_btn.draw():
                day = 3

            if no_btn.draw():
                screen.fill((255, 255, 255))
                background = pygame.image.load(asset_path("Bunny_Background.png"))
                background = pygame.transform.scale(background, (1000, 580))
                screen.blit(background, (0, 0))
                screen.blit(pygame.transform.scale(pygame.image.load(asset_path("Mayor.png")),(120, 180)), (750, 250))
                text = Text("Because of the Pollution, We will all have \n"
                            "to evacuate. Please pack your bags.",font, 500, 50, font_size, (0, 0, 0))
                text.draw_text()
                pygame.display.update()
                time.sleep(5)
                screen.fill((0, 0, 0))
                text = font.render("You died", False, (255, 255, 255))
                screen.blit(text, (400, 270))
                pygame.display.update()
                time.sleep(5)

                break


    if not show:
        player_group.update()
    text = font.render(f"X{score}", False, white)
    # pygame.draw.rect(screen, white, player.rect)
    screen.blit(text, (940, 15))
    screen.blit(coin, coin_rect)
    pygame.display.update()
