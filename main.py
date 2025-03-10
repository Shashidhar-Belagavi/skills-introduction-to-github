import pygame, random, sys
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

# colors
GREY = (29,29,27)
YELLOW = (243,216,63)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SILVER = (192,192,192)
BLACK = (0,0,0)
TRANSPARENT_GREY = (29,29,27,230)

# fonts
font = pygame.font.Font("FONT/monogram.ttf", 40)
font_1 = pygame.font.SysFont("Georgia",30)
font_2 = pygame.font.Font("FONT/invaders 1.ttf",220)
font_3 = pygame.font.SysFont("Times New Roman", 60)
font_4 = pygame.font.Font("FONT/Comic Sans.ttf", 30)
font_5 = pygame.font.SysFont("Georgia",40)
font_6 = pygame.font.Font("FONT/monogram.ttf", 80)

# Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET), pygame.SCALED | pygame.RESIZABLE)
background = pygame.Surface((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET), pygame.SRCALPHA)
Title = pygame.display.set_caption("Space Invaders")

# Icon
Ship_1 = pygame.image.load("Icons/Ship_1.png").convert_alpha()
Ship_2 = pygame.image.load("Icons/Ship_2.png").convert_alpha()
Ship_3 = pygame.image.load("Icons/Ship_3.png").convert_alpha()
Ship_4 = pygame.image.load("Icons/Ship_4.png").convert_alpha()
Ship_5 = pygame.image.load("Icons/Ship_5.png").convert_alpha()
icon = random.choice([Ship_1,Ship_2,Ship_3,Ship_4,Ship_5])
pygame.display.set_icon(icon)
 
clock = pygame.time.Clock()
timer = 0
game = Game(SCREEN_WIDTH , SCREEN_HEIGHT, OFFSET)
mouse_pos = pygame.mouse.get_pos()
mouse_clicked = pygame.mouse.get_pressed()

main_menu = True
Instructions = False
Options = False
Music = False
Sounds = False
Spaceship = False
Credits = False
play = False
pause = False
options_button = []
pause_menu_buttons = []
end_transition = False

# Custom Events
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, game.alien_shoot_delay)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(game.lower,game.upper))

spaceships = [
        {"image": pygame.transform.scale_by(pygame.image.load("Graphics/spaceship0.png").convert_alpha(), 2.5), "name": "Yellow", "rect": pygame.Rect(0,0,150,100)},
        {"image": pygame.transform.scale_by(pygame.image.load("Graphics/spaceship1.png").convert_alpha(), 2.5), "name": "Red", "rect": pygame.Rect(0,0,150,100)},
        {"image": pygame.transform.scale_by(pygame.image.load("Graphics/spaceship2.png").convert_alpha(), 2.5), "name": "Green", "rect": pygame.Rect(0,0,150,100)},
        {"image": pygame.transform.scale_by(pygame.image.load("Graphics/spaceship3.png").convert_alpha(), 2.5), "name": "Blue", "rect": pygame.Rect(0,0,150,100)},
        ]
selected_spaceship_index = 0

credit = [
    "Space  Invaders  Project",
    "Made  with  Pygame", 
    " ",
    "Spaceship  and  Lasers  by  Apurva  and  Arkan",
    "Aliens  by  Pratik",
    "Main  Menu  by  Shashidhar",
    "UI  by  Apurva",
    "Obstacles  by  Arkan",
    "Mysteryship  by  Pratik",
    "Level  Design  by  Shashidhar",
    " ",
    " ",
    "Special Thanks to -",
    " ",
    "1. ChatGPT - For suggesting ideas for",
    "game mechanics and implementation.",
    "https://chatgpt.com/",
    " ",
    "2. Nick  Koumaris - For  his  great  tutorial  on",
    "the  Space  Invaders  game  using  Pygame,",
    "which  we  used  as  a  reference  to  build  the",
    "basic  version  of  our  game.",
    " ",
    "His  Youtube  channel - www.youtube.com/",
    "@programmingwithnick",
    " ",
    "3. Pygame  Community - For  their  documentation  and",
    "free  resources  which  were  vital  for  learning  pygame",
    "and  developing  a  more  engaging  version  of  our  game.",
    " ",
    "Documentation - https://www.pygame.org/docs/",
    "Resources - https://www.pygame.org/wiki/resources",
    " ",
    " ",
    "THE  END"
]

