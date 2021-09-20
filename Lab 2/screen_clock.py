from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

fontHehe = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()
fillHour = "#FF0000"
fillMinute = "#FFA500"
fillSecond = "#FFFF00"

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py
    #hello

    if not buttonA.value:
        random_hour = random.randint(0,16777215)
        random_minute = random.randint(0,16777215)
        random_second = random.randint(0,16777215)
        hex_hour = str(hex(random_hour))
        hex_minute = str(hex(random_minute))
        hex_second = str(hex(random_second))
        fillHour = "#" + hex_hour[2:]
        fillMinute = "#" + hex_minute[2:]
        fillSecond = "#" + hex_second[2:]
        if len(fillHour) != 7:
            fillHour = fillHour + "0"
        if len(fillMinute) != 7:
            fillMinute = fillMinute + "0"
        if len(fillSecond) != 7:
            fillSecond = fillSecond + "0"

    timeString = strftime("%H:%M:%S")
    timeList = timeString.split(":")
    times = []
    for time in timeList:
        times.append(int(time))

    ideal = [16,37,0]

    if ideal[0] == 0:
        ideal[0] = 12

    if ideal[1] == 0:
        ideal[0] -= 1
        ideal[1] = 60

    if ideal[2] == 0:
        ideal[1] -= 1
        ideal[2] = 60

    new = []
    for i in range(len(ideal)):
        new.append(ideal[i] - times[i])
    
    if new[0] < 0 or new[1] < 0:
        new[0] = 23 + new[0]
        new[1] = 60 + new [1]

    textHour = str(new[0])
    draw.text((0,20), textHour, fill=fillHour, font=fontHehe)

    textMinute = str(new[1])
    draw.text((90,20), textMinute, fill=fillMinute, font=fontHehe)

    textSecond = str(new[2])
    draw.text((180,20),textSecond, fill=fillSecond, font=fontHehe)

    # Display image.
    disp.image(image, rotation)
    sleep(1)
