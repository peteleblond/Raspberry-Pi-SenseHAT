from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

red = (255, 0, 0)
green = (0, 255, 0)

y = (255, 255, 0) #Yellow
b = (0, 0, 0) # Black

stripes_1 = [
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y
]

stripes_2 = [
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y
]

stripes_3 = [
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y
]

stripes_4 = [
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b
]

stripes_5 = [
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b
]

stripes_6 = [
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, y,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b
]


while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = abs(x)
    y = abs(y)
    z = abs(z)

    if x > 1.5 or y > 1.5 or z > 1.5:
        count = 0
        while count < 3:
            sense.set_pixels(stripes_1)
            sleep(0.1)
            sense.set_pixels(stripes_2)
            sleep(0.1)
            sense.set_pixels(stripes_3)
            sleep(0.1)
            sense.set_pixels(stripes_4)
            sleep(0.1)
            sense.set_pixels(stripes_5)
            sleep(0.1)
            sense.set_pixels(stripes_6)
            sleep(0.1)
            count += 1
    else:
        sense.clear()
        sleep(0.5)
        sense.show_letter(".", green)
