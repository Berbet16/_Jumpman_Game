import pygame
import random
import time
import sys

pygame.init()
pygame.font.init()

# RENKLER
white = (255, 255, 255)
red = (156, 19, 19)
blue = ((48, 95, 156))

# ANİMASYON RESİMLERİNİN YÜKLENMESİ
idle_left = [pygame.image.load("./animation/idle/left/idle-left-1.png"), pygame.image.load("./animation/idle/left/idle-left-2.png"), pygame.image.load("./animation/idle/left/idle-left-3.png"), pygame.image.load("./animation/idle/left/idle-left-4.png")]
idle_right = [pygame.image.load("./animation/idle/right/idle-right-1.png"), pygame.image.load("./animation/idle/right/idle-right-2.png"), pygame.image.load("./animation/idle/right/idle-right-3.png"), pygame.image.load("./animation/idle/right/idle-right-4.png")]
run_left = [pygame.image.load("./animation/run/left/run-left-1.png"), pygame.image.load("./animation/run/left/run-left-2.png"), pygame.image.load("./animation/run/left/run-left-3.png"), pygame.image.load("./animation/run/left/run-left-4.png")]
run_right = [pygame.image.load("./animation/run/right/run-right-1.png"), pygame.image.load("./animation/run/right/run-right-2.png"), pygame.image.load("./animation/run/right/run-right-3.png"), pygame.image.load("./animation/run/right/run-right-4.png")]
climb = [pygame.image.load("./animation/climb/climb-1.png"), pygame.image.load("./animation/climb/climb-2.png"), pygame.image.load("./animation/climb/climb-3.png"), pygame.image.load("./animation/climb/climb-4.png")]
climb_rope = [pygame.image.load("./animation/climb/climb-rope-1.png"), pygame.image.load("./animation/climb/climb-rope-2.png"), pygame.image.load("./animation/climb/climb-rope-3.png"), pygame.image.load("./animation/climb/climb-rope-4.png")]

player = None

enemy_1 = None
enemy_2 = None
enemy_3 = None

ended_at = None

