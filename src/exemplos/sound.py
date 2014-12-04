import pygame, sys, time
from pygame.locals import *

pygame.init()

sound = pygame.mixer.Sound("../resources/bow.wav")
sound.play()

pygame.mixer.music.load("../resources/peace.mp3")
pygame.mixer.music.play(-1,0.0)
time.sleep(5)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()