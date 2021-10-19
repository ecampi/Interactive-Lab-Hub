from __future__ import print_function
import qwiic_joystick
import time
import sys

#things for the display:
from time import strftime, sleep
import subprocess
import digitalio
import board
import PIL
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random

def runExample():
	#setting up the display:

	cs_pin = digitalio.DigitalInOut(board.CE0)
	dc_pin = digitalio.DigitalInOut(board.D25)
	reset_pin = None
	BAUDRATE = 64000000  
	disp = st7789.ST7789(
		board.SPI(),
		cs=cs_pin,
		dc=dc_pin,
		rst=reset_pin,
		baudrate=BAUDRATE,
		width=135,
		height=240,
		x_offset=53,
		y_offset=40,
	)
	height = disp.width  
	width = disp.height
	image = Image.new("RGB", (width, height))
	rotation = 90
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image, rotation)
	padding = -2
	backlight = digitalio.DigitalInOut(board.D22)
	backlight.switch_to_output()
	backlight.value = True
	fontHehe = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
	buttonA = digitalio.DigitalInOut(board.D23)
	buttonA.switch_to_input()
	fillHour = "#FF0000"



	#joystick stuff:
	print("\nSparkFun qwiic Joystick   Example 1\n")
	myJoystick = qwiic_joystick.QwiicJoystick()

	if myJoystick.connected == False:
		print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myJoystick.begin()

	print("Initialized. Firmware Version: %s" % myJoystick.version)

	while True:

		if myJoystick.vertical == 0:
			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			draw.text((0,20), "UP", fill=fillHour, font=fontHehe)
			disp.image(image, rotation)
		elif myJoystick.vertical == 1023:
			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			draw.text((0,20), "DOWN", fill=fillHour, font=fontHehe)
			disp.image(image, rotation)
		else:
			draw.rectangle((0, 0, width, height), outline=0, fill=0)
			disp.image(image, rotation)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)