from ipywidgets import Image
import ipycanvas as ipc
from time import time, sleep
from threading import Thread

import numpy as np

class Game(Thread):
    def __init__(self, x0 , dx0 , y0, dy0, update_carchase, spacing, tire_d , car_l, t0=0, fps=15,canvas_width=910, canvas_height=300, meter_in_px0=260/4.5):        
        self.dt = 1 / fps # simulation timestep
        self.y = y0
        self.y0 = y0
        self.dy = dy0
        self.x = x0
        self.x0 = x0
        self.dx= dx0
        self.d2x=0
        self.spacing = spacing
        self.distance = 1000
        self.rotation1= 0
        self.rotation2 = 0
        self.update_carchase = update_carchase
        self.tire_d = tire_d
        self.tire_r = tire_d/2
        self.car_l = car_l
        self.desired_x = 0
        self.desired_dx = 0
        self.time = t0
        self.scale = 1
        self.is_running = True
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = ipc.MultiCanvas(7, width=canvas_width, height=self.canvas_height)
        self.meter_in_px0= meter_in_px0
        self.meter_in_px = meter_in_px0 # how many pixels one meter corresponds to, defines the scale  
        self.init_pos = np.array([self.canvas_width-260, self.canvas_height-98])
        
        super(Game, self).__init__()
        
    # main loop
    def run(self):
        frame_time = self.dt
        start_time = time()
        while(self.is_running):
            tick = time()
            self.desired_x, self.desired_dx, self.x, self.dx, self.d2x, self.y = self.update_carchase(self.x, self.dx, self.d2x, self.y, self.dy, self.spacing, self.dt)
            self.distance = self.y - self.x
            self.rotation1, self.rotation2 = self.tire_rotations(self.y0,self.x0)
            self.meter_in_px, self.scale = self.actual_mt_in_px(self.distance,self.meter_in_px0, self.canvas_width,self.car_l)
            self.draw_carchase(self.canvas,self.y, self.x, self.rotation1, self.rotation2,self.meter_in_px, self.scale, self.distance, self.canvas_width, self.canvas_height, self.car_l)
            self.time = tick - start_time 
            self.fps = 1 / frame_time
            if self.dt - (time() - tick) > 0:
                sleep(self.dt - (time() - tick))
            frame_time = time() - tick     
    # stop game 
    def tire_rotations(self, y0, x0):
        rotation1= (self.x-x0)/self.tire_r
        rotation2 = (self.y-y0)/self.tire_r
        return  rotation1, rotation2       
    def stop(self):
        self.is_running = False
    def actual_mt_in_px(self,distance, meter_in_px0, canvas_width, car_l):
        if (distance)>(1710/260):
            meter_in_px = canvas_width/(distance + 2*car_l )
            scale = meter_in_px/meter_in_px0
        else:
            meter_in_px = meter_in_px0
            scale = 1
        return meter_in_px, scale    
    # convert meters to pixels 
    def to_pixels(self, distance_in_meters):
        return distance_in_meters * self.meter_in_pixels

    # draw unicycle, pos = horizontal (motor position), y = [theta, phi]
    def draw_carchase(self,canvas, y, x, rotation1, rotation2,meter_in_px, scale, distance, canvas_width, canvas_height, car_l):
        sprite1 = Image.from_file('car1.png')
        sprite2 = Image.from_file('tire1.png')
        sprite3 = Image.from_file('tire1.png')
        sprite4 = Image.from_file('car2.png')
        sprite5 = Image.from_file('tire2.png')
        sprite6 = Image.from_file('tire2.png')   
        
        
        # kinematic relation of the wheel with the ground assuming there is no slipping

        #pos[0] = pos[0] + y[1] * 2 * r # for fixed camera
        # update canvas
        with ipc.hold_canvas(canvas):
            
            canvas.clear()
            canvas[0].fill_style = '#a9cafc'
            canvas[0].fill_rect(0, 0,canvas_width, canvas_height)
            canvas[1].translate((canvas_width-(distance+2*car_l)*meter_in_px)+130*scale,canvas_height-(44*scale))
            canvas[2].translate((canvas_width-(distance+2*car_l)*meter_in_px)+56*scale,canvas_height-(20*scale))
            canvas[3].translate((canvas_width-(distance+2*car_l)*meter_in_px)+218*scale,canvas_height-(20*scale))
            canvas[4].translate(canvas_width-130*scale,canvas_height-49*scale)
            canvas[5].translate(canvas_width-211*scale,canvas_height-20*scale)
            canvas[6].translate(canvas_width-55*scale,canvas_height-20*scale)
            canvas[1].draw_image(sprite1, -130, -44)
            canvas[2].draw_image(sprite2, -20, -20)
            canvas[3].draw_image(sprite3, -20, -20)
            canvas[4].draw_image(sprite4, -130,-49)
            canvas[5].draw_image(sprite5, -20, -20)
            canvas[6].draw_image(sprite6, -20, -20)
            canvas[2].rotate(rotation1)
            canvas[3].rotate(rotation1)
            canvas[5].rotate(rotation2)
            canvas[6].rotate(rotation2)
            canvas[1].scale(scale)
            canvas[2].scale(scale)
            canvas[3].scale(scale)
            canvas[4].scale(scale)
            canvas[5].scale(scale)
            canvas[6].scale(scale) 
            canvas[1].scale(1/scale)
            canvas[2].scale(1/scale)
            canvas[3].scale(1/scale)
            canvas[4].scale(1/scale)
            canvas[5].scale(1/scale)
            canvas[6].scale(1/scale)
            canvas[2].rotate(-rotation1)
            canvas[3].rotate(-rotation1)
            canvas[5].rotate(-rotation2)
            canvas[6].rotate(-rotation2)
            canvas[1].translate(-((canvas_width-(distance+2*car_l)*scale*self.meter_in_px0)+130*scale),-(canvas_height-(44*scale)))
            canvas[2].translate(-((canvas_width-(distance+2*car_l)*scale*self.meter_in_px0)+56*scale),-(canvas_height-(20*scale)))
            canvas[3].translate(-((canvas_width-(distance+2*car_l)*scale*self.meter_in_px0)+218*scale),-(canvas_height-(20*scale)))
            canvas[4].translate(-(canvas_width-130*scale),-(canvas_height-49*scale))
            canvas[5].translate(-(canvas_width-211*scale),-(canvas_height-20*scale))
            canvas[6].translate(-(canvas_width-55*scale),-(canvas_height-20*scale))

            
            

            