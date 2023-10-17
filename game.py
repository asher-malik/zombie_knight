import pygame
import random
import sys

vector = pygame.math.Vector2

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
FPS = 60
night = 1
num = 0

class Game:
    def __init__(self, portal_group, player, bullet_group, main_group, zombie_group, ruby_group):
        self.portal_group = portal_group
        self.player = player
        self.bullet_group = bullet_group
        self.main_group = main_group
        self.zombie_group = zombie_group
        self.ruby_group = ruby_group

        self.STARTING_HEALTH = 100

        self.score = 0
        self.health = self.STARTING_HEALTH
        self.night = 1
        self.time = 30

        self.game_time = 0

        self.level_music = pygame.mixer.music.load("sounds/level_music.wav")

        self.zombie_hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
        self.zombie_kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("sounds/ruby_pickup.wav")
        self.ruby_lost_sound = pygame.mixer.Sound("sounds/lost_ruby.wav")

        self.sub_font = pygame.font.Font("fonts/Pixel.ttf", 20)
        self.main_font = pygame.font.Font("fonts/Poultrygeist.ttf", 64)


    def update(self):
        global num
        if num == 1:
            pygame.mixer.music.play(-1)
        self.game_over()
        self.new_round()
        self.game_time += 1
        if self.game_time % 60 == 0:
            self.time -= 1
        self.draw()
        self.check_collisions()
        self.generate_zombies()
        num += 1

    def draw(self):
        self.score_text = self.sub_font.render(f"Score: {self.score}", True, "white")
        self.score_rect = self.score_text.get_rect()
        self.score_rect.topleft = (10, 685)

        self.health_text = self.sub_font.render(f"Health: {self.health}", True, "white")
        self.health_rect = self.health_text.get_rect()
        self.health_rect.topleft = (10, 710)

        self.night_text = self.sub_font.render(f"Night: {self.night}", True, "white")
        self.night_rect = self.night_text.get_rect()
        self.night_rect.topright = (WINDOW_WIDTH - 10, 685)

        self.sunrise_text = self.sub_font.render(f"Sunrise in: {self.time}", True, "white")
        self.sunrise_rect = self.sunrise_text.get_rect()
        self.sunrise_rect.topright = (WINDOW_WIDTH - 10, 710)

        self.zombie_knight_text = self.main_font.render("Zombie Knight", True, (46,139,87))
        self.zombie_knight_rect = self.zombie_knight_text.get_rect()
        self.zombie_knight_rect.topleft = (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT - 70)

        screen.blit(self.score_text, self.score_rect)
        screen.blit(self.health_text, self.health_rect)
        screen.blit(self.night_text, self.night_rect)
        screen.blit(self.sunrise_text, self.sunrise_rect)
        screen.blit(self.zombie_knight_text, self.zombie_knight_rect)

    def check_collisions(self):
        collided_portal = pygame.sprite.spritecollide(self.player, self.portal_group, False, pygame.sprite.collide_mask)
        collision_bullet_zombie = pygame.sprite.groupcollide(self.zombie_group, self.bullet_group, False, True)
        collided_zombie = pygame.sprite.spritecollide(self.player, self.zombie_group, False, pygame.sprite.collide_mask)
        collided_ruby = pygame.sprite.spritecollide(self.player, self.ruby_group, True, pygame.sprite.collide_mask)
        collided_zombie_ruby = pygame.sprite.groupcollide(self.zombie_group, self.ruby_group, False, True)
        collided_zombie_portal = pygame.sprite.groupcollide(self.zombie_group, self.portal_group, False, False, pygame.sprite.collide_mask)
        collided_ruby_portal = pygame.sprite.groupcollide(self.ruby_group, self.portal_group, False, False, pygame.sprite.collide_mask)

        if collided_ruby_portal:
            for portal in collided_ruby_portal.values():
                if portal[0].color == "green":
                    if portal[0].rect.y > 300:
                        self.portal_sound.play()
                        for portal in collided_ruby_portal.keys():
                            portal.position = vector(100, 46)
                    else:
                        self.portal_sound.play()
                        for portal in collided_ruby_portal.keys():
                            portal.position = vector(1190, 618)
                elif portal[0].color == "purple":
                    if portal[0].rect.y > 300:
                        self.portal_sound.play()
                        for portal in collided_ruby_portal.keys():
                            portal.position = vector(1190, 54)
                    else:
                        self.portal_sound.play()
                        for portal in collided_ruby_portal.keys():
                            portal.position = vector(100, 614)


        if collided_zombie_portal:
            for portal in collided_zombie_portal.values():
                if portal[0].color == "green":
                    if portal[0].rect.y > 300:
                        self.portal_sound.play()
                        for zombie in collided_zombie_portal.keys():
                            zombie.position = vector(100, 46)
                    else:
                        self.portal_sound.play()
                        for zombie in collided_zombie_portal.keys():
                            zombie.position = vector(1190, 618)
                elif portal[0].color == "purple":
                    if portal[0].rect.y > 300:
                        self.portal_sound.play()
                        for zombie in collided_zombie_portal.keys():
                            zombie.position = vector(1190, 54)
                    else:
                        self.portal_sound.play()
                        for zombie in collided_zombie_portal.keys():
                            zombie.position = vector(100, 614)

        if collided_zombie_ruby:
            zombie = Zombie(self.main_group)
            self.ruby_lost_sound.play()
            my_zombie_group.add(zombie)
        if collided_ruby:
            self.score += 125*self.night
            if self.health < 100:
               self.health += 10
            else:
                self.health = 100
            self.ruby_pickup_sound.play()
        if collided_portal:
            if collided_portal[0].color == "green":
                if collided_portal[0].rect.y < 300:
                    self.portal_sound.play()
                    self.player.position = vector(1174, 618)
                else:
                    self.portal_sound.play()
                    self.player.position = vector(72, 46)
            elif collided_portal[0].color == "purple":
                if collided_portal[0].rect.y < 300:
                    self.portal_sound.play()
                    self.player.position = vector(76, 614)
                else:
                    self.portal_sound.play()
                    self.player.position = vector(1187, 54)
        if collision_bullet_zombie:
            for zombie in collision_bullet_zombie.keys():
                if not zombie.is_dead:
                    zombie.is_dead = True
                    zombie.current_sprite = 0
            self.zombie_hit_sound.play()
        if collided_zombie:
            if collided_zombie[0].is_dead:
                collided_zombie[0].kill()
                self.zombie_kick_sound.play()
                ruby = Ruby(self.main_group)
                self.ruby_group.add(ruby)
                self.score += 25*self.night
            else:
                self.player_hit_sound.play()
                self.health -= 20
                if self.player.velocity.x > 0:
                    self.player.position.x -= 200
                elif self.player.velocity.x < 0:
                    self.player.position.x += 200
                self.player.rect.topleft = self.player.position

        self.player.rect.topleft = self.player.position

    def pregame_screen(self):
        global run, running
        pygame.mixer.music.pause()
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False
                        run = True
                        pygame.mixer.music.unpause()
            screen.fill("black")
            zombie_knight_text = self.main_font.render("Zombie Knight", True, (46,139,87))
            zombie_knight_rect = zombie_knight_text.get_rect()
            zombie_knight_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 32)

            play_text = self.main_font.render("Press 'Enter' to play", True, "white")
            play_rect = play_text.get_rect()
            play_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 45)

            screen.blit(zombie_knight_text, zombie_knight_rect)
            screen.blit(play_text, play_rect)

            pygame.display.flip()

    def game_over(self):
        global night
        if self.health <= 0:
            self.pause_game(f"Game Over final score: {self.score}", "Press 'Enter' to play again")
            pygame.mixer.music.unpause()
            self.ruby_group.empty()
            self.zombie_group.empty()
            self.bullet_group.empty()
            self.health = 100
            self.score = 0
            self.night = 1
            night = 1
            self.time = 30
            self.player.position = vector(622, 523)
            self.player.velocity = vector(0, 0)
            self.player.rect.topleft = self.player.position
            self.game_time = 0


    def pause_game(self, text1, text2):
        global running
        pause = True
        pygame.mixer.music.pause()
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False
            screen.fill("black")
            main_text = self.main_font.render(text1, True, (46,139,87))
            main_text_rect = main_text.get_rect()
            main_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60)

            sub_text = self.main_font.render(text2, True, "white")
            sub_rect = sub_text.get_rect()
            sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

            screen.blit(main_text, main_text_rect)
            screen.blit(sub_text, sub_rect)

            pygame.display.flip()

    def generate_zombies(self):
        if self.night < 6:
            if self.game_time % (360 - 60*self.night) == 0:
                zombie = Zombie(self.main_group)
                self.game_time = 0
                my_zombie_group.add(zombie)
        else:
            if self.game_time % 60 == 0:
                zombie = Zombie(self.main_group)
                self.game_time = 0
                my_zombie_group.add(zombie)

    def new_round(self):
        global night
        if self.time <= 0:
            self.pause_game("You survived the night!", "Press 'Enter' to continue...")
            self.game_time = 0
            self.time = 30
            self.night += 1
            self.player.position = vector(622, 523)
            self.player.velocity = vector(0, 0)
            self.player.rect.topleft = self.player.position
            pygame.mixer.music.unpause()
            self.zombie_group.empty()
            self.bullet_group.empty()
            self.ruby_group.empty()
            night += 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, main_group, ruby_maker_group):
        super(Player, self).__init__()
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.fire_right_sprites = []
        self.fire_left_sprites = []

        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (1).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (2).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (3).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (4).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (5).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (6).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (7).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (8).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (9).png"), (64, 64)))
        self.move_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/run/Run (10).png"), (64, 64)))
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (1).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (2).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (3).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (4).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (5).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (6).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (7).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (8).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (9).png"), (64, 64)))
        self.idle_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/idle/Idle (10).png"), (64, 64)))
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (1).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (2).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (3).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (4).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (5).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (6).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (7).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (8).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (9).png"), (64, 64)))
        self.jump_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/jump/Jump (10).png"), (64, 64)))
        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.fire_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (1).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (2).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (3).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (4).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (5).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (6).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (7).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (8).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (9).png"), (64, 64)))
        self.fire_right_sprites.append(
            pygame.transform.scale(pygame.image.load("images/player/attack/Attack (10).png"), (64, 64)))
        for sprite in self.fire_right_sprites:
            self.fire_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.is_jumping = False
        self.is_shooting = False

        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav")

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.ruby_maker_group = ruby_maker_group

        self.HORIZONTAL_ACCELERATION = 2.4
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.9
        self.VERTICAL_JUMP_SPEED = 18

        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.rect.topleft = self.position

        self.main_group = main_group

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.move()
        self.check_collisions()
        self.check_animations()

    def move(self):
        keys = pygame.key.get_pressed()
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, 0.5)
        elif keys[pygame.K_LEFT]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.2)
            else:
                self.animate(self.idle_left_sprites, 0.2)
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x >= WINDOW_WIDTH:
            self.position.x = 0
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += 0.5*self.acceleration + self.velocity

        self.rect.topleft = self.position

    def check_collisions(self):
        collided_platform = pygame.sprite.spritecollide(self, self.main_group, False, pygame.sprite.collide_mask)
        if self.velocity.y > 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top - 60
                self.velocity.y = 0
        elif self.velocity.y < 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top + 15
                self.velocity.y *= -1

        collided_ruby = pygame.sprite.spritecollide(self, self.ruby_maker_group, False, pygame.sprite.collide_mask)
        if self.velocity.y > 0:
            if collided_ruby:
                self.position.y = collided_ruby[0].rect.top - 60
                self.velocity.y = 0
                self.is_jumping = False
        elif self.velocity.y < 0:
            if collided_ruby:
                self.position.y = collided_ruby[0].rect.top + 40
                self.velocity.y *= -1

        self.rect.topleft = self.position

    def jump(self):
        collided_platform = pygame.sprite.spritecollide(self, self.main_group, False)
        if collided_platform:
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED
            self.is_jumping = True

    def shoot(self):
        self.is_shooting = True

    def check_animations(self):
        if self.is_jumping:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, 0.5)
                collided_platform = pygame.sprite.spritecollide(self, self.main_group, False)
                if collided_platform:
                   self.is_jumping = False
            else:
                self.animate(self.jump_left_sprites, 0.5)
                collided_platform = pygame.sprite.spritecollide(self, self.main_group, False)
                if collided_platform:
                    self.is_jumping = False
        elif self.is_shooting:
            if self.velocity.x > 0:
                self.animate(self.fire_right_sprites, 0.2)
                self.is_shooting = False
            elif self.velocity.x < 0:
                self.animate(self.fire_left_sprites, 0.2)
                self.is_shooting = False


    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]
        self.rect.topleft = self.position

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, num, main_group):
        super(Tile, self).__init__()
        if num == 1:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (1).png"), (32, 32))
        elif num == 2:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (2).png"), (32, 32))
        elif num == 3:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (3).png"), (32, 32))
        elif num == 4:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (4).png"), (32, 32))
        elif num == 5:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (5).png"), (32, 32))
        main_group.add(self)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Portal, self).__init__()
        self.portal_right_sprites = []
        self.color = color
        if self.color == "green":
            self.portal_right_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile000.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile001.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile002.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile003.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile004.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile005.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile006.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile007.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile008.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile009.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile010.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile011.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile012.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile013.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile014.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile015.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile016.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile017.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile018.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile019.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile020.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile021.png"), (120, 120)))

            self.current_sprite = random.randint(0, 21)
            self.image = self.portal_right_sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        if self.color == "purple":
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile000.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile001.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile002.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile003.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile004.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile005.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile006.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile007.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile008.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile009.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile010.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile011.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile012.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile013.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile014.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile015.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile016.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile017.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile018.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile019.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile020.png"), (120, 120)))
            self.portal_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/purple/tile021.png"), (120, 120)))

            self.current_sprite = random.randint(0, 21)
            self.image = self.portal_right_sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    def update(self):
        self.animate(self.portal_right_sprites, 0.5)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Bullet, self).__init__()
        self.player = player
        if self.player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"), (32, 32))
            self.rect = self.image.get_rect()
            self.speed = 16
            self.rect.center = (self.player.rect.x, self.player.rect.y + 25)
            self.start_x = self.player.rect.x
        elif self.player.velocity.x <= 0:
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/player/slash.png"), (32, 32)), True, False)
            self.rect = self.image.get_rect()
            self.speed = -16
            self.rect.center = (self.player.rect.x, self.player.rect.y + 25)
            self.start_x = self.player.rect.x

    def update(self):
        self.rect.x += self.speed
        self.destroy_bullet()

    def destroy_bullet(self):
        self.current_rect = self.player.rect.x

        if self.rect.right > WINDOW_WIDTH or self.rect.left < 0:
            self.kill()
        if abs(self.current_rect + 350) < abs(self.rect.x):
            self.kill()
        elif self.current_rect - 350 > abs(self.rect.x):
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, main_group):
        super(Zombie, self).__init__()
        self.num = random.randint(0, 1)

        self.move_right_sprites = []
        self.move_left_sprites = []
        self.dead_right_sprites = []
        self.dead_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        if self.num == 0:
            self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (1).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (2).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (3).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (4).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (5).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (6).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (7).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (8).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (9).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (10).png"), (64, 64)))
            for sprite in self.move_right_sprites:
                self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.dead_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"), (64, 64)))
            for sprite in self.dead_right_sprites:
                self.dead_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"), (64, 64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        else:
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (1).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (2).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (3).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (4).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (5).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (6).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (7).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (8).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (9).png"), (64, 64)))
            self.move_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (10).png"), (64, 64)))
            for sprite in self.move_right_sprites:
                self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"), (64, 64)))
            self.dead_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"), (64, 64)))
            for sprite in self.dead_right_sprites:
                self.dead_left_sprites.append(pygame.transform.flip(sprite, True, False))

            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"), (64, 64)))
            self.rise_right_sprites.append(
                pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"), (64, 64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.main_group = main_group

        self.starting_y = -120
        self.starting_x = random.randint(0, WINDOW_WIDTH)

        self.direction = random.choice([-1, 1])

        self.speed = random.randint(night, night + 10)

        self.HORIZONTAL_VELOCITY = self.speed*self.direction
        self.VERTICAL_ACCELERATION = 0.7

        self.position = vector(self.starting_x, self.starting_y)
        self.velocity = vector(self.HORIZONTAL_VELOCITY, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        self.current_sprite = 0
        if self.direction == -1:
            self.image = self.move_left_sprites[self.current_sprite]
        else:
            self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.time = 0
        self.is_dead = False

    def revive(self):
        if self.is_dead:
            self.time += 1
            if self.time % 120 == 0:
                self.time = 0
                if self.velocity.x > 0:
                    self.animate(self.rise_right_sprites, 0.1)
                elif self.velocity.x < 0:
                    self.animate(self.rise_left_sprites, 0.1)
                self.is_dead = False

    def update(self):
        self.revive()
        self.mask = pygame.mask.from_surface(self.image)
        self.move()
        self.check_collisions()
        if self.current_sprite != 9:
            self.check_animations()

    def move(self):
        if self.is_dead != True:
            self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
            self.velocity.y += self.acceleration.y
            self.position += 0.5*self.acceleration + self.velocity

            if self.velocity.x < 0:
                self.animate(self.move_left_sprites, 0.5)
            elif self.velocity.x > 0:
                self.animate(self.move_right_sprites, 0.5)

            if self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = WINDOW_WIDTH

            self.rect.topleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]

    def check_collisions(self):
        collided_platform = pygame.sprite.spritecollide(self, self.main_group, False, pygame.sprite.collide_mask)
        if self.velocity.y > 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top - 60
                self.velocity.y = 0
        elif self.velocity.y < 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top + 15
                self.velocity.y *= -1

        self.rect.topleft = self.position

    def check_animations(self):
        if self.is_dead:
            if self.velocity.x > 0:
                self.animate(self.dead_right_sprites, 1)
            elif self.velocity.x < 0:
                self.animate(self.dead_left_sprites, 1)

class Ruby(pygame.sprite.Sprite):
    def __init__(self, main_group):
        super(Ruby, self).__init__()
        self.image_sprites = []
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"), (64, 64)))

        self.current_sprite = 0
        self.image = self.image_sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.starting_x = 642
        self.starting_y = 63
        self.main_group = main_group

        self.direction = random.choice([-1, 1])

        self.position = vector(self.starting_x, self.starting_y)
        self.VERTICAL_ACCELERATION = 0.5
        self.HORIZONTAL_VELOCITY = 6*self.direction
        self.velocity = vector(self.HORIZONTAL_VELOCITY, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        self.rect.topleft = self.position

    def update(self):
        self.move()
        self.check_collisions()
        self.animate(self.image_sprites, 0.5)

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
        self.velocity.y += self.acceleration.y
        self.position += 0.5*self.acceleration + self.velocity

        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x >= WINDOW_WIDTH:
            self.position.x = 0

        self.rect.topleft = self.position

    def check_collisions(self):
        collided_platform = pygame.sprite.spritecollide(self, self.main_group, False, pygame.sprite.collide_mask)
        if self.velocity.y > 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top - 60
                self.velocity.y = 0
        elif self.velocity.y < 0:
            if collided_platform:
                self.position.y = collided_platform[0].rect.top + 15
                self.velocity.y *= -1
        self.rect.topleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]
        self.rect.topleft = self.position


class RubyMaker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RubyMaker, self).__init__()
        self.image_sprites = []
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"), (64, 64)))
        self.image_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"), (64, 64)))

        self.current_sprite = 0
        self.image = self.image_sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.topleft = (x, y)

    def update(self):
        self.animate(self.image_sprites, 0.4)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        self.image = sprite_list[int(self.current_sprite)]
        self.rect.topleft = (self.x, self.y)

