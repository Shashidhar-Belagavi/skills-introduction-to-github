import pygame, random # type: ignore
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import Mysteryship

class Game(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.level = 1
        self.level_transition = False
        self.alien_shoot_delay = 400
        self.lower = 6000
        self.upper = 12000
        self.spaceship_type = 0
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship = Spaceship(self.screen_width, self.screen_height, self.offset, self.spaceship_type)
        self.spaceship_group.add(self.spaceship)
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")
        self.exploion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        self.mystery_ship_sound = pygame.mixer.Sound("Sounds/Mystery Ship.ogg")
        self.game_over_sound = pygame.mixer.Sound("Sounds/game over.ogg")
        self.load_highscore()

    def update_spaceship(self, type):
        self.spaceship_group.empty()
        self.spaceship_type = type
        self.spaceship = Spaceship(self.screen_width, self.screen_height, self.offset, self.spaceship_type)
        self.spaceship_group.add(self.spaceship)


    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        if self.level == 1:
            no_of_obstacles = 4
        elif self.level == 2:
            no_of_obstacles = 3
        else:
            no_of_obstacles = 2
        gap = (self.screen_width + self.offset - (no_of_obstacles * obstacle_width))/(no_of_obstacles + 1)
        obstacles = []
        for i in range(no_of_obstacles):
            offset_x = (i+1)*gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)  
        return obstacles 
    
    def create_aliens(self):
        global alien_type
        global alien_color
        if self.level == 1:
            for row in range(5):
                for column in range(11):
                    x = 75 + column * 55
                    y = 110 + row * 55
                    if row==0:
                        alien_type = 3
                        alien_color = ((0,255,0))
                    elif row in (1,2):
                        alien_type = 2
                        alien_color = ((243,216,63))
                    else:
                        alien_type = 1
                        alien_color = ((117,122,176))
                    alien = Alien(alien_type, alien_color, x + self.offset/2, y)
                    self.aliens_group.add(alien)
        elif self.level == 2:
            for row in range(6):
                for column in range(11):
                    x = 75 + column * 55
                    y = 110 + row * 55
                    if row in (0,1):
                        alien_type = 3
                        alien_color = ((0,255,0))
                    elif row in (2,3):
                        alien_type = 2
                        alien_color = ((243,216,63))
                    else:
                        alien_type = 1
                        alien_color = ((117,122,176))
                    alien = Alien(alien_type, alien_color, x + self.offset/2, y)
                    self.aliens_group.add(alien)
        else:
            for row in range(7):
                for column in range(11):
                    x = 75 + column * 55
                    y = 110 + row * 55
                    if row in (0,1,2):
                        alien_type = 3
                        alien_color = ((0,255,0))
                    elif row in (3,4):
                        alien_type = 2
                        alien_color = ((243,216,63))
                    else:
                        alien_type = 1
                        alien_color = ((117,122,176))
                    alien = Alien(alien_type, alien_color, x + self.offset/2, y)
                    self.aliens_group.add(alien)
    
    def move_aliens(self, offset):
        self.offset = offset
        self.aliens_group.update(self.aliens_direction)
        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                if self.level == 1:
                    self.move_aliens_down(2)
                elif self.level == 2:
                    self.move_aliens_down(3)
                else:
                    self.move_aliens_down(4)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                if self.level == 1:
                    self.move_aliens_down(2)
                elif self.level == 2:
                    self.move_aliens_down(3)
                else:
                    self.move_aliens_down(4)

    def move_aliens_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            alien_color = random_alien.color
            if random_alien.type == 1:
                laser_speed = -5
            elif random_alien.type == 2:
                laser_speed = -6
            else:
                laser_speed = -7
            laser = Laser(random_alien.rect.center, laser_speed, self.screen_height, alien_color)
            self.alien_lasers_group.add(laser) 

    def create_mystery_ship(self):
        self.mystery_ship = Mysteryship(self.screen_width, self.offset)
        self.mystery_ship_group.add(self.mystery_ship)

    def check_for_collisions(self):
        # Spaceship   
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group: 
                alien_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if alien_hit:
                    self.exploion_sound.play()
                    for alien in alien_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.mystery_ship.mystery_ship_sound.stop()
                    self.exploion_sound.play()
                    self.score += random.randint(500,1000)
                    self.check_for_highscore()
                    laser_sprite.kill()
               
                for obstacle in self.obstacles: 
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()
        # Alien Lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over() 
                    laser_sprite.kill()
                
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group.sprite.lasers_group, True):
                    laser_sprite.kill()

                for obstacle in self.obstacles: 
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        # Aliens
        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def game_over(self):
        if self.mystery_ship_group.sprites():
            self.mystery_ship.mystery_ship_sound.stop()
        self.game_over_sound.play()
        self.run = False
        
    def reset(self):
        self.run = True
        self.level = 1
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def restart(self):
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt","w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

    def level_change(self):
        self.level += 1
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        for obstacle in self.obstacles:
            obstacle.blocks_group.empty()
        self.alien_shoot_delay -= 50
        self.lower += 6000
        self.upper += 6000
        self.create_aliens()
        self.move_aliens(self.offset)
        self.obstacles = self.create_obstacles()

            
            



        




                        




                








