# Oklab color space convenience library for python
# collated by Robert McMurray
# —
# https://github.com/rdmcmurray


import math


# Helper functions for color space conversion between Oklab and RGB
# by Robert McMurray

def rgb_to_linear(c):
	return (
		f_inv(c[0] / 255), 
		f_inv(c[1] / 255), 
		f_inv(c[2] / 255)
	)

def linear_to_rgb(c):
	return (
		clip_rgb(255 * f(c[0])), 
		clip_rgb(255 * f(c[1])), 
		clip_rgb(255 * f(c[2]))
	)

def clip_rgb(x):
	if x > 255:
		return 255
	elif x < 0:
		return 0

	return int(x)

# Linear conversions for RGB
# by Björn Ottosson
# python-ized by Robert McMurray
# —
# https://bottosson.github.io/posts/colorwrong/#what-can-we-do%3F

def f(x):
	if (x >= 0.0031308):
		return (1.055) * math.pow(x, (1.0/2.4)) - 0.055
	else:
		return 12.92 * x

def f_inv(x):
	if (x >= 0.04045):
		return math.pow(((x + 0.055)/(1 + 0.055)), 2.4)
	else:
		return x / 12.92

# Oklab conversions for linear RGB values
# by Björn Ottosson
# python-ized by Robert McMurray
# —
# https://bottosson.github.io/posts/oklab/#converting-from-linear-srgb-to-oklab

def linear_srgb_to_oklab(c):
	l = 0.4121656120 * c[0] + 0.5362752080 * c[1] + 0.0514575653 * c[2]
	m = 0.2118591070 * c[0] + 0.6807189584 * c[1] + 0.1074065790 * c[2]
	s = 0.0883097947 * c[0] + 0.2818474174 * c[1] + 0.6302613616 * c[2]

	l_ = l**(1./3.)
	m_ = m**(1./3.)
	s_ = s**(1./3.)

	return (
		0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
		1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
		0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_,
	)

def oklab_to_linear_srgb(c):
	l_ = c[0] + 0.3963377774 * c[1] + 0.2158037573 * c[2]
	m_ = c[0] - 0.1055613458 * c[1] - 0.0638541728 * c[2]
	s_ = c[0] - 0.0894841775 * c[1] - 1.2914855480 * c[2]

	l = l_*l_*l_
	m = m_*m_*m_
	s = s_*s_*s_

	return (
		+ 4.0767245293*l - 3.3072168827*m + 0.2307590544*s,
		- 1.2681437731*l + 2.6093323231*m - 0.3411344290*s,
		- 0.0041119885*l - 0.7034763098*m + 1.7068625689*s,
	)

