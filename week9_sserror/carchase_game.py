from ipywidgets import Image
import ipycanvas as ipc
from time import time, sleep
from threading import Thread

import numpy as np

class Game(Thread):
    def __init__(self, x0 , dx0 , y0, dy0, update_carchase, spacing, tire_d , car_l, t0=0, fps=60,canvas_width=910, canvas_height=300, meter_in_px0=260/4.5):        
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
        self.canvas = ipc.MultiCanvas(8, width=canvas_width, height=self.canvas_height)
        self.meter_in_px0= meter_in_px0
        self.meter_in_px = meter_in_px0  
        self.init_pos = np.array([self.canvas_width-130, self.canvas_height-self.meter_in_px])       
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
            self.meter_in_px, self.scale = self.actual_mt_in_px(self.distance,self.meter_in_px,self.meter_in_px0, self.canvas_width,self.car_l)
            self.draw_background(self.canvas[0],self.rotation2,self.tire_r)
            self.draw_carchase(self.canvas,self.y, self.x, self.rotation1, self.rotation2,self.meter_in_px, self.scale, self.distance, self.canvas_width, self.canvas_height, self.car_l)
            self.time = tick - start_time 
            self.fps = 1 / frame_time
            self.draw_text(self.canvas[7], self.fps, self.time, self.distance, self.dx, self.d2x, self.dy)
            if self.dt - (time() - tick) > 0:
                sleep(self.dt - (time() - tick))
            frame_time = time() - tick     
    # stop game 
    def tire_rotations(self, y0, x0):
        rotation1= ((self.x-x0)/self.tire_r)%(2*np.pi)
        rotation2 = ((self.y-y0)/self.tire_r)%(2*np.pi)
        return  rotation1, rotation2       
    def stop(self):
        self.is_running = False
    def actual_mt_in_px(self,distance,meter_in_px, meter_in_px0, canvas_width, car_l):
        if (distance)>(1710/260):
            meter_in_px = canvas_width/(distance + 2*car_l )
            scale = meter_in_px/meter_in_px0
        else:
            meter_in_px = meter_in_px0
            scale = 1
        return meter_in_px, scale
    # draw unicycle, pos = horizontal (motor position), y = [theta, phi]
    def draw_background(self, canvas, rotation2,tire_r):
        # kinematic relation of the wheel with the ground assuming there is no slipping
        pos = 1 * self.init_pos
        pos[0] = pos[0] - rotation2 * tire_r # for following camera
        #pos = 1 * init_pos
        #pos[0] = pos[0] + y[1] * 2 * r 
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.translate(pos[0], 0)
            canvas.fill_style = 'lightgray' 
            # reference lines for every meter
            discrete_shift = int(rotation2 * tire_r / self.meter_in_px) * 2 * self.meter_in_px
            for i in np.arange(discrete_shift - self.canvas_width, discrete_shift + self.canvas_width, 2 * self.meter_in_px): 
                canvas.fill_rect(i, 0, self.meter_in_px, self.canvas_height)
            canvas.translate(-pos[0], 0)
            canvas.stroke_rect(0, 0, self.canvas_width, self.canvas_height)

            canvas.fill_style = 'gray' 
            canvas.fill_rect(0, pos[1] + tire_r, self.canvas_width, self.canvas_height - (pos[1] + tire_r))
    def draw_carchase(self,canvas, y, x, rotation1, rotation2,meter_in_px, scale, distance, canvas_width, canvas_height, car_l):
        sprite1 = Image.from_file('car1.png')
        sprite2 = Image.from_file('tire1.png')
        sprite3 = Image.from_file('car2.png')
        sprite4 = Image.from_file('tire2.png')  
        with ipc.hold_canvas(canvas):   
            canvas.clear()
            canvas[1].translate((canvas_width-(distance+2*car_l)*meter_in_px)+130*scale,canvas_height-(44*scale))
            canvas[2].translate((canvas_width-(distance+2*car_l)*meter_in_px)+56*scale,canvas_height-(20*scale))
            canvas[3].translate((canvas_width-(distance+2*car_l)*meter_in_px)+218*scale,canvas_height-(20*scale))
            canvas[4].translate(canvas_width-130*scale,canvas_height-49*scale)
            canvas[5].translate(canvas_width-211*scale,canvas_height-20*scale)
            canvas[6].translate(canvas_width-55*scale,canvas_height-20*scale)
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
            canvas[1].draw_image(sprite1, -130, -44)
            canvas[2].draw_image(sprite2, -20, -20)
            canvas[3].draw_image(sprite2, -20, -20)
            canvas[4].draw_image(sprite3, -130,-49)
            canvas[5].draw_image(sprite4, -20, -20)
            canvas[6].draw_image(sprite4, -20, -20)
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
            canvas[1].translate(-((canvas_width-(distance+2*car_l)*meter_in_px)+130*scale),-(canvas_height-(44*scale)))
            canvas[2].translate(-((canvas_width-(distance+2*car_l)*meter_in_px)+56*scale),-(canvas_height-(20*scale)))
            canvas[3].translate(-((canvas_width-(distance+2*car_l)*meter_in_px)+218*scale),-(canvas_height-(20*scale)))
            canvas[4].translate(-(canvas_width-130*scale),-(canvas_height-49*scale))
            canvas[5].translate(-(canvas_width-211*scale),-(canvas_height-20*scale))
            canvas[6].translate(-(canvas_width-55*scale),-(canvas_height-20*scale))
    def draw_text(self, canvas, fps, time, distance,dx,d2x, dy):
        with ipc.hold_canvas(canvas):
            
            pos = (800, 20)
            spacing = 14
            canvas.font = '12px serif'
            canvas.fill_text('vel_escaper: {:.1f} m/s'.format(dy), pos[0], pos[1])
            pos = (400, 20)
            canvas.font = '14px serif'
            canvas.fill_text('FPS: {:.0f}'.format(fps), pos[0], pos[1])
            canvas.fill_text('Time: {:.1f} s'.format(time), pos[0], pos[1] + spacing)
            canvas.fill_text('Distance : {:.1f}'.format(distance), pos[0], pos[1]+2*spacing)               
            pos = (50, 20)
            spacing = 14
            canvas.font = '12px serif'
            canvas.fill_text('vel_chaser: {:.1f} m/s'.format(dx), pos[0], pos[1])

            