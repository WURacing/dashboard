# Authors: Michael Greer

# IMPORTANT FOR CIRCLE DEFINITION:
# We defined our unit circle as a mirror image of the standard unit circle.
# Circle starts at left and goes clockwise
# Code reflects this

###############################################################################################################

# -*- coding: utf-8 -*-

# Import statements

import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math				# sin, cos, etc
import struct			# For converting byte to float

# Is this a test or not
test = True

# Initialize serial
if (not test): 
	arduino = serial.Serial('/dev/ttyUSB0',9600)

# Draws pointer on dials
def draw_indicator(angle,length,center_x,center_y):

	x_len = math.cos(math.radians(angle))*float(length) # Finds the x and y compoents of the length
	y_len = math.sin(math.radians(angle))*float(length) 

	x_pos = center_x - x_len # Finds the x and y 
	y_pos = center_y - y_len
	
	inner_x_pos = int(center_x-(.6*x_len))										# x coordinate of inside point
	inner_y_pos = int(center_y-(.6*y_len))

	pygame.draw.line(screen,red,(inner_x_pos,inner_y_pos),(x_pos,y_pos),10)

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


#Draws all parts of display that are not data-dependent
def draw_screen():

#	Draw dial
	pygame.draw.circle(screen, lgrey, (160, 240), 210, 0)
	pygame.draw.circle(screen, black, (160, 240), 200, 0)
	draw_redline_arc(305,315,160,240,200)
	pygame.draw.rect(screen, lgrey, (0,100,20,280))
	pygame.draw.ellipse(screen, black, (8, 100, 20, 280), 0)
	pygame.draw.ellipse(screen, black, (8, 100, 20, 280), 0)
	draw_tick_marks(45,315,14,160,240,200)
# 	pygame.draw.rect(screen, green, (80,240,160,80))  RPM Font Box
	
#	Draw rectangles
	pygame.draw.rect(screen, lgrey, (440,10,320,210))
	pygame.draw.rect(screen, green, (450,20,300,190))
	pygame.draw.rect(screen, lgrey, (440,260,320,210))
	pygame.draw.rect(screen, green, (450,270,300,190))
	

# maps a variable from one space to another
def linear_transform(input,rangeOneStart,rangeOneEnd,rangeTwoStart,rangeTwoEnd):

	return int((input-rangeOneStart)*(float(rangeTwoEnd-rangeTwoStart)/float(rangeOneEnd-rangeOneStart))+rangeTwoStart)


############# Color Definitions
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
lgrey=	(150,150,150)
green = (0,120,0)
white = (255,255,255)
###############################

pygame.init()

font = pygame.font.Font("fonts/monaco.ttf", 24)

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

#pygame.display.toggle_fullscreen() # Sets display mode to full screen

screen.fill(grey)

pygame.draw.circle(screen, black, (160, 240), 200, 0)

display_font = pygame.font.Font("fonts/monaco.ttf", 120)

rpm_font = pygame.font.Font("fonts/monaco.ttf", 40)

draw_tick_marks(45,315,14,160,240,200)

# Overarching state variables
rpm = 0
engineLoad = 0
throttle = 0
temp = 0
speed = 0
gear = 0



# Test code
if (test):
	while 1:
		for i in range(0,13000,50):
			inpt = linear_transform(i,0,13000,45,315)
			
			draw_screen()

			draw_indicator(inpt,190,160,240)

			angle = display_font.render(str(inpt)+u'\N{DEGREE SIGN}',1,white)
			rpm = rpm_font.render(str(i),1,white)

			screen.blit(angle,(470,40))
			screen.blit(rpm,(100,260))

			pygame.display.update()

# Gets serial values and animates the dashboard
if (not test):
	while 1:
		while (arduino.inWaiting() == 0):		# Waits for new data
			pass
		data = arduino.read()					# Reads next byte out of buffer

		# Packet Headers:
		# 0x30 : RPMs
		# 0x31 : Engine Load
		# 0x32 : throttle
		# 0x33 : Coolant Temp (F)
		# 0x34 : O2 level
		# 0x35 : Vehicle Speed (The shitty one from the ECU anyway)
		# 0x36 : Gear (Again, shitty ECU version)
		# 0x37 : Battery Voltage
		# 0x38 : Shock pot sensor on right rear wheel
		# 0x39 : Shock pot sensor on left rear wheel


		if (data == 0x21):		# Magic Number
			data = arduino.read()
			if (data == 0x30):		# RPM
				payload = struct.unpack('>f', arduino.read(4))
				print (payload)
				rpm = payload
			elif (data == 0x31):	# Engine Load
				payload = struct.unpack('>f', arduino.read(4))
				print (payload)
				engineLoad = payload
			elif (data == 0x32):	# Throttle
				payload = struct.unpack('>f', arduino.read(4))
				print (payload)
				throttle = payload
			elif (data == 0x33):	# Coolant Temp
				payload = struct.unpack('>f', arduino.read(4))
				print (payload)
				temp = payload
			elif (data == 0x35):	# Vehicle Speed
				payload = struct.unpack('>f', arduino.read(4))
				print (payload)
				speed = payload
			elif (data == 0x36):	# Gear
				gear = int(arduino.read(1))
				print (gear)
			else:
				print ("ERROR: Corrupted Data")

		# Animate using new data
		draw_screen()
		
		draw_indicator(linear_transform(rpm,0,13000,45,315),190,160,240)

		text = display_font.render(str(temp) + u'\N{DEGREE SIGN}',1,white)

		screen.blit(text,(470,40))

		pygame.display.update()