text_surfaces = [font_1.render(line, True, YELLOW) for line in credit]
text_positions = [((SCREEN_WIDTH + OFFSET)//2 - surface.get_width()//2 - 10,
                   (SCREEN_HEIGHT + 2 * OFFSET) + i * 50)
                   for i, surface in enumerate(text_surfaces)]

class Button:
    def __init__(self, text, x, y, width, height): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_rect = pygame.Rect(x,y,width,height)
        self.draw()
 
    def draw(self):
        hovered = self.button_hovered()
        if hovered:
            pygame.draw.rect(screen, SILVER, self.button_rect, 1, 5, 10, 10, 10, 10)
            pygame.draw.polygon(screen, SILVER,
            [(self.x -20,self.y+5), (self.x -20,self.y+26), (self.x -10,self.y+15.5)], 0)
        if self.y in (390,440,490,540):
            text_surface = font_1.render(self.text, True, SILVER)
        else:
            text_surface = font_5.render(self.text, True, SILVER)
        screen.blit(text_surface, (self.x + 5, self.y - 2))

    def button_hovered(self):
        if self.button_rect.collidepoint(mouse_pos):
             return True

    def button_clicked(self):
        global main_menu, Instructions, Options, play 
        global Music, Sounds, Spaceship, Credits, options_button
        global pause, pause_menu_buttons
        if not Instructions and not Options:
            # Main-Menu Buttons
            if buttons[0].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                channel_main.stop()
                pygame.time.delay(200)
                if game_music.play:
                    pygame.mixer.music.load("Sounds/music.ogg")
                    pygame.mixer.music.play(-1)
                main_menu = False
                play = True
            elif buttons[1].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                main_menu = False
                Options = False
                Instructions = True
            elif buttons[2].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                main_menu = False
                Instructions = False
                Options = True
                Music = False
                Sounds = False
                Spaceship = False
                Credits = False
            elif buttons[3].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                sys.exit()

        # Options Buttons
        if options_button:
            if options_button[0].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                Music = True
                
            elif options_button[1].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                Sounds = True

            elif options_button[2].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                Spaceship = True

            elif options_button[3].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                Credits = True

        # Pause Menu Buttons
        if pause_menu_buttons:
            if pause_menu_buttons[0].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                pause = False
            elif pause_menu_buttons[1].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                pause = False
                game.restart()
            elif pause_menu_buttons[2].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                pause = False
                play = False
                main_menu = True
                if game_music.play:
                    pygame.mixer.music.stop()
                if main_menu_music.play:
                    channel_main.play(main_menu_theme, -1)
            elif pause_menu_buttons[3].button_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                sys.exit()

