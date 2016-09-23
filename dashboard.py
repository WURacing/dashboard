import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays

############# Color Definitions
red = 	(255,0,0)
black = (0,0,0)
grey = 	(200,200,200)
###############################

pygame.init()

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

screen.fill(grey)

pygame.draw.circle(screen, black, (40, 400), 200, 200)

pygame.draw.circle(screen, black, (760,400), 200, 200)

while 1:
	pygame.display.update()

	time.sleep(100)


