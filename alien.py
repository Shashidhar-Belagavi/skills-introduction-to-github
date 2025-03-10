import pygame, random # type: ignore

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, color, x, y):
        super().__init__()
        self.type = type
        self.color = color
        path = f"Graphics/alien_{self.type}.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
 
    def update(self, direction):
        self.rect.x += direction

class Mysteryship(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png").convert_alpha()
        x = random.choice([self.offset/2, (self.screen_width + self.offset/2) - self.image.get_width()])
        if x == self.offset/2:
            self.speed = 2
        else:
            self.speed = -2
        self.rect = self.image.get_rect(topleft = (x,90))
        self.mystery_ship_sound = pygame.mixer.Sound("Sounds/Mystery Ship.ogg")
        self.mystery_ship_sound.play()

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset/2:
            self.mystery_ship_sound.stop()
            self.kill()
        elif self.rect.left < self.offset/2:
            self.mystery_ship_sound.stop()
            self.kill()




    