# GAME CLASS
class Game():
    def __init__(self):
        self.caption = "Jumpman"

        self.started_at = None

        self.screen_width = 1000
        self.screen_height = 700

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()

        self.gravity = False

        self.play_big = pygame.font.Font("./fonts/Play/Play-Regular.ttf", 60)
        self.play_normal = pygame.font.Font("./fonts/Play/Play-Regular.ttf", 45)

        self.game_modes = ["EASY", "MEDIUM", "HARD"]
        self.default_game_mode = self.game_modes[0]
        self.game_mode = self.default_game_mode

        self.grounds = [pygame.Rect(0, 670, 1000, 30), pygame.Rect(400, 640, 200, 30), pygame.Rect(0, 500, 200, 30), pygame.Rect(800, 500, 200, 30), pygame.Rect(175, 470, 650, 30), pygame.Rect(0, 340, 111, 30), pygame.Rect(889, 340, 111, 30), pygame.Rect(334, 300, 332, 30), pygame.Rect(0, 200, 200, 30), pygame.Rect(800, 200, 200, 30), pygame.Rect(334, 150, 332, 30)]
        self.stairs = [pygame.Rect(115, 470, 62, 120), pygame.Rect(825, 470, 62, 120), pygame.Rect(340, 270, 62, 120), pygame.Rect(600, 270, 62, 120), pygame.Rect(470, 100, 62, 120)]
        self.bombs = [pygame.Rect(50, 630, 25, 25), pygame.Rect(925, 630, 25, 25), pygame.Rect(50, 300, 25, 25), pygame.Rect(925, 300, 25, 25), pygame.Rect(150, 150, 25, 25), pygame.Rect(825, 150, 25, 25), pygame.Rect(350, 100, 25, 25), pygame.Rect(625, 100, 25, 25)]
        self.ropes = [pygame.Rect(20, 370, 18, 90), pygame.Rect(962, 370, 18, 90)]

        self.bomb_image = pygame.image.load("./assets/bomb.png")
        self.heart_image = pygame.image.load("./assets/heart.png")

        self.map = pygame.image.load("./assets/map.png")

        self.animation_controller = 0

        self.started = False
        self.over = False

        self.current_ground = None

        self.score = 0

    # OYUN DEĞERLERİNİN EN BAŞTAKİ HALE GETİRİLMESİ
    def reset_game(self):
        self.bombs = [pygame.Rect(50, 300, 25, 25), pygame.Rect(925, 300, 25, 25), pygame.Rect(150, 150, 25, 25), pygame.Rect(825, 150, 25, 25), pygame.Rect(350, 100, 25, 25), pygame.Rect(625, 100, 25, 25)]
        self.default_game_mode = self.game_modes[0]
        player.hearts = 3

    # OYUN BAŞLANGIÇ MENÜSÜ
    def display_menu(self, event):
        if self.started == False and self.over == False:
            self.game_mode_1 = pygame.image.load("./assets/easy.png")
            self.game_mode_2 = pygame.image.load("./assets/medium.png")
            self.game_mode_3 = pygame.image.load("./assets/hard.png")

            self.screen.fill((0, 0, 0))

            if self.game_mode == self.game_modes[0]:
                self.screen.blit(self.game_mode_1, (0, 0))

            elif self.game_mode == self.game_modes[1]:
                self.screen.blit(self.game_mode_2, (0, 0))

            elif self.game_mode == self.game_modes[2]:
                self.screen.blit(self.game_mode_3, (0, 0))

            pygame.display.update() 

            if event.type == pygame.KEYDOWN and not game.started: 
                if event.key == pygame.K_DOWN:
                    if self.game_mode == self.game_modes[0]:
                        self.game_mode = self.game_modes[1]

                    elif self.game_mode == self.game_modes[1]:
                        self.game_mode = self.game_modes[2]  

                if event.key == pygame.K_UP:
                    if self.game_mode == self.game_modes[2]:
                        self.game_mode = self.game_modes[1]

                    elif self.game_mode == self.game_modes[1]:
                        self.game_mode = self.game_modes[0] 

                if event.key == pygame.K_RETURN:
                    game.started = True 
                    self.started_at = time.time() 

    # "GAME OVER" MENÜSÜ
    def display_game_over(self, event):
        if self.over:
            self.started = False
            self.play_again_screen = pygame.image.load("./assets/play-again.png")

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.play_again_screen, (0, 0))

            self.score_text = self.play_big.render('Skor: ' + str(self.score), False, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 0))

            self.time_text = self.play_big.render("Süre: " + str(self.seconds), False, (255, 255, 255))
            self.screen.blit(self.time_text, (10, 100))

            pygame.display.update() 

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    self.reset_game()

                    self.over = False
                    self.started = False

    # EKRANA ÇİZİLMESİ GEREKEN HER ŞEYİN ÇİZİLMESİ
    def draw(self):
        self.screen.fill((0, 0, 0))

        for ground in self.grounds:
            pygame.draw.rect(self.screen, (0, 0, 0), ground)

        for stair in self.stairs:
            pygame.draw.rect(self.screen, (0, 0, 0), stair)

        for rope in self.ropes:
            pygame.draw.rect(self.screen, (0, 0, 0), rope)

        self.screen.blit(self.map, (0, 0))

        for bomb in self.bombs:
            self.screen.blit(self.bomb_image, bomb)

        for i in range(1, player.hearts + 1):
            self.screen.blit(self.heart_image, (1000 - i * 50, 20))

        player.animate()

        enemy_1.display()
        enemy_1.move()
        enemy_1.check_collision()

        enemy_2.display()
        enemy_2.move()
        enemy_2.check_collision()

        if self.game_mode == self.game_modes[1] or self.game_mode == self.game_modes[2]:
            enemy_3.display()
            enemy_3.move()
            enemy_3.check_collision()                      

        pygame.display.update()          

    # OYUNUN BİTİP BİTMEDİĞİNİN KONTROLÜ
    def check_game_over(self):
        global player

        global enemy_1
        global enemy_2
        global enemy_3

        if self.started == True:
            if len(self.bombs) == 0 or player.hearts == 0:
                self.ended_at = time.time()
                self.seconds = int(self.ended_at - self.started_at)

                if len(self.bombs) < 6:
                    self.score = (60 - int(self.seconds)) + (6 - len(self.bombs)) * 20

                elif player.hearts == 0:
                    self.score = 0

                self.over = True
                self.started = False

                player = Player(game.screen_width / 2  - idle_right[0].get_width() / 2, game.screen_height - idle_right[0].get_height() - 75)

                enemy_1 = Enemy1()
                enemy_2 = Enemy1()
                enemy_3 = Enemy2(0, 630)

