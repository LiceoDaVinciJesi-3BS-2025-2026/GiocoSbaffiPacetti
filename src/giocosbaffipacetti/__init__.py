# GIOCO SBAFFI E PACETTI

import pygame
import random
import sys

# Inizializza pygame e il sistema audio
pygame.init()
pygame.mixer.init()

# Offset della camera (serve per far salire la visuale quando il player sale)
camera_offset = 0

# Dimensioni finestra
WIDTH = 1200
HEIGHT = 700 

# Creazione finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE JUMP")

# Caricamento e ridimensionamento dello sfondo
background_img = pygame.image.load("schermata_gioco.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Clock per gestire gli FPS
clock = pygame.time.Clock()
FPS = 60

# Suoni
jump_sound = pygame.mixer.Sound("sound_jump.mp3")
gameover_sound = pygame.mixer.Sound("sound_gameover.mp3")

# Colori
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
GRAY = (100, 100, 100)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Font utilizzati nel gioco
font_big = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 40)

# pulsante pausa
pause_button = pygame.Rect(WIDTH - 80, 20, 50, 50)
DARK_OVERLAY = (0, 0, 0, 150)

# pulsante classifica
leaderboard_button = pygame.Rect(WIDTH//2 - 100, 450, 200, 50)

# Stati gioco
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3
LEADERBOARD = 4
game_state = MENU
last_block_spawned = None

# Nome giocatore
player_name = ""

# ===== GIOCATORE =====
player_width = 50
player_height = 150

# Rettangolo che rappresenta il giocatore
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - 100, player_width, player_height)

# Velocità verticale
player_vel_y = 0

# Gravità
gravity = 0.8

# Forza del salto
jump_power = -13

