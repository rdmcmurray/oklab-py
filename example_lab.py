# OKlab NeoPixel Lab Color Cycling for CircuitPython
# by Robert McMurray
# —
# https://github.com/rdmcmurray


import math
import board
import neopixel
import oklab


# QtPy board specs
# Change to suit your board and LED setup

pixel_pin = board.A0
num_pixels = 30

pixels = neopixel.NeoPixel(pixel_pin, num_pixels)
pixels.brightness = 1


# For iterating in while True:

period = 1023
period_range = range(period)


# This function rotates through the lab color space
# A helpful visual is to imagine a circle drawn over the color square on this page:
# https://observablehq.com/@fil/oklab-color-space
# Given a value from 0-period, it returns a lab color along the circumference of the circle

def radial_lab(x, period, offset=0):
	circumference = 2 * math.pi
	# Current position along the circumference
	angle = (x + offset) / period * circumference
	# Chroma 0-0.5
	# Can be thought of as the radius of the circle
	# It controls how evenly the color transitions
	chroma = 0.25
	# Lightness is 0-1, black to white, so 0.5 is 100% unadulterated chroma
	# This lets us control perceived brightness without having to change the NeoPixel brightness, which would be slower	
	l = 0.5
	# a is red-green: 0.25 to -0.25
	a = chroma * math.cos(angle)
	# b is blue-yellow: 0.25 to -0.25
	b = chroma * math.sin(angle)

	return (l, a, b)


# Get OKlab color based on our position in a range
# Change that to linear RGB, then to RGB
# Assign all NeoPixels and display

def rainbow(x, period):
	c = radial_lab(x, period)
	s = "Lab: "
	s += str(c)
	c = oklab.oklab_to_linear_srgb(c)
	c = oklab.linear_to_rgb(c)
	s += "\t RGB: "
	s += str(c)

	print(s)

	pixels.fill(c)
	pixels.show()


while True:
	for i in period_range:
		rainbow(i, period)