class Button_Anim(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating_off = False
        self.is_animating_on= False
        self.sprites.append(pygame.image.load("Toggle Button/button frame 1.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 2.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 3.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 4.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 5.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 6.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 7.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 8.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 9.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 10.png").convert_alpha())
        self.sprites.append(pygame.image.load("Toggle Button/button frame 11.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft = (pos_x,pos_y))
        self.play = True
        self.pause = False

    def animate(self):
        if self.current_sprite == 0:
            self.is_animating_off = True

        elif self.current_sprite == len(self.sprites)-1:
            self.is_animating_on = True

    def update(self):
        if self.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            self.animate()
        
        if self.is_animating_off:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites)-1:
                self.current_sprite = len(self.sprites)-1
                self.is_animating_off = False
            self.image = self.sprites[self.current_sprite]
            
        elif self.is_animating_on:
            self.current_sprite -= 1
            if self.current_sprite < 0:
                self.current_sprite = 0
                self.is_animating_on = False
            self.image = self.sprites[self.current_sprite]

class Back_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Graphics/back.png")
        self.rect = self.image.get_rect(topleft = (25,25))

back_button_group = pygame.sprite.GroupSingle()

main_menu_music = Button_Anim(500,200)
game_music = Button_Anim(500,300)
credits_music = Button_Anim(500,400)

# Images and Music
bg_image = pygame.image.load("Graphics/bg.jpg").convert_alpha()
game_over_1 = pygame.transform.scale_by(pygame.image.load("Graphics/game over1.png").convert_alpha(),2.75)
game_over_2 = pygame.transform.scale_by(pygame.image.load("Graphics/game over2.png").convert_alpha(),2.75)
game_over = random.choice([game_over_1,game_over_2])
main_menu_theme = pygame.mixer.Sound("Sounds/halo theme.ogg")
credits_theme = pygame.mixer.Sound("Sounds/Autumn Memory.ogg")
channel_main = pygame.mixer.Channel(0)
channel_credits = pygame.mixer.Channel(1)
channel_main.play(main_menu_theme, -1)

# Game Loop
run = True
while run:           
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()
    screen.fill(GREY)
    dt = clock.tick(60)
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_menu_music.rect.collidepoint(mouse_pos):
                if main_menu_music.play:
                    if channel_main.get_busy:
                        channel_main.pause()
                        main_menu_music.pause = True
                else:
                    if main_menu_music.pause:
                        channel_main.unpause()
                    else:
                        if not channel_main.get_busy():
                            channel_main.play(main_menu_theme, -1)
                    main_menu_music.pause = False
                main_menu_music.play = not main_menu_music.play

            if game_music.rect.collidepoint(mouse_pos):
                game_music.play = not game_music.play

            if credits_music.rect.collidepoint(mouse_pos):
                credits_music.play = not credits_music.play

        if play:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not pause:
                    pause = True
                elif event.key == pygame.K_ESCAPE and pause:
                    pause = False

            if event.type == SHOOT_LASER and game.run and not pause:
                game.alien_shoot_laser() 

            if event.type == MYSTERYSHIP and game.run and game.aliens_group.sprites() and not pause: 
                game.create_mystery_ship()   
                pygame.time.set_timer(MYSTERYSHIP, random.randint(game.lower, game.upper))

            keys = pygame.key.get_pressed()
                    
            if keys[pygame.K_SPACE] and game.run == False and not pause:
                if game_music.play:
                    pygame.mixer.music.play(-1)    
                game.reset()

    def draw_main_menu():
        global buttons
        screen.blit(bg_image, (-350,0))
        play_button = Button("PLAY",353,390,86,31)
        instructions_button = Button("INSTRUCTIONS",278,440,240,31)
        options_button = Button("OPTIONS",325,490,145,31)
        quit_button = Button("QUIT",353,540,86,31)
        buttons = [play_button,instructions_button,options_button,quit_button]
        play_button.button_clicked()
        game_title = font_2.render(".", True, SILVER)
        screen.blit(game_title, (170,40))
        pygame.display.flip()

    def instructions():
        global Instructions, main_menu
        screen.blit(background, (0,0))
        background.fill(GREY)
        instructions_back = Back_Button()
        back_button_group.add(instructions_back)
        if instructions_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            back_button_group.remove(instructions_back)
            instructions_back.kill()
            Instructions = False
            main_menu = True
        Diamond = pygame.image.load("Graphics/Diamond.png").convert_alpha()
        pygame.draw.rect(screen, YELLOW, (10,120,780,650), 2, 0, 40, 40, 40, 40)
        with open("Instructions.txt","r") as inst:
            inst_title = inst.readline()
            inst_title_surface = font_3.render(inst_title, True, SILVER)
            inst_title_shadow = font_3.render(inst_title, True, BLACK)
            screen.blit(inst_title_shadow, (233,23))
            screen.blit(inst_title_surface,(235,20))
            y = 100
            inst_list = inst.readlines()
            screen.blit(Diamond, (35,y+57))
            screen.blit(Diamond, (35,y+206))
            screen.blit(Diamond, (35,y+407))
            screen.blit(Diamond, (35,y+608))
            for line in inst_list:
                inst_surface = font_4.render(line, True, YELLOW)
                screen.blit(inst_surface, (30,y))
                y += 50
            back_button_group.draw(screen)
        pygame.display.flip()
    
    def options():
        global Options, main_menu, options_button
        global Music, Sounds, Spaceship, Credits
        screen.blit(background, (0,0))
        background.fill(GREY)
        options_back = Back_Button()
        back_button_group.add(options_back)
        option_image = pygame.image.load("Graphics/Galaxy.png").convert_alpha()
        screen.blit(option_image, (-400,0))
        options_title = font_3.render("Options", True, SILVER)
        options_title_shadow = font_3.render("Options", True, BLACK)
        screen.blit(options_title_shadow, (273,23))
        screen.blit(options_title,(275,20))
        pygame.draw.rect(screen, BLACK, (260,360,250,300), 0, 0, 20, 20, 20, 20)
        music_button = Button("Music",320,381,120,45)
        sounds_button = Button("Sounds",306,451,142,45)
        spaceship_button = Button("Spaceship",290,521,189,45)
        credits_button = Button("Credits",305,591,140,45)
        options_button = [music_button,sounds_button,spaceship_button,credits_button]
        music_button.button_clicked()
        if options_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            back_button_group.remove(options_back)
            options_back.kill()
            Options = False
            main_menu = True
        if Music:
            music()
        if Sounds:
            sounds()
        if Spaceship:
            spaceship()
        if Credits:
            credits_()
        back_button_group.draw(screen)
        pygame.display.flip()

    def music():
        global Music, Options, moving_sprites
        screen.blit(background, (0,0))
        background.fill(GREY)
        music_back = Back_Button()
        back_button_group.add(music_back)
        if music_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            back_button_group.remove(music_back)
            music_back.kill()
            Music = False
            Options = True
        music_title = font_3.render("Music", True, SILVER)
        music_title_shadow = font_3.render("Music", True, BLACK)
        screen.blit(music_title_shadow, (303,23))
        screen.blit(music_title,(305,20))
        main_menu_music_surface = font_5.render("Main Menu Music", True, SILVER)
        game_music_surface = font_5.render("Game Music", True, SILVER)
        credits_music_surface = font_5.render("Credits Music", True, SILVER)
        screen.blit(main_menu_music_surface, (50,200))
        screen.blit(game_music_surface, (50,300))
        screen.blit(credits_music_surface, (50,400))

        moving_sprites = pygame.sprite.Group()
        moving_sprites.add(main_menu_music)
        moving_sprites.add(game_music)
        moving_sprites.add(credits_music)
        moving_sprites.draw(screen)
        moving_sprites.update()
        back_button_group.draw(screen)
        pygame.display.flip()
    
    def sounds():
        global Sounds, main_menu, Options
        screen.blit(background, (0,0))
        background.fill(GREY)
        sounds_back = Back_Button()
        back_button_group.add(sounds_back)
        if sounds_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            back_button_group.remove(sounds_back)
            sounds_back.kill()
            Sounds = False
            Options = True
        sounds_title = font_3.render("Sounds", True, SILVER)
        sounds_title_shadow = font_3.render("Sounds", True, BLACK)
        pygame.draw.rect(screen, SILVER, (50,180,700,500), 2, 0, 40, 40, 40, 40)
        screen.blit(sounds_title_shadow, (283,23))
        screen.blit(sounds_title,(285,20))
        play_sound_button = pygame.image.load("Graphics/play.png").convert_alpha()
        laser_sound = font_5.render("Laser Sound", True, SILVER)
        explosion_sound = font_5.render("Explosion Sound", True, SILVER)
        mystery_ship_sound = font_5.render("Mystery Ship Sound", True, SILVER)
        game_over_sound = font_5.render("Game Over Sound", True, SILVER)
        screen.blit(laser_sound, (120,250))
        screen.blit(explosion_sound, (120,350))
        screen.blit(mystery_ship_sound, (120,450))
        screen.blit(game_over_sound, (120,550))

        screen.blit(play_sound_button, (600,250))
        screen.blit(play_sound_button, (600,350))
        screen.blit(play_sound_button, (600,450))
        screen.blit(play_sound_button, (600,550))

        if pygame.Rect(600,250,50,50).collidepoint(mouse_pos) and mouse_clicked[0]:
            game.laser_sound.play()

        elif pygame.Rect(600,350,50,50).collidepoint(mouse_pos) and mouse_clicked[0]:
            game.exploion_sound.play()
        
        elif pygame.Rect(600,450,50,50).collidepoint(mouse_pos) and mouse_clicked[0]:
            game.mystery_ship_sound.play()

        elif pygame.Rect(600,550,50,50).collidepoint(mouse_pos) and mouse_clicked[0]:
            game.game_over_sound.play()
        back_button_group.draw(screen)
        pygame.display.flip()

    def spaceship():
        global Spaceship, Options, spaceships, selected_spaceship_index
        screen.blit(background, (0,0))
        background.fill(GREY)
        spaceship_back = Back_Button()
        back_button_group.add(spaceship_back)
        if spaceship_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            back_button_group.remove(spaceship_back)
            spaceship_back.kill()
            Spaceship = False
            Options = True
        spaceship_title = font_3.render("Spaceship", True, SILVER)
        spaceship_title_shadow = font_3.render("Spaceship", True, BLACK)
        screen.blit(spaceship_title_shadow,(273,23))
        screen.blit(spaceship_title, (275,20))
        select_spaceship = font_5.render("Select  Your  Spaceship", True, SILVER)
        screen.blit(select_spaceship, (200,200))
        for i, spaceship in enumerate(spaceships):
            if(i%2==0):
                x = 160
                y = 400 + i*125
            else:
                x = 520
                y = 400 + (i-1)*125
            spaceship["rect"] = pygame.Rect(x-20,y-10,150,100)
            if i == selected_spaceship_index:
                pygame.draw.rect(screen, SILVER, spaceship["rect"], 2)
            screen.blit(spaceship["image"], (x,y))
        
        if mouse_clicked[0]:
            for i, spaceship in enumerate(spaceships):
                if spaceship["rect"].collidepoint(mouse_pos):
                    selected_spaceship_index = i
                    game.update_spaceship(selected_spaceship_index)
        back_button_group.draw(screen)                   
        pygame.display.flip() 

    def credits_():
        global Credits, Options, text_surfaces, text_positions
        screen.blit(background, (0,0))
        background.fill(GREY)
        credits_back = Back_Button()
        back_button_group.add(credits_back)
        if credits_music.play:
            if channel_main.get_busy():
                channel_main.pause()
            if not channel_credits.get_busy():
                channel_credits.play(credits_theme, -1)
            else:
                channel_credits.unpause()
        if credits_back.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
            text_positions = [((SCREEN_WIDTH + OFFSET)//2 - surface.get_width()//2 - 10,
                   (SCREEN_HEIGHT + 2 * OFFSET) + i * 50)
                   for i, surface in enumerate(text_surfaces)]
            if channel_credits.get_busy():
                channel_credits.pause()
                if main_menu_music.play:
                    channel_main.unpause()
            back_button_group.remove(credits_back)
            credits_back.kill()
            Options = True
            Credits = False
        credits_title = font_3.render("Credits", True, SILVER)
        credits_title_shadow = font_3.render("Credits", True, BLACK)
        screen.blit(credits_title_shadow, (283,23))
        screen.blit(credits_title,(285,20))

        for i, position in enumerate(text_positions):
            text_positions[i] = (position[0], position[1] - 2)

        for surface, position in zip(text_surfaces, text_positions):
            if position[1] >= 120:
                screen.blit(surface, position)

        if all(position[1] + surface.get_height() < 120 for surface, position in zip(text_surfaces, text_positions)):
            text_positions = [((SCREEN_WIDTH + OFFSET)//2 - surface.get_width()//2 - 10,
                   (SCREEN_HEIGHT + 2 * OFFSET) + i * 50)
                   for i, surface in enumerate(text_surfaces)]
            if channel_credits.get_busy():
                channel_credits.pause()
                if main_menu_music.play:
                    channel_main.play(main_menu_theme, -1) 
            Credits = False
        back_button_group.draw(screen)
        pygame.display.flip()

    def pause_menu():
        global pause, play, pause_menu_buttons
        screen.blit(background, (0,0))
        background.fill(TRANSPARENT_GREY)
        pause_title = font_3.render("Pause Menu", True, SILVER)
        pause_title_shadow = font_3.render("Pause Menu", True, BLACK)
        screen.blit(pause_title_shadow, (243,23))
        screen.blit(pause_title, (245,20))
        pygame.draw.rect(screen, BLACK, (210,260,350,360), 0, 0, 40, 40, 40, 40)
        resume_button = Button("Resume", 305, 310, 153, 50)
        restart_button = Button("Restart", 310, 380, 140, 50)
        main_menu_button = Button("Main Menu", 275, 450, 215, 50)
        quit_button_ = Button("Quit", 335, 520, 92, 50)
        pause_menu_buttons = [resume_button, restart_button, main_menu_button, quit_button_]
        resume_button.button_clicked()
        pygame.display.flip()

    # Managing game states 
    if main_menu and not Instructions and not Options:
        draw_main_menu()

    elif Instructions:
        instructions()
        
    elif Options:
        options()

    elif play:   
        if game.run:
            if not game.aliens_group.sprites():
                if game.level<3:
                    screen.fill(GREY)
                    level_title = font_6.render(f"LEVEL - 0{game.level+1}", True, SILVER)
                    level_title_shadow = font_6.render(f"LEVEL - 0{game.level+1}", True, BLACK)
                    screen.blit(level_title_shadow, (243,353))
                    screen.blit(level_title, (245,350))
                    if not pause:
                        if not game.level_transition:
                            game.level_transition = True
                            timer = 0
                        else:
                            timer += dt
                            if timer >= 3000:
                                game.level_change()
                                game.level_transition = False
                                timer = 0    
                else:
                    if not pause:
                        pygame.mixer.music.stop()
                        victory = font_3.render("YOU WON", True, YELLOW)
                        msg = font_1.render("    Congratulations!\nYou Saved Humanity\nFrom Alien Invasion", True, YELLOW)
                        screen.blit(victory, (250,220))
                        screen.blit(msg, (250,340))
                        if not end_transition:
                            end_transition = True
                            timer = 0
                        else:
                            timer += dt
                            if timer >= 10000:
                                if main_menu_music.play:
                                    channel_main.play(main_menu_theme, -1)
                                play = False
                                main_menu = True

            if not game.level_transition:
                if not pause:
                    # Updating
                    game.spaceship_group.update() 
                    game.move_aliens(OFFSET)
                    game.alien_lasers_group.update()
                    game.mystery_ship_group.update()
                    game.check_for_collisions()

                # UI
                pygame.draw.rect(screen, YELLOW, (10,10,780,780), 2, 0, 60, 60, 60, 60)
                pygame.draw.line(screen, YELLOW, (25,730),(775,730), 3)

                level_surface = font.render(f"LEVEL 0{game.level}", True,  YELLOW)
                score_text_surface = font.render("SCORE", True, YELLOW)
                high_score_text_surface = font.render("HIGH-SCORE", True, YELLOW)

                screen.blit(level_surface, (570,740,50,50))
                x = 50
                for life in range(game.lives):
                    screen.blit(game.spaceship_group.sprite.image, (x,745))
                    x += 50

                screen.blit(score_text_surface, (50,15,50,50))
                screen.blit(high_score_text_surface, (600,15,50,50))
                formatted_score = str(game.score).zfill(5)
                formatted_high_score = str(game.highscore).zfill(5)
                score_surface = font.render(formatted_score, False, YELLOW)
                high_score_surface = font.render(formatted_high_score, False, YELLOW)
                screen.blit(score_surface, (50,40,50,50))
                screen.blit(high_score_surface, (640,40,50,50))

                # Drawing  
                game.spaceship_group.draw(screen)
                game.spaceship_group.sprite.lasers_group.draw(screen)
                game.aliens_group.draw(screen)
                game.alien_lasers_group.draw(screen)
                game.mystery_ship_group.draw(screen)
                for obstacle in game.obstacles: 
                    obstacle.blocks_group.draw(screen)
        else:
            screen.fill(GREY)
            pygame.mixer.music.stop()
            screen.blit(game_over, (-50,40))
            play_again = font_3.render("Press Space Bar To Play Again", True, SILVER)
            screen.blit(play_again, (25,710))
    if pause:
        pause_menu()
    pygame.display.flip()
pygame.quit()
        
