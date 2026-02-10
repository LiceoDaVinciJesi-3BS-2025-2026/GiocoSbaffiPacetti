# def main() -> None:

import pygame

pygame.init()   

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Lavorare con le Immagini") 

imgSfondo = pygame.image.load("schermata_gioco.png") 
imgSfondo = pygame.transform.scale(imgSfondo,(SCREEN_WIDTH,SCREEN_HEIGHT))

imgSfondo2 = pygame.image.load("schermo2.png") 
imgSfondo2 = pygame.transform.scale(imgSfondo2,(SCREEN_WIDTH,SCREEN_HEIGHT))

imgAlieno = pygame.image.load("alieno.png") 
imgAlieno = pygame.transform.scale(imgAlieno,(100,100))

clock = pygame.time.Clock()

x = 350
y = 400

width = 30
height = 30

speed = 4

camera_x = 0
camera_y = 0

world_size = (2000, 2000)

running = True

while running:  

    pygame.time.delay(10)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y > 0: 
        y -= speed
        
    screen.fill((0, 0, 0))
     
    screen.blit(imgSfondo2, (-camera_x, -camera_y))
    
    screen.blit(imgAlieno, (SCREEN_WIDTH/2 - 25, SCREEN_HEIGHT/2 - 25))   


    pygame.display.flip() 

# 
pygame.quit()






import pygame
import sys

# Inizializzazione Pygame
pygame.init()

# Dimensioni finestra
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Background")

# Carica le immagini di sfondo
# Sostituisci 'sfondo.png' con i nomi dei tuoi file
bg1 = pygame.image.load('sfondo.png').convert() 
bg2 = pygame.image.load('sfondo.png').convert()

# Posizioni iniziali
bgX = 0
bgX2 = bg1.get_width()

# Velocità di scorrimento
speed = 5

clock = pygame.time.Clock()

running = True
while running:
    # 1. Rileva eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Aggiorna posizioni (sposta a sinistra)
    bgX -= speed
    bgX2 -= speed

    # 3. Riposiziona quando escono dallo schermo
    if bgX < -bg1.get_width():
        bgX = bg1.get_width()
    if bgX2 < -bg2.get_width():
        bgX2 = bg2.get_width()

    # 4. Disegna gli sfondi
    screen.blit(bg1, (bgX, 0))
    screen.blit(bg2, (bgX2, 0))

    # 5. Aggiorna lo schermo
    pygame.display.flip()
    clock.tick(60) # 60 FPS

pygame.quit()
sys.exit()