# Immagine del player
player_img = pygame.image.load("alieno.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_width, player_height))
on_ground = False

 
# ===== BLOCCHI / PIATTAFORME =====
blocks = []
block_width = 150
block_height = 40
block_speed = 4
spawn_timer = 0
spawn_delay = 2000
spawn_next_on_center = False
block_to_watch = None
waiting_for_spawn = False
next_spawn_time = random.randint(800, 2000)

# Immagini blocchi
block_img = pygame.image.load("ufo.png").convert_alpha()
block_img = pygame.transform.scale(block_img, (block_width, block_height))
block_img_appiccicoso = pygame.image.load("ufo_appiccicoso.png").convert_alpha()
block_img_appiccicoso = pygame.transform.scale(block_img_appiccicoso, (block_width, block_height))

# ===== PUNTEGGIO =====
score = 0
level = 1
score_saved = False

# Classifica
leaderboard = []
MAX_SCORES = 10
first_jump_done = False

# RESET DEL GIOCO
def reset_game():
    """
    Ripristina tutte le variabili del gioco
    quando si inizia una nuova partita
    """
    global blocks, score, level, block_speed, spawn_delay, next_spawn_time
    global player, player_vel_y, on_ground
    global score_saved, last_block_spawned, first_jump_done 
    
    blocks = []
    last_block_spawned = None
    score = 0
    level = 1
    block_speed = 4
    spawn_delay = 1500
    
    # Riposiziona il player
    player.y = HEIGHT - 100
    player.x = WIDTH // 2 - player_width // 2
    player_vel_y = 0
    on_ground = False
    score_saved = False
    first_jump_done = False 
    next_spawn_time = random.randint(800, 2000)
    
    spawn_block()

# GENERAZIONE BLOCCO
def spawn_block():
    """
    Genera un nuovo blocco.
    Il lato di spawn dipende dal blocco precedente.
    """
    global last_block_spawned

    # Determina lato di spawn
    if last_block_spawned and last_block_spawned["type"] == "moving":
        # Blocchi moving -> spawn dal lato opposto della direzione dell'ultimo blocco
        if last_block_spawned["direction"] == 1:
            x = WIDTH - block_width
            direction = -1
        else:
            x = 0
            direction = 1
    else:
        # Spawn casuale se non ci sono blocchi o blocco normale
        side = random.choice(["left", "right"])
        if side == "left":
            x = 0
            direction = 1
        else:
            x = WIDTH - block_width
            direction = -1

    # Altezza del nuovo blocco
    if len(blocks) == 0:
        y = HEIGHT - 50
    else:
        last_block = blocks[-1]
        y = last_block["rect"].y - 50  

    block_type = random.choice(["normal", "moving"])

    block = {
        "rect": pygame.Rect(x, y, block_width, block_height),
        "direction": direction,
        "placed": False,
        "type": block_type
    }

    blocks.append(block)
    last_block_spawned = block

# DISEGNO TESTO
def draw_text(text, font, color, x, y):
    """Disegna testo sullo schermo"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# CARICAMENTO CLASSIFICA
def load_leaderboard():
    """
    Carica la classifica dal file classifica.txt
    """
    global leaderboard
    leaderboard = []
    try:
        with open("classifica.txt", "r") as f:
            for line in f:
                line = line.strip()
                if "," in line:
                    name, score = line.strip().split(",")
                    leaderboard.append((name, int(score)))
    except FileNotFoundError:
        pass

# SALVATAGGIO CLASSIFICA
def save_leaderboard():
    with open("classifica.txt", "w") as f:
        for name, score in leaderboard:
            f.write(f"{name},{score}\n")

# AGGIORNA CLASSIFICA
def update_leaderboard(name, score):
    """
    Aggiorna la classifica:
    - se il giocatore esiste aggiorna il punteggio
    - se non esiste lo aggiunge
    """
    global leaderboard

    found = False

    for i, (n, s) in enumerate(leaderboard):
        if n == name:
            found = True
            if score > s:  # aggiorna solo se il nuovo punteggio è migliore
                leaderboard[i] = (name, score)
            break

    if not found:
        leaderboard.append((name, score))
        
    # Ordina classifica
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
    
    # Mantieni solo i primi 10
    leaderboard = leaderboard[:MAX_SCORES]

    save_leaderboard()  

# CICLO PRINCIPALE DEL GIOCO
def main():
    global game_state, player_name
    global player_vel_y, on_ground
    global spawn_timer, camera_offset, next_spawn_time
    global score, level, block_speed, spawn_delay
    global waiting_for_spawn, spawn_next_on_center, block_to_watch
    global score_saved, first_jump_done
    while True:
        dt = clock.tick(FPS)
        screen.blit(background_img, (0, 0))
        
        # EVENTI INPUT
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ===== MENU =====
            if game_state == MENU:
                
                # Input nome giocatore
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        if player_name != "":
                            reset_game()
                            game_state = PLAYING

                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

                    else:
                        if len(player_name) < 12:
                            player_name += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if leaderboard_button.collidepoint(event.pos):
                        game_state = LEADERBOARD

            # ===== PLAYING =====
            elif game_state == PLAYING:

                if event.type == pygame.KEYDOWN:

                    # Pausa
                    if event.key == pygame.K_p:
                        game_state = PAUSED

                    # Salto
                    if event.key == pygame.K_SPACE and on_ground:
                        player_vel_y = jump_power
                        on_ground = False
                        first_jump_done = True 
                        jump_sound.play()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.collidepoint(event.pos):
                        game_state = PAUSED

            # ===== PAUSA =====
            elif game_state == PAUSED:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PLAYING

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.collidepoint(event.pos):
                        game_state = PLAYING

            # ===== GAME OVER =====
            elif game_state == GAME_OVER:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = MENU

            # ===== CLASSIFICA =====
            elif game_state == LEADERBOARD:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = MENU

        # ===== MENU =====
        if game_state == MENU:
            draw_text("SPACE JUMP", font_big, BLUE, WIDTH//2 - 140, 150)
            draw_text("Inserisci il tuo nome:", font, WHITE, WIDTH//2 - 150, 250)
            pygame.draw.rect(screen, GRAY, (WIDTH//2 - 150, 300, 300, 50), 2)
            draw_text(player_name, font, WHITE, WIDTH//2 - 140, 310)
            draw_text("Premi ENTER per iniziare", font, WHITE, WIDTH//2 - 180, 380)
            pygame.draw.rect(screen, BLUE, leaderboard_button, border_radius=12)
            draw_text("CLASSIFICA", font, WHITE, leaderboard_button.x + 20, leaderboard_button.y + 12.5)

        # ===== GIOCO =====
        elif game_state == PLAYING:
            
            # Gravità
            player_vel_y += gravity
            player.y += player_vel_y
            
            if player.bottom >= HEIGHT:
                if first_jump_done:
                    if not score_saved:
                        gameover_sound.play()
                        update_leaderboard(player_name, score)
                        score_saved = True
                    game_state = GAME_OVER
                else:
                    player.bottom = HEIGHT
                    player_vel_y = 0
                    on_ground = True
                
            if player.y < HEIGHT // 2:
                camera_offset = HEIGHT // 2 - player.y
                player.y = HEIGHT // 2
        
                for block in blocks:
                    block["rect"].y += camera_offset
                    
            if spawn_next_on_center and block_to_watch is not None:
                block_center_x = block_to_watch["rect"].x + block_width // 2
                if abs(block_center_x - WIDTH // 2) < 5:  # centro ±5 px
                    spawn_block()
                    spawn_next_on_center = False
                    block_to_watch = None
                    
            if waiting_for_spawn:
                spawn_timer += dt

                if spawn_timer >= spawn_delay:
                    spawn_block()
                    waiting_for_spawn = False
            
            # Movimento blocchi
            for block in blocks:

                # blocchi verdi si muovono sempre
                if block["type"] == "moving":
                    block["rect"].x += block["direction"] * block_speed

                # blocchi blu si muovono solo finché non li usi
                elif block["type"] == "normal" and not block["placed"]:
                    block["rect"].x += block["direction"] * block_speed


                # rimbalzo ai bordi
                if block["rect"].left <= 0:
                    block["rect"].left = 0
                    block["direction"] = 1

                if block["rect"].right >= WIDTH:
                    block["rect"].right = WIDTH
                    block["direction"] = -1

                # Collisioni con il giocatore
                if player.colliderect(block["rect"]):
                    if player_vel_y > 0:
                        # Atterra sul blocco
                        player.bottom = block["rect"].top
                        player_vel_y = 0
                        on_ground = True

                        # Se blocco è mobile, trasporta il giocatore
                        if block["type"] == "moving":
                            player.x += block["direction"] * block_speed
                            if player.left < 0:
                                player.left = 0
                            if player.right > WIDTH:
                                player.right = WIDTH

                        # Segna blocco come "placed" e genera il prossimo
                        if not block["placed"]:
                            block["placed"] = True
                            score += 10
                            if block["type"] == "normal":
                                waiting_for_spawn = True
                                spawn_timer = 0
                            elif block["type"] == "moving":
                                spawn_next_on_center = True
                                block_to_watch = block

                    else:
                        # Colpito da sotto -> GAME OVER
                        if not score_saved:
                            gameover_sound.play()
                            update_leaderboard(player_name, score)
                            score_saved = True
                        game_state = GAME_OVER
   
            # Difficoltà crescente
            level = score // 100 + 1
            block_speed = random.randint(2, 10) + level * 0.5
            spawn_delay = max(600, 1500 - level * 100)
            
            
            # Bottone pausa
            pygame.draw.rect(screen, GRAY, pause_button, border_radius=12)

            # Icona pausa (due linee)
            pygame.draw.rect(screen, WHITE, (pause_button.x + 15, pause_button.y + 12, 6, 25))
            pygame.draw.rect(screen, WHITE, (pause_button.x + 29, pause_button.y + 12, 6, 25))



            
            # Disegno
            for block in blocks:

                if block["type"] == "moving":
                    screen.blit(block_img, block["rect"])
                else:
                    screen.blit(block_img_appiccicoso, block["rect"])
                    
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
            draw_text("GAME OVER", font_big, RED, WIDTH//2 - 150, 150)
            draw_text(f"Giocatore: {player_name}", font, WHITE, WIDTH//2 - 120, 230)
            draw_text(f"Punteggio finale: {score}", font, WHITE, WIDTH//2 - 140, 270)
            draw_text("Premi ENTER per tornare al menu", font, WHITE, WIDTH//2 - 220, HEIGHT - 80)
  
          # ===== CLASSIFICA =====
        elif game_state == LEADERBOARD:

            draw_text("CLASSIFICA", font_big, BLUE, WIDTH//2 - 150, 150)
            y_offset = 225
            
            for i in range(10):

                if i < len(leaderboard):
                    name, scr = leaderboard[i]
                    text = f"{i+1}. {name} - {scr}"
                else:
                    text = f"{i+1}. ---"

                # Colori podio
                if i == 0:
                    color = GOLD
                elif i == 1:
                    color = SILVER
                elif i == 2:
                    color = BRONZE
                else:
                    color = WHITE

                draw_text(text, font, color, WIDTH//2 - 150, y_offset)
                y_offset += 40
            draw_text("Premi ESC per tornare al menu", font, WHITE, WIDTH//2 - 200, HEIGHT - 50)

        pygame.display.flip()
       
if __name__ == "__main__":
    load_leaderboard()
    main()
    