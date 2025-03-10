import pygame  # type: ignore
from laser import Laser

spaceship_type = 0

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset, spaceship_type):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_type = spaceship_type
        self.image  = pygame.image.load(f"Graphics/spaceship{self.spaceship_type}.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2,self.screen_height))
        self.speed = 5
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 400
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")

    def get_user_input(self):
        keys = pygame.key.get_pressed()  

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            if self.spaceship_type == 1:
                laser_color = (255,0,0)
            elif self.spaceship_type == 2:
                laser_color = (0,255,0)
            elif self.spaceship_type == 3:
                laser_color = (0,0,255)
            else:
                laser_color = (243,216,63)
            laser = Laser(self.rect.center, 5, self.screen_height, laser_color)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
    

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset


    def recharge_laser(self): 
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()
        

    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2,self.screen_height))
        self.lasers_group.empty()

        
        
        
