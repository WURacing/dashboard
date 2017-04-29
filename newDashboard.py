# -*- coding: utf-8 -*-

# Authors: Michael Greer, Matthew Shepherd

# IMPORTANT FOR CIRCLE DEFINITION:
# We defined our unit circle as a mirror image of the standard unit circle.
# Circle starts at left and goes clockwise
# Code reflects this

###############################################################################################################

#####	Import statements	#####

import pygame 			# Graphics and Drawing Module
import serial			# Serial Library
import time				# For delays
import math				# sin, cos, etc
import struct			# For converting byte to float
import datetime			# For delta timing
import os				# For testing?
from subprocess import call 	#Used for calling external functions

#####	Initialize Libraries and Variable Declarations	  #####

### Initialize pygame
pygame.init()

### Initialize as Testing Mode or Reading Rode
# True => Testing
# False => Reading
test = True

### Initialize serial
if (not test): 
	ser = serial.Serial('/dev/ttyACM0',9600)

### [Overarching State Variable] Declarations
rpm = 0.0
display_rpm = 0.0
engineLoad = 0.0
throttle = 0.0
temp = 0.0
oxygen = 0.0
speed = 0.0
gear = 0
volts = 0.0 	# This is actually a running average of the voltage across 20 elements

buf_length = 50
volt_buf = [13] * buf_length;
buf_count = 0;
buf_sum = sum(volt_buf)

shutoff = False;

### Font Declarations
temp_font = pygame.font.Font("fonts/monaco.ttf", 40)
rpm_font = pygame.font.Font("fonts/Roboto-BlackItalic.ttf", 100)
warning_font = pygame.font.Font("fonts/Roboto-BlackItalic.ttf", 120)

### Important Constats
shift_rpm = 11500
high_temp = 210
low_battery = 12
redline_rpm = 12000


##### Function Definitions #####

### Maps a variable from one space to another
def linear_transform(input,rangeOneStart,rangeOneEnd,rangeTwoStart,rangeTwoEnd):
	return int((input-rangeOneStart)*(float(rangeTwoEnd-rangeTwoStart)/float(rangeOneEnd-rangeOneStart))+rangeTwoStart)

### Draws the RPM bar at the top of the screen
def draw_rpm_bar(i):
	inpt = linear_transform(i,0,13000,0,800)
	
	for j in range(0,inpt):
		colorInpt = linear_transform(j,0,800,0,13000)
		pygame.draw.line(screen, rpmColor(colorInpt), (j,0), (j,100), 1)


### Draws all parts of display that are not data-dependent
def draw_screen():
	screen.fill(black)
	
	#Bar line
	pygame.draw.line(screen, lgrey, (0,100),(800,100), 5)

### Smooths rpm readout
def smooth_rpm():
	global rpm, display_rpm
	
	display_rpm += (rpm-display_rpm)/2

### Draws the warning message for flashing warnings on the dashboard
def draw_warning_message(message, primary, secondary):
	pygame.draw.rect(screen, primary, (25,125,750,325))
	pygame.draw.rect(screen, secondary, (50,150,700,275))

###	This wasn't really doing what it was mean to 

	# if (message == "test"):
	# 	warning = warning_font.render("WARNING",1,white)
	# 	screen.blit(warning,(135,175))
		
	# else:
	# 	warning = warning_font.render("Hello!",1,white)
	# 	screen.blit(warning,(135,175))

	warning = warning_font.render(message,1,white)
	screen.blit(warning, (135,175));

### Reads data from bus
# All code taken from Thomas Kelly's implementation of readData() in serial_thread.py
def readData():
	global ser
	global rpm, engineLoad, throttle, temp, oxygen, speed, gear, volts
	if (ser.inWaiting() > 0):
		data = ser.read()
		if (data == bytes(b'!')):
			data = ser.read()
			# Packet Headers:
			# 0x30 : RPMs
			# 0x31 : Engine Load
			# 0x32 : throttle
			# 0x33 : Coolant Temp (F)
			# 0x34 : O2 level
			# 0x35 : Vehicle Speed (The shitty one from the ECU anyway)
			# 0x36 : Gear (Again, shitty ECU version)
			# 0x37 : Battery Voltage

			if (data == bytes(b'0')):
				payload = struct.unpack('>f',ser.read(4))[0]
				rpm = payload

			elif (data == bytes(b'1')):
				payload = struct.unpack('>f',ser.read(4))[0]
				engineLoad = payload

			elif (data == bytes(b'2')):
				payload = struct.unpack('>f',ser.read(4))[0]
				throttle = payload

			elif (data == bytes(b'3')):
				payload = struct.unpack('>f',ser.read(4))[0]
				temp = payload

			elif (data == bytes(b'4')):
				payload = struct.unpack('>f',ser.read(4))[0]
				oxygen = payload

			elif (data == bytes(b'5')):
				payload = struct.unpack('>f',ser.read(4))[0]
				speed = payload

			elif (data == bytes(b'6')):
				payload = ord(struct.unpack('c',ser.read())[0])
				gear = payload

			elif (data == bytes(b'7')):
				payload = struct.unpack('>f',ser.read(4))[0]
				voltageUpdate(payload)


			else:
				print("ERROR: Corrupted Data")
		else:
			pass
	else:
		pass

