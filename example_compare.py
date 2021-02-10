# OKlab RGB NeoPixel Comparison for CircuitPython
# by Robert McMurray
# —
# https://github.com/rdmcmurray


import board
import neopixel
import oklab


# QtPy board specs
# Change to suit your board and LED setup

pixel_pin = board.A0
num_pixels = 30

pixels = neopixel.NeoPixel(pixel_pin, num_pixels)
pixels.brightness = 1


# Takes an rbg color
# Modifies the lightness in OKlab color space
# Returns rgb

def rgb_lab_rgb(c, lightness):
	ln_rgb = oklab.rgb_to_linear(c)
	ok_lab = oklab.linear_srgb_to_oklab(ln_rgb)

	# lightness: 0-1
	l = lightness
	# a is red-green: 0.25 to -0.25
	a = ok_lab[1]
	# b is blue-yellow: 0.25 to -0.25
	b = ok_lab[2]
	# assemble!
	py_lab = (l, a, b)

	ln_rgb = oklab.oklab_to_linear_srgb(py_lab)
	rgb = oklab.linear_to_rgb(ln_rgb)

	return rgb


# From Adafruit pypixelbuf
# Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.

def rgb_color_wheel(pos):
	if pos < 0 or pos > 255:
		return (0, 0, 0)
	if pos < 85:
		return (255 - pos * 3, pos * 3, 0)
	if pos < 170:
		pos -= 85
		return (0, 255 - pos * 3, pos * 3)
	pos -= 170
	return (pos * 3, 0, 255 - pos * 3)


# Runs the NeoPixel strip through a rainbow
# Half is normal RGB
# Half is normal RGB -> OKlab lightness modified -> RGB
# There is another example which starts in Lab space, but for comparison's sake we start with the same value

def compare_rgb_oklab():
	r = 255
	rc = range(r)
	rp = range(num_pixels)

	for i in rc:

		# Lightness is 0-1, black to white, so 0.5 is 100% unadulterated chroma
		# This lets us control perceived brightness without having to change the NeoPixel brightness, which would be slower
		new_lightness = 0.5

		c = rgb_color_wheel(i)
		d = rgb_lab_rgb(c, new_lightness)

		s = "Initial RGB: "
		s += str(c)
		s += "\t OKlab to RGB: "
		s += str(d)
		print(s)

		for p in rp:
			if p <= num_pixels / 2:
				pixels[p] = c

			elif p > num_pixels / 2:
				pixels[p] = d

while True:
	compare_rgb_oklab()
