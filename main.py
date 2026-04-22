import pygame
import random
from settings import *
from ui import UI, Button
from entities import Player, Enemy, Tile, Decoration, load_image


class EchoKnight:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.state = MENU
        self.camera_x = 0

        self.buttons = {
            "play": Button(WIDTH // 2 - 100, 260, 200, 50, "PLAY", (100, 50, 200)),
            "credits": Button(WIDTH // 2 - 100, 330, 200, 50, "CREDITS", (80, 80, 80)),
            "quit": Button(WIDTH // 2 - 100, 400, 200, 50, "QUIT", (150, 0, 0))
        }

        self.load_assets()
        self.reset_game()

    def load_assets(self):
        self.bg_images = [
            load_image(BACKGROUND_1, (WIDTH, HEIGHT), (20, 20, 35)),
            load_image(BACKGROUND_2, (WIDTH, HEIGHT), (25, 25, 40)),
            load_image(BACKGROUND_3, (WIDTH, HEIGHT), (30, 30, 45)),
        ]

        self.ground_tile_img = load_image(GROUND_TILE, (TILE_SIZE, TILE_SIZE), (90, 90, 90))
        self.platform_tile_img = load_image(PLATFORM_TILE, (TILE_SIZE, TILE_SIZE), (120, 120, 120))

        self.crate_img = load_image(CRATE_IMG, (50, 50), (130, 90, 50))
        self.torch_img = load_image(TORCH_IMG, (32, 64), (255, 180, 80))
        self.stone_img = load_image(STONE_IMG, (46, 30), (120, 120, 120))

    def reset_game(self):
        self.player = Player()

        self.tiles = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_arrows = pygame.sprite.Group()
        self.melee_hit_targets = set()

        self.current_bg = random.choice(self.bg_images)
        self.build_level()
        self.camera_x = 0

    def build_level(self):
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            self.tiles.add(Tile(x, HEIGHT - 64, self.ground_tile_img))

        platform_layout = [
            (350, 470, 3),
            (700, 390, 4),
            (1100, 450, 3),
            (1450, 350, 4),
            (1850, 430, 3),
            (2250, 320, 5),
            (2700, 420, 3),
        ]

        for px, py, count in platform_layout:
            for i in range(count):
                self.tiles.add(Tile(px + i * TILE_SIZE, py, self.platform_tile_img))

        deco_data = [
            (420, HEIGHT - 64, self.crate_img),
            (900, HEIGHT - 64, self.stone_img),
            (1180, HEIGHT - 64, self.torch_img),
            (1600, HEIGHT - 64, self.crate_img),
            (2100, HEIGHT - 64, self.stone_img),
            (2500, HEIGHT - 64, self.torch_img),
        ]

        for x, y, img in deco_data:
            self.decorations.add(Decoration(x, y, img))

        spawn_data = [
            (550, HEIGHT - 64, "slime", None),
            (830, 390, "bat", None),
            (1230, HEIGHT - 64, "zombie", None),
            (1540, 350, "skeleton", "plain"),
            (2050, HEIGHT - 64, "skeleton", "sword"),
            (2380, 320, "skeleton", "bow"),
            (2850, HEIGHT - 64, "bat", None),
        ]

        for x, y, etype, variant in spawn_data:
            self.enemies.add(Enemy(x, y, etype, variant))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == MENU:
                    if self.buttons["play"].is_clicked(event.pos):
                        self.state = PLAYING
                    elif self.buttons["credits"].is_clicked(event.pos):
                        self.state = CREDITS
                    elif self.buttons["quit"].is_clicked(event.pos):
                        return False
                elif self.state == CREDITS:
                    self.state = MENU
                elif self.state == GAME_OVER:
                    self.reset_game()
                    self.state = PLAYING

            if event.type == pygame.KEYDOWN:
                if self.state == PLAYING:
                    if event.key == pygame.K_z:
                        bullet = self.player.shoot()
                        if bullet:
                            self.bullets.add(bullet)

                    if event.key == pygame.K_x:
                        started = self.player.start_melee()
                        if started:
                            self.melee_hit_targets.clear()

                elif self.state == CREDITS and event.key == pygame.K_ESCAPE:
                    self.state = MENU

                elif self.state == GAME_OVER and event.key == pygame.K_r:
                    self.reset_game()
                    self.state = PLAYING

        return True

    def update_camera(self):
        self.camera_x = self.player.rect.centerx - WIDTH // 2
        self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH - WIDTH))

    def handle_melee_hits(self):
        if self.player.attack_type == "melee" and self.player.attack_timer > 0:
            attack_rect = self.player.melee_attack_rect()
            for enemy in self.enemies:
                if enemy in self.melee_hit_targets:
                    continue
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(PLAYER_MELEE_DAMAGE)
                    self.melee_hit_targets.add(enemy)

        if self.player.attack_type != "melee":
            self.melee_hit_targets.clear()

    def update_playing(self):
        self.player.update(self.tiles)
        self.bullets.update()
        self.enemy_arrows.update()

        for enemy in self.enemies:
            enemy.update(self.player, self.tiles, self.enemy_arrows)

        bullet_hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemies_hit in bullet_hits.items():
            for enemy in enemies_hit:
                enemy.take_damage(bullet.damage)

        self.handle_melee_hits()

        arrow_hits = pygame.sprite.spritecollide(self.player, self.enemy_arrows, True)
        for arrow in arrow_hits:
            self.player.take_damage(arrow.damage, arrow.rect.centerx)

        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_hits:
            self.player.take_damage(enemy.damage, enemy.rect.centerx)

        if self.player.health <= 0:
            self.state = GAME_OVER

        self.update_camera()

    def draw_world_group(self, group):
        for sprite in group:
            draw_rect = sprite.rect.copy()
            draw_rect.x -= self.camera_x
            self.screen.blit(sprite.image, draw_rect)

    def draw_background(self):
        bg_width = self.current_bg.get_width()
        x1 = -(self.camera_x * 0.3) % bg_width
        self.screen.blit(self.current_bg, (x1 - bg_width, 0))
        self.screen.blit(self.current_bg, (x1, 0))
        self.screen.blit(self.current_bg, (x1 + bg_width, 0))

    def draw_melee_effect(self):
        if self.player.attack_type == "melee" and self.player.attack_timer > 0:
            attack_rect = self.player.melee_attack_rect()
            draw_rect = attack_rect.copy()
            draw_rect.x -= self.camera_x
            pygame.draw.rect(self.screen, (255, 120, 180), draw_rect, 2)

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.ui.title_font.render("ECHO KNIGHT", True, PINK)
        self.screen.blit(title, (WIDTH // 2 - 210, 120))

        for button in self.buttons.values():
            button.draw(self.screen)

    def draw_credits(self):
        self.screen.fill((15, 15, 25))
        title = self.ui.title_font.render("CREDITS", True, GOLD)
        self.screen.blit(title, (WIDTH // 2 - 130, 100))

        lines = [
            "Echo Knight project",
            "Player sprite based on your original character",
            "Side-scrolling prototype with melee and cannon attack",
            "Click or press ESC to return"
        ]

        for i, line in enumerate(lines):
            txt = self.ui.font.render(line, True, WHITE)
            self.screen.blit(txt, (WIDTH // 2 - 260, 240 + i * 40))

    def draw_game_over(self):
        self.screen.fill(BLACK)
        title = self.ui.title_font.render("YOU DIED", True, RED)
        self.screen.blit(title, (WIDTH // 2 - 170, 200))

        text = self.ui.font.render("Click or press R to restart", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - 135, 300))

    def draw_playing(self):
        self.draw_background()
        self.draw_world_group(self.tiles)
        self.draw_world_group(self.decorations)
        self.draw_world_group(self.enemies)
        self.draw_world_group(self.bullets)
        self.draw_world_group(self.enemy_arrows)

        player_rect = self.player.rect.copy()
        player_rect.x -= self.camera_x
        self.screen.blit(self.player.image, player_rect)

        self.draw_melee_effect()
        self.ui.draw_hud(self.screen, self.player)

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if self.state == PLAYING:
                self.update_playing()

            if self.state == MENU:
                self.draw_menu()
            elif self.state == PLAYING:
                self.draw_playing()
            elif self.state == CREDITS:
                self.draw_credits()
            elif self.state == GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    EchoKnight().run()
