import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math


# Draws tick marks along the outside of circles
def draw_tick_marks(startAngle,stopAngle,numMarks,center_x,center_y,radius):

	angle_diff = stopAngle-startAngle												# Value of the difference between the start and stop angles
	spacing = float(angle_diff)/float(numMarks-1)									# Angle spacing between each mark

	for mark in range(numMarks): 													# Loops through each tick mark
		current_angle=startAngle+(spacing*float(mark))								# Current angle for this tick mark
		y_len = math.sin(math.radians(current_angle))*radius						# y component of length
		x_len = math.cos(math.radians(current_angle))*radius						# x component of length

		x_pos = int(center_x - x_len)												# x coordinate of outside point
		y_pos = int(center_y - y_len)												# y coordinate of outside point

		inner_x_pos = int(center_x-(.9*x_len))										# x coordinate of inside point
		inner_y_pos = int(center_y-(.9*y_len))										# y coordinate of inside point

		#print x_pos, y_pos, inner_x_pos, inner_y_pos								# debug

		pygame.draw.line(screen,white,(x_pos,y_pos),(inner_x_pos,inner_y_pos),5)	# draws tick mark



############# Color Definitions
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
green = (0,120,0)
white = (255,255,255)
###############################

pygame.init()

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

screen.fill(grey)

pygame.draw.circle(screen, black, (160, 240), 200, 0)

pygame.draw.rect(screen, green, (400,20,250,190))
pygame.draw.rect(screen, green, (400,270,250,190))

draw_tick_marks(45,315,13,160,240,200)



while 1:
	pygame.display.update()






