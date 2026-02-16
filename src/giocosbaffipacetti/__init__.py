# def main() -> None:

import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Jump Pro")

clock = pygame.time.Clock()
FPS = 60

# Suoni
# jump_sound = pygame.mixer.Sound("jump.wav")
# gameover_sound = pygame.mixer.Sound("gameover.wav")

# Colori
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
BLACK = (20, 20, 20)
GREEN = (50, 200, 50)
GRAY = (100, 100, 100)

font_big = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 40)

# Stati gioco
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Nome giocatore
player_name = ""
active_input = True

# Giocatore
player_size = 40
player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - 100, player_size, player_size)
player_vel_y = 0
gravity = 0.8
jump_power = -15
on_ground = False

# Blocchi
blocks = []
block_width = 120
block_height = 30
block_speed = 4
spawn_timer = 0
spawn_delay = 1500

# Punteggio
score = 0
level = 1

def reset_game():
    global blocks, score, level, block_speed, spawn_delay
    global player, player_vel_y, on_ground
    blocks = []
    score = 0
    level = 1
    block_speed = 4
    spawn_delay = 1500
    player.y = HEIGHT - 100
    player_vel_y = 0
    on_ground = False

def spawn_block():
    side = random.choice(["left", "right"])
    y = HEIGHT - block_height - len(blocks) * block_height
    
    if side == "left":
        x = -block_width
        direction = 1
    else:
        x = WIDTH
        direction = -1
    
    block = {
        "rect": pygame.Rect(x, y, block_width, block_height),
        "direction": direction,
        "placed": False
    }
    
    blocks.append(block)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Loop principale
while True:
    dt = clock.tick(FPS)
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # MENU
        if game_state == MENU:
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN and player_name != "":
                    reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12:
                        player_name += event.unicode
        
        # GIOCO
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_power
                    on_ground = False
#                    jump_sound.play()
        
        # GAME OVER
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MENU
                    player_name = ""
    
    # ===== MENU =====
    if game_state == MENU:
        draw_text("TOWER JUMP PRO", font_big, GREEN, WIDTH//2 - 200, 150)
        draw_text("Inserisci il tuo nome:", font, WHITE, WIDTH//2 - 160, 250)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 150, 300, 300, 50), 2)
        draw_text(player_name, font, WHITE, WIDTH//2 - 140, 310)
        draw_text("Premi ENTER per iniziare", font, WHITE, WIDTH//2 - 180, 380)
    
    # ===== GIOCO =====
    elif game_state == PLAYING:
        
        # Gravità
        player_vel_y += gravity
        player.y += player_vel_y
        
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT
            player_vel_y = 0
            on_ground = True
        
        # Spawn blocchi
        spawn_timer += dt
        if spawn_timer > spawn_delay:
            spawn_block()
            spawn_timer = 0
        
        # Movimento blocchi
        for block in blocks:
            if not block["placed"]:
                block["rect"].x += block["direction"] * block_speed
                
                if (block["direction"] == 1 and block["rect"].x >= WIDTH//2 - block_width//2) or \
                   (block["direction"] == -1 and block["rect"].x <= WIDTH//2 - block_width//2):
                    
                    block["rect"].x = WIDTH//2 - block_width//2
                    block["placed"] = True
                    score += 10
        
            # Collisioni
            if player.colliderect(block["rect"]):
                if player_vel_y > 0 and player.bottom - player_vel_y <= block["rect"].top:
                    player.bottom = block["rect"].top
                    player_vel_y = 0
                    on_ground = True
                else:
#                    gameover_sound.play()
                    game_state = GAME_OVER
        
        # Difficoltà crescente
        level = score // 50 + 1
        block_speed = 4 + level * 0.5
        spawn_delay = max(600, 1500 - level * 100)
        
        # Disegno
        for block in blocks:
            pygame.draw.rect(screen, RED, block["rect"])
        
        pygame.draw.rect(screen, BLUE, player)
        
        draw_text(f"Giocatore: {player_name}", font, WHITE, 20, 20)
        draw_text(f"Punteggio: {score}", font, WHITE, 20, 60)
        draw_text(f"Livello: {level}", font, WHITE, 20, 100)
    
    # ===== GAME OVER =====
    elif game_state == GAME_OVER:
        draw_text("GAME OVER", font_big, RED, WIDTH//2 - 150, 200)
        draw_text(f"Giocatore: {player_name}", font, WHITE, WIDTH//2 - 120, 300)
        draw_text(f"Punteggio finale: {score}", font, WHITE, WIDTH//2 - 140, 350)
        draw_text("Premi ENTER per tornare al menu", font, WHITE, WIDTH//2 - 220, 450)
    
    pygame.display.flip()