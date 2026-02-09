# def main() -> None:

import pygame

pygame.init()   

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("scappa dalla classe") 

imgSfondo = pygame.image.load("immagine_classe.png")
imgSfondo = pygame.transform.scale(imgSfondo,(SCREEN_WIDTH,SCREEN_HEIGHT))

running = True

while running:  

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    screen.blit(imgSfondo,(0,0) )
    
    pygame.display.flip()

# 
pygame.quit()