game = Game()

# PLAYER CLASS
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = idle_right[0].get_width()
        self.height = idle_right[0].get_height()

        self.velocity = 5
        self.mass = 1

        self.direction = "right"

        self.jump = False
        self.jump_count = 10

        self.climb_up = False
        self.climb_down = False
        
        self.rope_climb = False

        self.climb_count = 0

        self.current_stair = None
        self.current_rope = None

        self.left = False
        self.right = False

        self.jump_count = 4

        self.animation_counter = 0
        self.idle_counter = 0
        self.jump_counter = 0

        self.player_rect = None

        self.hearts = 3

        self.grounds_down = []

    # YATAY ÇARPIŞMANIN KONTROL EDİLMESİ (SOL / SAĞ)
    def check_horizontal_collision(self, player, grounds):
        if player != None:
            player_x = player.x
            player_width = player.width

            for ground in grounds:
                if player.colliderect(ground):
                    if ground.x + ground.width + self.player_rect.width >= player_x >= ground.x + ground.width - self.player_rect.width:
                        return 'collide-right'

                    if ground.x - self.player_rect.width <= player_x + player_width <= ground.x + self.player_rect.width:
                        return 'collide-left'

    # YERÇEKİMİNİN KONTROL EDİLMESİ
    def gravity_control(self):
        if self.player_rect != None:
            self.grounds_down = []

            for ground in game.grounds:
                if self.player_rect.x + self.player_rect.width >= ground.x and self.player_rect.x <= ground.x + ground.width:
                        if self.player_rect.y + self.height <= ground.y and len(self.grounds_down) < 5:
                            self.grounds_down.append(ground)

            if len(self.grounds_down) > 0:
                if self.grounds_down[-1].y > self.player_rect.y + self.height:
                    self.player_rect.y += self.velocity

    # BOMBANIN DOKUNULDUĞUNDA YOK OLMASI
    def destroy_bomb(self):
        if self.player_rect != None:    
            for bomb in game.bombs:
                if self.player_rect.colliderect(bomb) and self.player_rect.y <= bomb.y:
                    game.bombs.remove(bomb)

    # ANİMASYONLARIN YAPILMASI
    def animate(self):
        if self.jump:
            self.y -= (self.jump_count * abs(self.jump_count)) * 4     
            self.jump_count -= 2    

            if self.jump_count < 0:
                self.jump = False
                self.jump_count = 4

        if self.climb_up or self.climb_down or self.rope_climb:
            if self.climb_up:
                if self.climb_count < 3 and self.player_rect.y > self.current_stair.y + 30:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_rect = climb[self.climb_count].get_rect(x=self.x, y=self.y)
                game.screen.blit(climb[self.climb_count], self.player_rect)

            elif self.climb_down:
                if self.climb_count < 3:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_rect = climb[self.climb_count].get_rect(x=self.x, y=self.y)
                game.screen.blit(climb[self.climb_count], self.player_rect)

            elif self.rope_climb:
                if self.climb_count < 3:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_rect = climb_rope[self.climb_count].get_rect(x=self.x, y=self.y)
                game.screen.blit(climb_rope[self.climb_count], self.player_rect)   

            else:
                self.climb_up = False
                self.climb_down = False
                self.rope_climb = False             

        elif self.left:
            self.direction = "left"
            self.player_rect = run_left[self.animation_counter].get_rect(x=self.x, y=self.y)
            game.screen.blit(run_left[self.animation_counter], self.player_rect)

        elif self.right:
            self.direction = "right"
            self.player_rect = run_right[self.animation_counter].get_rect(x=self.x, y=self.y)
            game.screen.blit(run_right[self.animation_counter], (self.x, self.y))

        else:
            if self.direction == "left":
                self.player_rect = idle_left[self.idle_counter].get_rect(x=self.x, y=self.y)
                game.screen.blit(idle_left[self.idle_counter], self.player_rect)

            elif self.direction == "right":
                self.player_rect = idle_right[self.idle_counter].get_rect(x=self.x, y=self.y)
                game.screen.blit(idle_right[self.idle_counter], self.player_rect)

            self.idle_counter += 1

