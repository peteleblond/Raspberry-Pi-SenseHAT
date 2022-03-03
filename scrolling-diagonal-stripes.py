from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

y = (255, 255, 0) #Yellow
b = (0, 0, 0) # Black

smiley_face = [
   y, y, y, y, y, y, y, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, b, b, y, y, b, b, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, y, y, b, b, y, y, y,
   y, y, y, y, y, y, y, y
]

frowning_face = [
   y, y, y, y, y, y, y, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, b, b, y, y, b, b, y,
   y, y, y, y, y, y, y, y,
   y, y, y, b, b, y, y, y,
   y, y, b, y, y, b, y, y,
   y, b, y, y, y, y, b, y
]

stripes_1 = [
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b,
   y, b, b, y, y, b, b, y,
   b, b, y, y, b, b, y, y,
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b,
   y, b, b, y, y, b, b, y,
   b, b, y, y, b, b, y, y
]

stripes_2 = [
   b, b, y, y, b, b, y, y,
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b,
   y, b, b, y, y, b, b, y,
   b, b, y, y, b, b, y, y,
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b,
   y, b, b, y, y, b, b, y
]

stripes_3 = [
   y, b, b, y, y, b, b, y,
   b, b, y, y, b, b, y, y,
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b,
   y, b, b, y, y, b, b, y,
   b, b, y, y, b, b, y, y,
   b, y, y, b, b, y, y, b,
   y, y, b, b, y, y, b, b
]

while True:
   sense.set_pixels(stripes_1)
   sleep(0.1)
   sense.set_pixels(stripes_2)
   sleep(0.1)
   sense.set_pixels(stripes_3)
   sleep(0.1)