# Used to turn off the RPi when the battery voltage gets critically low
def lowBatteryShutoff():
	shutoff = True;
	call(["shutdown"])	# Executes the shutdown function

def voltageUpdate(vInput):

	buf_count %= buf_length

	buf_sum -= volt_buf[buf_count]

	volt_buf[buf_count] = vInput;

	buf_sum += volt_buf[buf_count]

	volts = buf_sum/float(buf_length)

	buf_count += 1

	if (volts < low_battery):

		lowBatteryShutoff()


### OBSOLETE ####

# # Draws pointer on dials
# def draw_indicator(angle,length,center_x,center_y):
# 
# 	x_len = math.cos(math.radians(angle))*float(length) # Finds the x and y compoents of the length
# 	y_len = math.sin(math.radians(angle))*float(length) 
# 
# 	x_pos = center_x - x_len # Finds the x and y 
# 	y_pos = center_y - y_len
# 	
# 	inner_x_pos = int(center_x-(.6*x_len))										# x coordinate of inside point
# 	inner_y_pos = int(center_y-(.6*y_len))
# 
# 	pygame.draw.line(screen,red,(inner_x_pos,inner_y_pos),(x_pos,y_pos),10)
# 
# # Draws tick marks along the outside of circles
# def draw_tick_marks(startAngle,stopAngle,numMarks,center_x,center_y,radius):
# 
# 	angle_diff = stopAngle-startAngle												# Value of the difference between the start and stop angles
# 	spacing = float(angle_diff)/float(numMarks-1)									# Angle spacing between each mark
# 
# 	for mark in range(numMarks): 													# Loops through each tick mark
# 		current_angle=startAngle+(spacing*float(mark))								# Current angle for this tick mark
# 		y_len = math.sin(math.radians(current_angle))*radius						# y component of length
# 		x_len = math.cos(math.radians(current_angle))*radius						# x component of length
# 
# 		x_pos = int(center_x - x_len)												# x coordinate of outside point
# 		y_pos = int(center_y - y_len)												# y coordinate of outside point
# 
# 		inner_x_pos = int(center_x-(.9*x_len))										# x coordinate of inside point
# 		inner_y_pos = int(center_y-(.9*y_len))										# y coordinate of inside point
# 
# 		num_x_pos = int(center_x-(.8*x_len))
# 		num_y_pos = int(center_y-(.8*y_len))
# 
# 		#print x_pos, y_pos, inner_x_pos, inner_y_pos								# debug
# 
# 		pygame.draw.line(screen,white,(x_pos,y_pos),(inner_x_pos,inner_y_pos),6)	# draws tick mark
# 
# 		num = font.render(str(mark),1,white)
# 
# 		(num_width,num_height) = font.size(str(num))
# 
# 		screen.blit(num,(num_x_pos-5,num_y_pos-(num_height/2)))
# 
# # Draws redline on outside of circle
# def draw_redline_arc(startAngle,stopAngle,center_x,center_y,radius):
# 
# 	rect = (center_x-radius,center_y-radius,2*radius,2*radius)		# Defines the rectangle to draw arc in
# 
# 	start_radians = math.radians((-stopAngle)+180)					# Converts between our "unit circle" and standard unic circle
# 	stop_radians = math.radians((-startAngle)+180)
# 
# 	pygame.draw.arc(screen,red,rect,start_radians,stop_radians,10)	# Draws Arc
#

#### END OBSOLETE ####




######	Color Definitions	######
red = 	(255,0,0)
black = (0,0,0)
grey = 	(100,100,100)
lgrey=	(150,150,150)
green = (0,120,0)
white = (255,255,255)

#Returns the color of the RPM bar depending on the RPM
def rpmColor(n):
	# HSLA formatting	
	inpt = linear_transform(n,0,13000,100,0)
	color = pygame.Color(255)
	color.hsla = (inpt,100,50,0)
	return color




#####	MAIN CODE	#####

