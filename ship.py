################################################
# ship.py - Ship motion experiments 
#
# Input from MQTT wrapper 
# Just fly around.  :)
################################################# 

import time
from datetime import datetime

#from gamepad_wrapper import Gamepad_wrapper

###################################
# Graphics imports, constants and structures
###################################
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from matrix import read_matrix

# open the config file and read the size of our matrix
matrix_data = read_matrix()

# this is the size of ONE of our matrixes. 
matrix_rows = matrix_data[1] 
matrix_columns = matrix_data[0] 

# how many matrixes stacked horizontally and vertically 
matrix_horizontal = matrix_data[2] 
matrix_vertical = matrix_data[3] 

total_rows = matrix_rows * matrix_vertical
total_columns = matrix_columns * matrix_horizontal

options = RGBMatrixOptions()
options.rows = matrix_rows 
options.cols = matrix_columns 
options.chain_length = matrix_horizontal
options.parallel = matrix_vertical 
options.hardware_mapping = 'regular'  
options.gpio_slowdown = 2

matrix = RGBMatrix(options = options)

###################################################
# global data
# Update this comment!!!
###################################################

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (0,255,255)
purple = (255,0,255)

ship_color = green

speed_delay = .1

###################################
# Ship Class
###################################
class Ship():
  def __init__(self, x, y):
    global ship_color

    self.x = x  # x and y gonna be top-left corner of ship. 
    self.y = y  # orientation doesn't matter

    self.dir = 0   # 0 = Up, 1 = Up-right, 2=right...etc to 7=up-left

    self.image = Image.new("RGB", (3,3))
    self.draw  = ImageDraw.Draw(self.image)

    self.draw.line((1,0,0,2),fill=ship_color)
    self.draw.line((1,0,2,2),fill=ship_color)

    self.images = []
    self.images.append(self.image)

    self.base_image_45 = Image.new("RGB", (3,3))
    draw_45 = ImageDraw.Draw(self.base_image_45)
    draw_45.line((0,0,2,0),fill=ship_color)
    draw_45.line((2,0,2,2),fill=ship_color)
  
    self.images.append(self.base_image_45)

    self.images.append(self.image.rotate(-90))
    self.images.append(self.base_image_45.rotate(-90))

    self.images.append(self.image.rotate(180))
    self.images.append(self.base_image_45.rotate(180))

    self.images.append(self.image.rotate(90))
    self.images.append(self.base_image_45.rotate(90))

  def show(self):
    global matrix

    matrix.SetImage(self.images[self.dir], self.x, self.y)

  def rotate_right(self):
    self.dir = self.dir + 1
    if (self.dir > 7):
      self.dir = 0

  def rotate_left(self):
    self.dir = self.dir - 1
    if (self.dir < 0):
      self.dir = 7

  def move(self):
    pass

###################################
# Main loop 
###################################

#wrapper = Gamepad_wrapper(1)

ship = Ship(5,5)
ship.show()

while True:
  time.sleep(1) 
  ship.rotate_left() 
  ship.show()
