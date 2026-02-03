# def main() -> None:
    
import pygame

pygame.init()   

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 880

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Lavorare con le Immagini") 

imgSfondo = pygame.image.load("sfondo.webp") 
imgSfondo = pygame.transform.scale(imgSfondo,(SCREEN_WIDTH,SCREEN_HEIGHT))

# imgMosca = pygame.image.load("mosca.png") 
# imgMosca = pygame.transform.scale(imgMosca,(30,30))
# 
# x = SCREEN_WIDTH // 2
# y = SCREEN_HEIGHT // 2
# 
# width = 30
# height = 30
# 
# speed = 8
# 
# running = True
# 
# while running:  
# 
#     pygame.time.delay(10)
# 
#     for event in pygame.event.get(): 
#         if event.type == pygame.QUIT: 
#             running = False
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             running = False
# 
#     keys = pygame.key.get_pressed() 
#     if keys[pygame.K_LEFT] and x > 0: 
#         x -= speed 
#     if keys[pygame.K_RIGHT] and x < SCREEN_WIDTH - width: 
#         x += speed 
#     if keys[pygame.K_UP] and y > 0: 
#         y -= speed 
#     if keys[pygame.K_DOWN] and y < SCREEN_HEIGHT - height: 
#         y += speed
# 
#     # invece di screen.fill("white")
#     screen.blit(imgSfondo,(0,0) )
# 
#     # invece di pygame.draw.rect(screen, "red", (x, y, width, height)) 
#     screen.blit(imgMosca,(x,y))
# 
#     pygame.display.flip() 
# 
# # 
pygame.quit()
# 