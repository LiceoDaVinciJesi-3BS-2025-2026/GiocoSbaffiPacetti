
import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

camera_offset = 0

WIDTH = 1200
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE JUMP")

background_img = pygame.image.load("schermata_gioco.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

# Suoni
jump_sound = pygame.mixer.Sound("sound_jump.mp3")
gameover_sound = pygame.mixer.Sound("sound_gameover.mp3")

# Colori
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
BLACK = (20, 20, 20)
GREEN = (50, 200, 50)
GRAY = (100, 100, 100)

font_big = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 40)

# pulsante pausa
pause_button = pygame.Rect(WIDTH - 80, 20, 50, 50)
DARK_OVERLAY = (0, 0, 0, 150)

# Stati gioco
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3
game_state = MENU

# Nome giocatore
player_name = ""
active_input = True

# Giocatore
player_width = 50
player_height = 150
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 100, player_width, player_height)
player_vel_y = 0
gravity = 0.8
jump_power = -15
player_img = pygame.image.load("alieno.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_width, player_height))
on_ground = False


# Blocchi
blocks = []
block_width = 150
block_height = 40
block_speed = 4
spawn_timer = 0
spawn_delay = 1500
block_img = pygame.image.load("ufo.png").convert_alpha()

block_img = pygame.transform.scale(block_img, (block_width, block_height))


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

    if len(blocks) == 0:
        y = HEIGHT 
    else:
        last_block = blocks[-1]
        y = last_block["rect"].y - 50  

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
    
    
def main():
    global game_state, player_name
    global player_vel_y, on_ground
    global spawn_timer, camera_offset
    global score, level, block_speed, spawn_delay
    while True:
        dt = clock.tick(FPS)
        screen.blit(background_img, (0, 0))
        
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
                    if event.key == pygame.K_p:
                        game_state = PAUSED
                    if event.key == pygame.K_SPACE and on_ground:
                        player_vel_y = jump_power
                        on_ground = False
                        jump_sound.play()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.collidepoint(event.pos):
                        game_state = PAUSED

                elif game_state == PAUSED:
                    for block in blocks:
                        screen.blit(block_img, block["rect"])
                    screen.blit(player_img, player)

                    draw_text("PAUSA", font_big, RED, WIDTH//2 - 100, HEIGHT//2 - 50)
                    draw_text("Premi P per continuare", font, WHITE, WIDTH//2 - 150, HEIGHT//2 + 20)
            
            # GAME OVER
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = MENU
                        player_name = ""
            
            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PLAYING
                elif game_state == PAUSED:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_button.collidepoint(event.pos):
                            game_state = PLAYING



        # ===== MENU =====
        if game_state == MENU:
            draw_text("SPACE JUMP", font_big, BLUE, WIDTH//2 - 140, 150)
            draw_text("Inserisci il tuo nome:", font, WHITE, WIDTH//2 - 150, 250)
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
                
            if player.y < HEIGHT // 2:
                camera_offset = HEIGHT // 2 - player.y
                player.y = HEIGHT // 2
        
                for block in blocks:
                    block["rect"].y += camera_offset
                    
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
                    if player_vel_y > 0:
                        player.bottom = block["rect"].top
                        player_vel_y = 0
                        on_ground = True
                    else:
                        gameover_sound.play()
                        game_state = GAME_OVER
            
            # Difficoltà crescente
            level = score // 50 + 1
            block_speed = 4 + level * 0.5
            spawn_delay = max(600, 1500 - level * 100)
            
            
            # Bottone pausa
            pygame.draw.rect(screen, GRAY, pause_button, border_radius=12)

            # Icona pausa (due linee)
            pygame.draw.rect(screen, WHITE, (pause_button.x + 15, pause_button.y + 12, 6, 25))
            pygame.draw.rect(screen, WHITE, (pause_button.x + 29, pause_button.y + 12, 6, 25))



            
            # Disegno
            for block in blocks:
                screen.blit(block_img, block["rect"])
            
            screen.blit(player_img, player)
            
            draw_text(f"Giocatore: {player_name}", font, WHITE, 20, 20)
            draw_text(f"Punteggio: {score}", font, WHITE, 20, 60)
            draw_text(f"Livello: {level}", font, WHITE, 20, 100)
        
        elif game_state == PAUSED:

            # Disegna scena congelata
            for block in blocks:
                screen.blit(block_img, block["rect"])
            screen.blit(player_img, player)

            draw_text(f"Giocatore: {player_name}", font, WHITE, 20, 20)
            draw_text(f"Punteggio: {score}", font, WHITE, 20, 60)
            draw_text(f"Livello: {level}", font, WHITE, 20, 100)

            # Overlay scuro trasparente
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(DARK_OVERLAY)
            screen.blit(overlay, (0, 0))

            # Scritta centrale
            draw_text("PAUSA", font_big, WHITE, WIDTH//2 - 100, HEIGHT//2 - 60)

            # Bottone play
            pygame.draw.rect(screen, GRAY, pause_button, border_radius=12)

            # Triangolo play
            pygame.draw.polygon(screen, WHITE, [
                (pause_button.x + 18, pause_button.y + 12),
                (pause_button.x + 18, pause_button.y + 38),
                (pause_button.x + 38, pause_button.y + 25)
            ])

        # ===== GAME OVER =====
        elif game_state == GAME_OVER:
            draw_text("GAME OVER", font_big, RED, WIDTH//2 - 150, 200)
            draw_text(f"Giocatore: {player_name}", font, WHITE, WIDTH//2 - 120, 300)
            draw_text(f"Punteggio finale: {score}", font, WHITE, WIDTH//2 - 140, 350)
            draw_text("Premi ENTER per tornare al menu", font, WHITE, WIDTH//2 - 220, 450)
        
        pygame.display.flip()
       
if __name__ == "__main__":
    main()
    