# ENEMY CLASS
class Enemy1():
    def __init__(self):
        self.random_x_array = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        self.random_y_array = [100, 200, 300, 400, 500, 600]

        self.directions = ["horizontal", "vertical"]
        self.direction = "horizontal"

        self.x = random.choice(self.random_x_array)
        self.y = 0

        self.velocity = 15

        self.enemy_rect = pygame.Rect(self.x, self.y, 15, 15)

    # DÜŞMANIN BAŞLANGIÇ HALİNE GETİRİLMESİ
    def reset_enemy(self):
        self.enemy_rect = pygame.Rect(self.x, self.y, 15, 15)

    # DÜŞMANIN HAREKET ETTİRİLMESİ
    def move(self):
        if self.enemy_rect.x >= game.screen_width or self.enemy_rect.y >= game.screen_height:
            self.direction = random.choice(self.directions)

            if self.direction == "horizontal":
                self.enemy_rect.y = 0
                self.enemy_rect.x = random.choice(self.random_y_array)

            else:
                self.enemy_rect.x = 0
                self.enemy_rect.y = random.choice(self.random_x_array)

        else:
            if self.direction == "horizontal":
                self.enemy_rect.y += self.velocity

            else:
                self.enemy_rect.x += self.velocity

    # DÜŞMANLA ÇARPIŞMANIN KONTROL EDİLMESİ
    def check_collision(self):
        if player.player_rect.colliderect(self.enemy_rect):
            self.reset_enemy()
            player.hearts -= 1

    # DÜŞMANIN EKRANDA GÖSTERİLMESİ        
    def display(self):
        pygame.draw.circle(game.screen, (255, 255, 255), (self.enemy_rect.x, self.enemy_rect.y), 15, 15)

# ENEMY CLASS 2
class Enemy2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.velocity = 15

        self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)

    # DÜŞMANIN BAŞLANGIÇ HALİNE GETİRİLMESİ    
    def reset_enemy(self):
        self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)

    # DÜŞMANLA ÇARPIŞMANIN KONTROL EDİLMESİ
    def check_collision(self):
        if player.player_rect.colliderect(self.enemy_rect):
            self.reset_enemy()
            player.hearts -= 1

    # DÜŞMANIN EKRANDA GÖSTERİLMESİ 
    def display(self):
        pygame.draw.circle(game.screen, (255, 0, 0), (self.enemy_rect.x, self.enemy_rect.y), 20, 20)

    # DÜŞMANIN HAREKET ETTİRİLMESİ
    def move(self):
        # HARD
        if game.game_mode == "HARD":
            self.velocity = 25

        # MEDIUM AND HARD
        if self.enemy_rect.x < game.screen_width - self.enemy_rect.width:
            self.enemy_rect.x += self.velocity

        else:
            self.enemy_rect.x = 0


