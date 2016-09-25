# IMPORTANT FOR CIRCLE DEFINITION:
# We defined our unit circle as a mirror image of the standard unit circle.
# Circle starts at left and goes clockwise
# Code reflects this

###############################################################################################################

# Import statements

import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math				# sin, cos, etc

# Draws pointer on dials
def draw_indicator(angle,length,center_x,center_y):

	x_len = math.cos(math.radians(angle))*float(length) # Finds the x and y compoents of the length
	y_len = math.sin(math.radians(angle))*float(length) 

	x_pos = center_x - x_len # Finds the x and y 
	y_pos = center_y - y_len

	pygame.draw.line(screen,red,(center_x,center_y),(x_pos,y_pos),4)

	pygame.draw.circle(screen, red, (center_x,center_y), int(length/15))


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

		num_x_pos = int(center_x-(.8*x_len))
		num_y_pos = int(center_y-(.8*y_len))

		#print x_pos, y_pos, inner_x_pos, inner_y_pos								# debug

		pygame.draw.line(screen,white,(x_pos,y_pos),(inner_x_pos,inner_y_pos),6)	# draws tick mark

		num = font.render(str(mark),1,white)

		(num_width,num_height) = font.size(str(num))

		screen.blit(num,(num_x_pos-5,num_y_pos-(num_height/2)))


# Draws redline on outside of circle
def draw_redline_arc(startAngle,stopAngle,center_x,center_y,radius):

	rect = (center_x-radius,center_y-radius,2*radius,2*radius)		# Defines the rectangle to draw arc in

	start_radians = math.radians((-stopAngle)+180)					# Converts between our "unit circle" and standard unic circle
	stop_radians = math.radians((-startAngle)+180)

	pygame.draw.arc(screen,red,rect,start_radians,stop_radians,10)	# Draws Arc


############# Color Definitions
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
green = (0,120,0)
white = (255,255,255)
###############################

pygame.init()

font = pygame.font.Font(None, 36)

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

screen.fill(grey)

pygame.draw.circle(screen, black, (160, 240), 200, 0)

pygame.draw.rect(screen, green, (400,20,250,190))
pygame.draw.rect(screen, green, (400,270,250,190))

font = pygame.font.Font(None, 36)

draw_tick_marks(45,315,14,160,240,200)



while 1:
	for i in range(45,315):
		pygame.draw.circle(screen, black, (160, 240), 200, 0)
		draw_redline_arc(305,315,160,240,200)
		draw_tick_marks(45,315,14,160,240,200)
		draw_indicator(i,190,160,240)

		pygame.display.update()




