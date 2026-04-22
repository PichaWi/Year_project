import pygame
import math
from settings import *


def load_image(path, size, fallback_color=(255, 255, 255)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        base = load_image(PINK_LASER_IMG, (28, 10), PINK)

        if direction == "left":
            self.image = pygame.transform.flip(base, True, False)
            self.vx = -BULLET_SPEED
        else:
            self.image = base
            self.vx = BULLET_SPEED

        self.rect = self.image.get_rect(center=(x, y))
        self.damage = PLAYER_RANGED_DAMAGE

    def update(self, *args):
        self.rect.x += self.vx
        if self.rect.right < 0 or self.rect.left > WORLD_WIDTH:
            self.kill()


class EnemyArrow(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.base_image = load_image(ENEMY_ARROW_IMG, (26, 8), (220, 220, 220))
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1

        self.vx = (dx / dist) * ENEMY_PROJECTILE_SPEED
        self.vy = (dy / dist) * ENEMY_PROJECTILE_SPEED
        self.damage = ARROW_DAMAGE

        angle = -math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, *args):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        if (
            self.rect.right < 0 or
            self.rect.left > WORLD_WIDTH or
            self.rect.top > HEIGHT or
            self.rect.bottom < 0
        ):
            self.kill()


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.images = {
            "idle_right": load_image(PLAYER_IDLE_RIGHT, (64, 64), (255, 255, 255)),
            "idle_left": load_image(PLAYER_IDLE_LEFT, (64, 64), (255, 255, 255)),
            "run_right": load_image(PLAYER_RUN_RIGHT, (64, 64), (255, 220, 180)),
            "run_left": load_image(PLAYER_RUN_LEFT, (64, 64), (180, 220, 255)),
            "jump_right": load_image(PLAYER_JUMP_RIGHT, (64, 64), (255, 255, 180)),
            "jump_left": load_image(PLAYER_JUMP_LEFT, (64, 64), (255, 255, 180)),
            "fall_right": load_image(PLAYER_FALL_RIGHT, (64, 64), (255, 180, 120)),
            "fall_left": load_image(PLAYER_FALL_LEFT, (64, 64), (255, 180, 120)),
            "attack_right": load_image(PLAYER_ATTACK_RIGHT, (76, 64), (255, 140, 140)),
            "attack_left": load_image(PLAYER_ATTACK_LEFT, (76, 64), (255, 140, 140)),
            "cannon_right": load_image(PLAYER_CANNON_RIGHT, (76, 64), (255, 140, 220)),
            "cannon_left": load_image(PLAYER_CANNON_LEFT, (76, 64), (255, 140, 220)),
        }

        self.facing = "right"
        self.image = self.images["idle_right"]
        self.rect = self.image.get_rect(midbottom=(150, HEIGHT - 120))

        self.vel_y = 0
        self.on_ground = False
        self.health = PLAYER_MAX_HEALTH
        self.inv_timer = 0
        self.shot_cooldown = 0
        self.melee_cooldown = 0
        self.attack_timer = 0
        self.attack_type = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.facing = "right"

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

        return dx

    def update_animation(self, dx):
        if self.attack_timer > 0:
            if self.attack_type == "melee":
                self.image = self.images["attack_left"] if self.facing == "left" else self.images["attack_right"]
            elif self.attack_type == "ranged":
                self.image = self.images["cannon_left"] if self.facing == "left" else self.images["cannon_right"]
            return

        if not self.on_ground:
            if self.vel_y < 0:
                self.image = self.images["jump_left"] if self.facing == "left" else self.images["jump_right"]
            else:
                self.image = self.images["fall_left"] if self.facing == "left" else self.images["fall_right"]
        else:
            if dx < 0:
                self.image = self.images["run_left"]
            elif dx > 0:
                self.image = self.images["run_right"]
            else:
                self.image = self.images["idle_left"] if self.facing == "left" else self.images["idle_right"]

    def update(self, tiles):
        dx = self.handle_input()

        self.rect.x += dx
        self.collide_horizontal(tiles)

        self.vel_y += GRAVITY
        if self.vel_y > PLAYER_MAX_FALL:
            self.vel_y = PLAYER_MAX_FALL

        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide_vertical(tiles)

        if self.inv_timer > 0:
            self.inv_timer -= 1
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.melee_cooldown > 0:
            self.melee_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.attack_type = None

        self.update_animation(dx)

    def collide_horizontal(self, tiles):
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.rect.right > tile.rect.left and self.rect.left < tile.rect.left:
                self.rect.right = tile.rect.left
            elif self.rect.left < tile.rect.right and self.rect.right > tile.rect.right:
                self.rect.left = tile.rect.right

    def collide_vertical(self, tiles):
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

    def shoot(self):
        if self.shot_cooldown == 0 and self.attack_timer == 0:
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN
            self.attack_timer = 10
            self.attack_type = "ranged"

            offset = 26 if self.facing == "right" else -26
            return Bullet(self.rect.centerx + offset, self.rect.centery - 4, self.facing)
        return None

    def start_melee(self):
        if self.melee_cooldown == 0 and self.attack_timer == 0:
            self.melee_cooldown = PLAYER_MELEE_COOLDOWN
            self.attack_timer = PLAYER_MELEE_TIME
            self.attack_type = "melee"
            return True
        return False

    def melee_attack_rect(self):
        if self.facing == "right":
            return pygame.Rect(self.rect.right - 2, self.rect.top + 12, 50, 40)
        return pygame.Rect(self.rect.left - 48, self.rect.top + 12, 50, 40)

    def take_damage(self, amount, from_x=None):
        if self.inv_timer == 0:
            self.health -= amount
            self.inv_timer = PLAYER_INVINCIBILITY

            if from_x is not None:
                if self.rect.centerx < from_x:
                    self.rect.x -= PLAYER_KNOCKBACK
                else:
                    self.rect.x += PLAYER_KNOCKBACK


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, etype="slime", variant=None):
        super().__init__()
        self.etype = etype
        self.variant = variant
        self.vel_y = 0
        self.on_ground = False
        self.attack_timer = 0

        if etype == "slime":
            self.image = load_image(SLIME_IMG, (48, 40), (0, 255, 100))
            self.health = SLIME_HEALTH
            self.speed = SLIME_SPEED
            self.damage = SLIME_DAMAGE

        elif etype == "bat":
            self.image = load_image(BAT_IMG, (48, 34), (180, 100, 220))
            self.health = BAT_HEALTH
            self.speed = BAT_SPEED
            self.damage = BAT_DAMAGE

        elif etype == "zombie":
            self.image = load_image(ZOMBIE_IMG, (56, 56), (70, 120, 70))
            self.health = ZOMBIE_HEALTH
            self.speed = ZOMBIE_SPEED
            self.damage = ZOMBIE_DAMAGE

        elif etype == "skeleton":
            if variant == "sword":
                self.image = load_image(SKELETON_SWORD_IMG, (56, 56), (220, 220, 220))
            elif variant == "bow":
                self.image = load_image(SKELETON_BOW_IMG, (56, 56), (220, 220, 220))
            else:
                self.image = load_image(SKELETON_PLAIN_IMG, (56, 56), (220, 220, 220))

            self.health = SKELETON_HEALTH
            self.speed = SKELETON_SPEED
            self.damage = SKELETON_DAMAGE

        self.rect = self.image.get_rect(midbottom=(x, y))

    def apply_gravity(self, tiles):
        if self.etype != "bat":
            self.vel_y += GRAVITY
            if self.vel_y > PLAYER_MAX_FALL:
                self.vel_y = PLAYER_MAX_FALL

            self.rect.y += self.vel_y
            hits = pygame.sprite.spritecollide(self, tiles, False)
            self.on_ground = False

            for tile in hits:
                if self.vel_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel_y = 0
                    self.on_ground = True

    def update(self, player, tiles, enemy_arrows):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.etype == "slime":
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            self.apply_gravity(tiles)

        elif self.etype == "zombie":
            if abs(player.rect.centerx - self.rect.centerx) < 260:
                if player.rect.centerx < self.rect.centerx:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed
            self.apply_gravity(tiles)

        elif self.etype == "bat":
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)

        elif self.etype == "skeleton":
            dist_x = player.rect.centerx - self.rect.centerx

            if self.variant == "bow":
                if abs(dist_x) > 220:
                    self.rect.x += self.speed if dist_x > 0 else -self.speed
                elif abs(dist_x) < 140:
                    self.rect.x -= self.speed if dist_x > 0 else -self.speed

                if self.attack_timer == 0 and abs(dist_x) < 450:
                    arrow = EnemyArrow(
                        self.rect.centerx,
                        self.rect.centery - 10,
                        player.rect.centerx,
                        player.rect.centery
                    )
                    enemy_arrows.add(arrow)
                    self.attack_timer = 90

                self.apply_gravity(tiles)

            else:
                if player.rect.centerx < self.rect.centerx:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed
                self.apply_gravity(tiles)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
