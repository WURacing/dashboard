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

# Is this a test or not.
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

# maps a variable from one space to another
def linear_transform(input,rangeOneStart,rangeOneEnd,rangeTwoStart,rangeTwoEnd):

	return int((input-rangeOneStart)*(float(rangeTwoEnd-rangeTwoStart)/float(rangeOneEnd-rangeOneStart))+rangeTwoStart)

# Draw a warning message to the screen.
def draw_warning_message(msg,primaryColor,secondaryColor):

	#if you're using a different display resolution than 800x400, these constants must be changed 
	warning_width = 600
	warning_height = 300
	base_x = 100 # x coord for upper left corner of warning
	base_y = 100  # y coord for upper left corner of warning

	pygame.draw.rect(screen, primaryColor, (base_x,base_y,warning_width,warning_height))


	#draw the borders to the warning
	line_width = 20
	line_width_add = line_width/2.22 # additional amount to add to x or y when drawing lines to account for line width
	pygame.draw.line(screen, secondaryColor, (base_x, base_y+line_width_add), (base_x+.25*warning_width, base_y+line_width_add), line_width)
	pygame.draw.line(screen, secondaryColor, (base_x+line_width_add, base_y), (base_x+line_width_add, base_y+.25*warning_height), line_width)
	#pygame.draw.line(screen, red, (150,75), (100,150), 20)

	# pygame.draw.line(screen,white,(x_pos,y_pos),(inner_x_pos,inner_y_pos),6)

# Draw the bar for displaying rpm
def draw_rpm_bar(i):
	inpt = linear_transform(i,0,13000,0,800)	
	for j in range(0,inpt):
		colorInpt = linear_transform(j,0,800,0,13000)
		pygame.draw.line(screen, rpmColor(colorInpt), (j,0), (j,100), 1)


############# Color Definitions
red =   (255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
green = (0,120,0)
white = (255,255,255)
###############################


def rgbToHsl(r,g,b):
	r /= float (255)
	g /= float (255)
	g /= float (255)

	maxVal = max(r,g,b)
	minVal = min(r,g,b)
	l = (maxVal + minVal) / float (2)
	s = None
	h = None

	if maxVal == minVal:
		h = 0
		s = 0
	else:
		temp = 0
		if g < b:
			temp = 6
		else:
			temp = 0

		diff = maxVal - minVal
		if s > .5:
			s = diff / (2-maxVal-minVal)
		else:
			s = diff / (maxVal+minVal)
		if maxVal == r:
			h = (g - b)/diff + temp
		elif maxVal == g:
			h =  (b - r)/diff + 2
		elif maxVal == b:
			h = (r - g)/diff +4

		h /=6
	print(h)
	print(s)
	print(l)
	return [h,s,l]

def rpmColor(n):
	inpt = linear_transform(n,0,13000,0,255)
	if (inpt < 100):
		return (		100+(inpt/2),			200-(inpt/2),			0)
	elif (inpt < 200):
		return (		150+((inpt-100)/2),		150-((inpt-100)),		0)
	elif (inpt < 250):
		return (		200+(inpt-200),			50-(inpt-200),			0)
	else:
		return (		250,					0,						0)

###############################



rgbToHsl(123,5,0)
pygame.init()

font = pygame.font.Font("fonts/OpenSans-Regular.ttf", 24)

display_size=width, height=800,480 # Size of the Adafruit screen

screen = pygame.display.set_mode(display_size)

if(not test):

	pygame.display.toggle_fullscreen() # Sets display mode to full screen

# Display Logo
img = pygame.image.load("WURacing-Logo-Big.png")
img = pygame.transform.scale(img, (600,480))
screen.blit(img, (100,0))
pygame.display.flip()
time.sleep(1)


screen.fill(black)

#display_font = pygame.font.Font("fonts/monaco.ttf", 120)
rpm_font = pygame.font.Font("fonts/Roboto-BlackItalic.ttf", 100)


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
		for i in range(0,13000):
			screen.fill(black)
			draw_rpm_bar(i)
			#pygame.draw.circle(screen, black, (160, 240), 200, 0)
			#draw_redline_arc(305,315,160,240,200)
			#draw_tick_marks(45,315,14,160,240,200)
			#draw_indicator(i,190,160,240)

			#pygame.draw.rect(screen, green, (400,20,300,190))
			#pygame.draw.rect(screen, green, (400,270,300,190))


			# if i>500:
			# 	print("time to shift")
			# 	draw_warning_message("test", white, red)

			text = rpm_font.render(str(i),1,white)
			#rpmText = rpm_font.render(str(i),white)


			screen.blit(text,(280,180))

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

		if (data == 0x30):		# RPM
			payload = struct.unpack('f', arduino.read(4))
			print (payload)
			rpm = payload
		elif (data == 0x31):	# Engine Load
			payload = struct.unpack('f', arduino.read(4))
			print (payload)
			engineLoad = payload
		elif (data == 0x32):	# Throttle
			payload = struct.unpack('f', arduino.read(4))
			print (payload)
			throttle = payload
		elif (data == 0x33):	# Coolant Temp
			payload = struct.unpack('f', arduino.read(4))
			print (payload)
			temp = payload
		elif (data == 0x35):	# Vehicle Speed
			payload = struct.unpack('f', arduino.read(4))
			print (payload)
			speed = payload
		elif (data == 0x36):	# Gear
			gear = int(arduino.read(1))
			print (gear)
		else:
			print ("ERROR: Corrupted Data")

		# Animate using new data
		pygame.draw.circle(screen, black, (160, 240), 200, 0)
		draw_redline_arc(305,315,160,240,200)
		draw_tick_marks(45,315,14,160,240,200)
		draw_indicator(linear_transform(rpm,0,13000,45,315),190,160,240)

		pygame.draw.rect(screen, green, (400,20,300,190))
		pygame.draw.rect(screen, green, (400,270,300,190))

		text = display_font.render(u'\N{DEGREE SIGN}',1,white)

		screen.blit(text,(420,40))

		pygame.display.update()












