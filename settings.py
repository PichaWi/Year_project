import pygame

# Screen
WIDTH, HEIGHT = 1000, 600
FPS = 60
TITLE = "Echo Knight"

# States
MENU, PLAYING, CREDITS, GAME_OVER = "menu", "playing", "credits", "game_over"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
GOLD = (255, 215, 0)
RED = (220, 50, 50)

# Physics
GRAVITY = 0.7
PLAYER_SPEED = 5
JUMP_POWER = -14
PLAYER_MAX_FALL = 14

# Player combat
PLAYER_MAX_HEALTH = 100
PLAYER_INVINCIBILITY = 40
PLAYER_SHOT_COOLDOWN = 18
PLAYER_MELEE_COOLDOWN = 24
PLAYER_MELEE_TIME = 10
PLAYER_MELEE_DAMAGE = 2
PLAYER_RANGED_DAMAGE = 1
PLAYER_KNOCKBACK = 8

# Projectiles
BULLET_SPEED = 12
ENEMY_PROJECTILE_SPEED = 7
ARROW_DAMAGE = 8

# World
TILE_SIZE = 64
WORLD_WIDTH = 3200
WORLD_HEIGHT = HEIGHT

# Enemy balance
SLIME_SPEED = 2
BAT_SPEED = 3
ZOMBIE_SPEED = 1
SKELETON_SPEED = 2

SLIME_HEALTH = 2
BAT_HEALTH = 1
ZOMBIE_HEALTH = 3
SKELETON_HEALTH = 2

SLIME_DAMAGE = 1
BAT_DAMAGE = 1
ZOMBIE_DAMAGE = 2
SKELETON_DAMAGE = 2

# Player assets
PLAYER_IDLE_RIGHT = "assets/player/player_idle_right.png"
PLAYER_IDLE_LEFT = "assets/player/player_idle_left.png"
PLAYER_RUN_RIGHT = "assets/player/player_run_right.png"
PLAYER_RUN_LEFT = "assets/player/player_run_left.png"
PLAYER_JUMP_RIGHT = "assets/player/player_jump_right.png"
PLAYER_JUMP_LEFT = "assets/player/player_jump_left.png"
PLAYER_FALL_RIGHT = "assets/player/player_fall_right.png"
PLAYER_FALL_LEFT = "assets/player/player_fall_left.png"
PLAYER_ATTACK_RIGHT = "assets/player/player_attack_right.png"
PLAYER_ATTACK_LEFT = "assets/player/player_attack_left.png"
PLAYER_CANNON_RIGHT = "assets/player/player_cannon_right.png"
PLAYER_CANNON_LEFT = "assets/player/player_cannon_left.png"

# Enemy assets
SLIME_IMG = "assets/enemies/slime.png"
BAT_IMG = "assets/enemies/bat.png"
ZOMBIE_IMG = "assets/enemies/zombie.png"
SKELETON_PLAIN_IMG = "assets/enemies/skeleton_plain.png"
SKELETON_SWORD_IMG = "assets/enemies/skeleton_sword.png"
SKELETON_BOW_IMG = "assets/enemies/skeleton_bow.png"

# Projectile assets
PINK_LASER_IMG = "assets/projectiles/pink_laser.png"
ENEMY_ARROW_IMG = "assets/projectiles/enemy_arrow.png"

# Backgrounds
BACKGROUND_1 = "assets/backgrounds/background_1.png"
BACKGROUND_2 = "assets/backgrounds/background_2.png"
BACKGROUND_3 = "assets/backgrounds/background_3.png"

# Tiles
GROUND_TILE = "assets/tiles/ground_tile.png"
PLATFORM_TILE = "assets/tiles/platform_tile.png"

# Objects
CRATE_IMG = "assets/objects/crate.png"
TORCH_IMG = "assets/objects/torch.png"
STONE_IMG = "assets/objects/stone.png"