# CREATING THE PLAYER
player = Player(game.screen_width / 2  - idle_right[0].get_width() / 2, game.screen_height - idle_right[0].get_height() - 75)

enemy_1 = Enemy1()
enemy_2 = Enemy1()
enemy_3 = Enemy2(0, 630)

while True:
    # GRAVITY
    player.gravity_control()

    game.animation_controller += 1

    if player.player_rect != None:
        player.x = player.player_rect.x
        player.y = player.player_rect.y

    for event in pygame.event.get():
        # QUIT
        if event.type == pygame.QUIT: 
            sys.exit()

        # MENU
        game.display_menu(event)

        # GAME OVER
        game.display_game_over(event)

    # RUN
    if game.started: 
        keys = pygame.key.get_pressed()

        if player.player_rect != None and player.climb_up == False and player.climb_down == False:
            if keys[pygame.K_LEFT] and player.player_rect.x > 0 + player.velocity and player.check_horizontal_collision(player.player_rect, game.grounds) != "collide-right":
                player.player_rect.x -= player.velocity
                player.left = True
                player.right = False

                if game.animation_controller % 6 == 0:
                    player.animation_counter += 1

                    if player.animation_counter >= len(run_right):
                        player.animation_counter = 0

                    game.animation_controller = 0
                    
            elif keys[pygame.K_RIGHT] and player.player_rect.x + player.width < game.screen_width and player.check_horizontal_collision(player.player_rect, game.grounds) != "collide-left":
                player.player_rect.x += player.velocity
                player.right = True
                player.left = False

                if game.animation_controller % 6 == 0:
                    player.animation_counter += 1

                    if player.animation_counter >= len(run_right):
                        player.animation_counter = 0

                    game.animation_controller = 0

            else:
                player.right = False
                player.left = False

                player.animation_counter = 0

                if player.animation_counter % 6 == 0:
                    if player.idle_counter >= len(idle_right):
                        player.idle_counter = 0

        # CLIMB AND JUMP
        if keys[pygame.K_UP]:
            if player.player_rect != None and player.player_rect.collidelist(game.stairs) != -1:
                for stair in game.stairs:
                    if player.player_rect.colliderect(stair):
                        player.current_stair = stair
                        player.climb_up = True 

                        break

                if player.climb_up:
                    player.player_rect.centerx = player.current_stair.centerx
                    player.player_rect.y -= player.velocity * 2 

            elif player.player_rect != None and player.player_rect.collidelist(game.ropes) != -1:
                for rope in game.ropes:
                    if player.player_rect.colliderect(rope):
                        player.current_rope = rope
                        player.rope_climb = True 

                        break

                if player.rope_climb:
                    player.player_rect.centerx = player.current_rope.x
                    player.player_rect.y -= player.velocity * 2                 

            else:
                player.rope_climb = False
                player.climb_up = False
                player.jump = True            

        elif keys[pygame.K_DOWN]:
            if player.player_rect != None and player.player_rect.collidelist(game.stairs) != -1:
                for stair in game.stairs:
                    if player.player_rect.colliderect(stair):
                        player.current_stair = stair
                        player.climb_down = True 

                        break

                if player.current_stair.y + player.current_stair.height > player.player_rect.y + player.height and player.climb_down and len(player.grounds_down) > 0:
                    player.player_rect.centerx = player.current_stair.centerx
                    player.player_rect.y += player.velocity

                else:
                    player.climb_down = False

            else:
                player.climb_down = False

        else:
            player.climb_up = False
            player.climb_down = False
            player.rope_climb = False

        # DESTROYING THE BOMB
        player.destroy_bomb()

        # DRAW
        if game.animation_controller % 6 == 0:
            game.draw()    

    game.check_game_over() 

    game.clock.tick(60)