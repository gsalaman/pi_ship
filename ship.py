################################################
# ship.py - Ship motion experiments 
#
# Input from MQTT wrapper 
# Just fly around.  :)
################################################# 

import time
from datetime import datetime

from gamepad_wrapper import Gamepad_wrapper

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


speed_delay = .1

###################################
# Ship Class
###################################
class Ship():
  def __init__(self, x, y):
    ship_color = green
   

    self.x = x  # x and y gonna be top-left corner of ship. 
    self.y = y  # orientation doesn't matter

    self.dir = 0   # 0 = Up, 1 = Up-right, 2=right...etc to 7=up-left

    self.ship_size = 3
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

  def erase(self):
    global matrix
    
    blank_image = Image.new("RGB", (3,3))
    matrix.SetImage(blank_image, self.x, self.y)

  def rotate_right(self):
    self.dir = self.dir + 1
    if (self.dir > 7):
      self.dir = 0

  def rotate_left(self):
    self.dir = self.dir - 1
    if (self.dir < 0):
      self.dir = 7

  def move(self):
    global matrix_rows
    global matrix_columns

    # dir = up
    if (self.dir == 0):
      new_x = self.x
      new_y = self.y - 1

    # dir = up-right
    elif (self.dir == 1):
      new_x = self.x + 1
      new_y = self.y - 1

    # dir = right
    elif (self.dir == 2):
      new_x = self.x + 1
      new_y = self.y

    # dir = down-right
    elif (self.dir == 3):
      new_x = self.x + 1
      new_y = self.y + 1

    # dir = down
    elif (self.dir == 4):
      new_x = self.x
      new_y = self.y + 1

    # dir = down-left
    elif (self.dir == 5):
      new_x = self.x - 1
      new_y = self.y + 1

    # dir = left
    elif (self.dir == 6):
      new_x = self.x - 1
      new_y = self.y

    # dir = up-left
    elif (self.dir == 7):
      new_x = self.x - 1 
      new_y = self.y - 1
    
    #invalid dir!!!
    else:
      print("Invalid dir in move!!!")
      exit(1) 
  
    # Make sure our new position isn't off the screen
    if ((new_x >= 0) and (new_x <= matrix_columns-self.ship_size)):
      self.x = new_x
    if ((new_y >= 0) and (new_y <= matrix_rows-self.ship_size)):
      self.y = new_y 

###################################
# Main loop 
###################################
init_image = Image.new("RGB", (total_columns, total_rows))
init_draw = ImageDraw.Draw(init_image)
init_draw.text((0,0),"Waiting for controller", fill=red)
matrix.SetImage(init_image, 0,0)

wrapper = Gamepad_wrapper(1)

while wrapper.player_count() != 1:
  time.sleep(0.001)

# blank the screen
init_draw.rectangle((0,0,total_columns,total_rows), fill=black)
matrix.SetImage(init_image, 0,0)

ship = Ship(5,5)
ship.rotate_right()
ship.show()

last_update_time = datetime.now()

while True:

  input = wrapper.get_next_input()
  if (input == None):
    key = None
  else:
    key = input[1]

  ship.erase()
  if (key == "left"):
    ship.rotate_left()
  elif (key == "right"):
    ship.rotate_right()
  elif (key == "up"):
    ship.move()
  ship.show() 

  time.sleep(speed_delay) 