# Setup Screen
display_size=width, height=800,480 # Size of the Adafruit screen
screen = pygame.display.set_mode(display_size)
#pygame.display.toggle_fullscreen() # Sets display mode to full screen

# More Screen Setup (I dunno what this does? artifact from old code?)
screen.fill(green)
pygame.display.flip()

# Final Screen Serup
screen.fill(grey)

# Display Logo (doesn't work on my laptop for some reason; uncomment to display)
img = pygame.image.load("WURacing-Logo-Big.png")
img = pygame.transform.scale(img, (600,480))
screen.blit(img, (400,0))
time.sleep(5)


###		Testing Mode	 ###
if (test):

# 	Setup for warning delta timing
	warning_state = True
	previousTime = datetime.datetime.now()
	
	while 1:
		for i in range(0,13000,50):
			inpt = linear_transform(i,0,13000,0,800)
			inptTemp = linear_transform(i,0,13000,45,315)
			draw_screen()
			draw_rpm_bar(i)
			
# 			Get Raw Input RPM
			txtrpm = rpm_font.render(str(int(i)),1,white)
			
# 			Readability RPM (I prefer this formatting; replace line above to implement
# 			txtrpm = rpm_font.render((str(int(i / 1000)) + "." + str(int((i % 1000) / 100)) + "k"),1,white)

# 			Draw Raw Input RPM (Always text-centered)
			if (i < 100):
				screen.blit(txtrpm,(355,180))
			elif (i < 1000):
				screen.blit(txtrpm,(320,180))
			elif (i < 10000):
				screen.blit(txtrpm,(285,180))
			else:
				screen.blit(txtrpm,(250,180))
			
# 			Draw Temperature
			txttemp = temp_font.render((str(int(inptTemp)) + "\xb0"),1,white)
			screen.blit(txttemp,(80,375))
			
# 			Delta Timing for warning message
			currentTime = datetime.datetime.now()
			deltaTime = currentTime - previousTime
			
			
###			Warning Message Code
	
# 			Flashing Message State Machine
			if (deltaTime.microseconds > 500000):
				if (warning_state):
					# Draw State
					warning_state = False
					previousTime = datetime.datetime.now()
				else:
 					# Don't Draw State
					warning_state = True
					previousTime = datetime.datetime.now()
			
# 			Draw/Don't Draw depending on state
			if (warning_state):
				draw_warning_message("test",red,grey)
			 
			pygame.display.update()


###		Reading Mode	 ###
# Gets serial values and animates the dashboard
if (not test):
	ser.flush()
	warning_state = True
	previousTime = datetime.datetime.now()

	while (True):

		draw_screen()
		draw_rpm_bar(rpm)

#			Check for warnings
		redline = rpm > redline_rpm
		shift 	= rpm > shift_rpm
		overheat= temp > high_temp

		
# 			Get Raw Input RPM
		txtrpm = rpm_font.render(str(int(rpm)),1,white)
		
# 			Readability RPM (I prefer this formatting; replace line above to implement
# 			txtrpm = rpm_font.render((str(int(i / 1000)) + "." + str(int((i % 1000) / 100)) + "k"),1,white)

# 			Draw Raw Input RPM (Always text-centered)
		if (rpm < 100):
			screen.blit(txtrpm,(355,180))
		elif (rpm < 1000):
			screen.blit(txtrpm,(320,180))
		elif (rpm < 10000):
			screen.blit(txtrpm,(285,180))
		else:
			screen.blit(txtrpm,(250,180))
		
# 			Draw Temperature
		txttemp = temp_font.render((str(int(temp)) + "\xb0"),1,white)
		screen.blit(txttemp,(80,375))
		
# 			Delta Timing for warning message
		currentTime = datetime.datetime.now()
		deltaTime = currentTime - previousTime
		
		
###			Warning Message Code

# 			Flashing Message State Machine
		if (deltaTime.microseconds > 500000):
			if (warning_state):
				# Draw State
				warning_state = False
				previousTime = datetime.datetime.now()
			else:
					# Don't Draw State
				warning_state = True
				previousTime = datetime.datetime.now()
		
# 			Draw/Don't Draw depending on state
		if (warning_state and shutoff):
			draw_warning_message("SHUTOFF",red,grey)
		elif (warning_state and redline):
			draw_warning_message("REDLINE",red,grey)
		elif (warning_state and overheat):
			draw_warning_message("OVERHEAT",red,grey)
		elif (warning_state and shift):
			draw_warning_message("SHIFT",green,grey)
		 
		pygame.display.update()

		readData()

#		print ("end of while loop")