my_player_group = pygame.sprite.Group()
my_main_tile_group = pygame.sprite.Group()
my_portal_group = pygame.sprite.Group()
my_bullet_group = pygame.sprite.Group()
my_zombie_group = pygame.sprite.Group()
my_ruby_maker_group = pygame.sprite.Group()
my_ruby_group = pygame.sprite.Group()


tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, my_main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, my_main_tile_group)
        if tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, my_main_tile_group)
        elif tile_map[i][j] == 4:
            Tile(j*32, i*32, 4, my_main_tile_group)
        elif tile_map[i][j] == 5:
            Tile(j*32, i*32, 5, my_main_tile_group)
        elif tile_map[i][j] == 6:
            my_player = Player(j*32, i*32-30, my_main_tile_group, my_ruby_maker_group)
            my_player_group.add(my_player)
        elif tile_map[i][j] == 7:
            portal = Portal(j*32, i*32, "green")
            my_portal_group.add(portal)
        elif tile_map[i][j] == 8:
            portal = Portal(j*32, i*32, "purple")
            my_portal_group.add(portal)
        elif tile_map[i][j] == 9:
            ruby_maker = RubyMaker(j*32, i*32)
            my_ruby_maker_group.add(ruby_maker)

run = False

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

my_game = Game(my_portal_group, my_player, my_bullet_group, my_main_tile_group, my_zombie_group, my_ruby_group)

running = True

my_game.pregame_screen()

while running and run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()
                my_player.jump_sound.play()
            if event.key == pygame.K_UP:
                my_player.shoot()
                my_player.slash_sound.play()
                bullet = Bullet(my_player)
                my_bullet_group.add(bullet)
            if event.key == pygame.K_p:
                my_player.pause_music()
            if event.key == pygame.K_o:
                my_player.unpause_music()
    screen.blit(background_image, background_rect)

    my_main_tile_group.update()
    my_main_tile_group.draw(screen)

    my_player_group.update()
    my_player_group.draw(screen)

    my_portal_group.update()
    my_portal_group.draw(screen)

    my_bullet_group.update()
    my_bullet_group.draw(screen)

    my_zombie_group.update()
    my_zombie_group.draw(screen)

    my_ruby_maker_group.update()
    my_ruby_maker_group.draw(screen)

    my_ruby_group.update()
    my_ruby_group.draw(screen)

    my_game.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.quit()
pygame.quit()