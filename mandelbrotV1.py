# Python code for Mandelbrot Fractal

# Import necessary libraries
import threading
import colorsys
import time

from PIL import Image
from numpy import array
from yaspin import yaspin
from yaspin.spinners import Spinners


# setting the width of the output image as 1024
MAX_ITERS = 1000 * 100

# a function to return a tuple of colors
# as integer value of rgb
def rgb_conv(i):
    color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5))
    return tuple(color.astype(int))


# function defining a mandelbrot
def mandelbrot(x, y):
    c0 = complex(x, y)
    c = 0
    # iterator value somehow controls pixel color
    for i in range(1, MAX_ITERS):
        if abs(c) > 2:
            return rgb_conv(i)
        c = c * c + c0
    return (0, 0, 0)

# lock = threading.Lock()

w = 1024
h = 1024 # not using this yet
wh = w * h
numThr = 4 # number of threads to run

# creating the new image in RGB mode
img = Image.new('RGB', (w, int(w / 2)))
pixels = img.load()

class ManFrThread(threading.Thread): 
    def __init__ (self, k):
          self.k = k
          threading.Thread.__init__(self)

    def run(self):
        # each thread only calculates its own share of pixels
        for i in range(k, wh, numThr):
            kx = i % w
            ky = int(i / w)

            mx = (kx - (0.75 * w)) / (w / 4)
            my = (ky - (w / 4)) / (w / 4)
            
            pixels[kx, ky] = mandelbrot(mx, my)
            

if __name__ == "__main__":
    tArr = []
    for k in range(numThr): # create all threads
        print("starting thread: %d" % k)
        tArr.append(ManFrThread(k))
    for k in range(numThr): # start all threads
        tArr[k].start()
    
    with yaspin(
    Spinners.bouncingBall,
    color="magenta",
    on_color="on_cyan",
    attrs=["bold", "blink"],
    ) as sp:
        sp.text = "Building Mandelbrot set"

        start = time.time()
        for k in range(numThr): # wait until all threads finished
            tArr[k].join()
        end = time.time()
        print("Time elsasped %f s" % (end - start) )
        
        # to display the created fractal after computation
        img.show()
        img.save("mandel-v1.png")

    # for x in range(img.size[0]):

    #     # displaying the progress as percentage
    #     perct = (x / WIDTH * 100.0)

    #     # print("%.2f %%" % perct)
    #     for y in range(img.size[1]):
    #         mx = (x - (0.75 * WIDTH)) / (WIDTH / 4)
    #         my = (y - (WIDTH / 4)) / (WIDTH / 4)
    #         pixels[x, y] = mandelbrot(mx, my)
