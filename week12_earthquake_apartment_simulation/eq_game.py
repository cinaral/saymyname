import ipycanvas as ipc
#import ipyevents as ipe

from ipywidgets import Image

from time import time, sleep
from threading import Thread

import numpy as np
#from scipy.integrate import odeint
#import sympy as sy

class Game(Thread):
    def __init__(self, x0, dx0, update_building, t0=0, fps=30, canvas_width=900, canvas_height=300, meter_in_pixels=10):
        self.dt = 1 / fps # simulation timestep
        self.x = x0
        self.dx = dx0
        self.update_building = update_building
        self.time = t0
        self.is_running = True
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.meter_in_pixels = meter_in_pixels # how many pixels one meter corresponds to, defines the scale  
        self.init_pos = np.array([self.canvas_width / 2, self.canvas_height])
        self.canvas = ipc.MultiCanvas(3, width=self.canvas_width, height=self.canvas_height)
        super(Game, self).__init__()
     
    # main loop
    def run(self):
        frame_time = self.dt
        start_time = time()
        while(self.is_running):
            tick = time()
            self.x = self.update_building(self.x, self.dx, self.dt)
            self.draw_building(self.canvas, self.x, self.canvas_width, self.canvas_height)
            self.time = tick - start_time 
            self.fps = 1 / frame_time
            if self.dt - (time() - tick) > 0:
                sleep(self.dt - (time() - tick))
            frame_time = time() - tick
            
    # stop game 
    def stop(self):
        self.is_running = False
    
    # convert meters to pixels 
    def to_pixels(self, distance_in_meters):
        return distance_in_meters * self.meter_in_pixels    
    
    def draw_building(self, canvas, x, canvas_width, canvas_height):
        
        sprite1 = Image.from_file('houseBeige.png')
        sprite2 = Image.from_file('houseBeigeAlt.png')
        sprite3 = Image.from_file('houseBeigeAlt2.png')
        sprite4 = Image.from_file('houseBeigeBottomLeft.png')
        sprite5 = Image.from_file('houseBeigeBottomMid.png')
        sprite6 = Image.from_file('houseBeigeBottomRight.png')
        sprite7 = Image.from_file('houseBeigeMidLeft.png')
        sprite8 = Image.from_file('houseBeigeMidRight.png')
        sprite9 = Image.from_file('houseBeigeTopLeft.png')
        sprite10 = Image.from_file('houseBeigeTopRight.png')
        
        #for i in np.arange(0,10):
            #x[i][0] = self.to_pixels(x[i][0])
        
        #pos = 1 * self.init_pos
        #pos[0] = pos[0] - x[i][0]
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas[1].translate(+x[0][0], 0)
            canvas[2].translate(+x[1][0], 0)
            canvas[3].translate(+x[2][0], 0)
            canvas[4].translate(+x[3][0], 0)
            canvas[5].translate(+x[4][0], 0)
            canvas[6].translate(+x[5][0], 0)
            canvas[7].translate(+x[6][0], 0)
            canvas[8].translate(+x[7][0], 0)
            canvas[9].translate(+x[8][0], 0)
            canvas[10].translate(+x[9][0], 0)
            canvas[1].draw_image(sprite1, 300, 250)#m1
            canvas[2].draw_image(sprite2, 300, 225)#m2
            canvas[3].draw_image(sprite3, 300, 200)#m3
            canvas[4].draw_image(sprite4, 300, 175)#m4
            canvas[5].draw_image(sprite5, 300, 150)#m5
            canvas[6].draw_image(sprite6, 300, 125)#m6
            canvas[7].draw_image(sprite7, 300, 100)#m7
            canvas[8].draw_image(sprite8, 300, 75)#m8
            canvas[9].draw_image(sprite9, 300, 50)#m9
            canvas[10].draw_image(sprite10, 300, 25)#m10
            canvas[1].translate(-x[0][0], 0)
            canvas[2].translate(-x[1][0], 0)
            canvas[3].translate(-x[2][0], 0)
            canvas[4].translate(-x[3][0], 0)
            canvas[5].translate(-x[4][0], 0)
            canvas[6].translate(-x[5][0], 0)
            canvas[7].translate(-x[6][0], 0)
            canvas[8].translate(-x[7][0], 0)
            canvas[9].translate(-x[8][0], 0)
            canvas[10].translate(-x[9][0], 0)
            
            
##            canvas[1].fill_rect(300, 25, 30, 25) # x10 for m10
##            canvas[1].translate(+x[9][0], 0)
##            canvas[2].fill_rect(300, 50, 30, 25) # x9 for m9
##            canvas[2].translate(+x[8][0], 0)
##            canvas[3].fill_rect(300, 75, 30, 25) # x8 for m8
##            canvas[3].translate(+x[7][0], 0)
##            canvas[4].fill_rect(300, 100, 30, 25) # x7 for m7
##            canvas[4].translate(+x[6][0], 0)
##            canvas[5].fill_rect(300, 125, 30, 25) # x6 for m6
##            canvas[5].translate(+x[5][0], 0)
##            canvas[6].fill_rect(300, 150, 30, 25) # x5 for m5
##            canvas[6].translate(+x[4][0], 0)
##            canvas[7].fill_rect(300, 175, 30, 25) # x4 for m4
##            canvas[7].translate(+x[3][0], 0)
##            canvas[8].fill_rect(300, 200, 30, 25) # x3 for m3
##            canvas[8].translate(+x[2][0], 0)
##            canvas[9].fill_rect(300, 225, 30, 25) # x2 for m2
##            canvas[9].translate(+x[1][0], 0)
##            canvas[10].fill_rect(300, 250, 30, 25) # x1 for m1
##            canvas[10].translate(+x[0][0], 0)
        

