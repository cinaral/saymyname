import ipycanvas as ipc
import ipyevents as ipe

from time import time, sleep
from threading import Thread

import numpy as np

class Game(Thread):
    def __init__(self, y0, dy0, update_unicycle, d, l, th0_desired=0, dth0_desired=0, t0=0, fps=30, canvas_width=600, canvas_height=300, meter_in_pixels=100):        
        self.dt = 1 / fps # simulation timestep
        self.y = y0
        self.dy = dy0
        self.update_unicycle = update_unicycle
        self.d = d
        self.l = l
        
        self.th_desired = th0_desired
        self.dth_desired = dth0_desired
        
        self.time = t0
        self.is_running = True

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.meter_in_pixels = meter_in_pixels # how many pixels one meter corresponds to, defines the scale  
        self.init_pos = np.array([self.canvas_width / 2, self.canvas_height * 3 / 4])
        self.canvas = ipc.MultiCanvas(3, width=self.canvas_width, height=self.canvas_height)
        self.event = ipe.Event(source=self.canvas, watched_events=['keydown'])
        self.event.on_dom_event(self.handle_events) 
        
        self.t_history = None
        self.ydyd2y_history = None
        self.th_desired_history = None

        super(Game, self).__init__()
        
    # main loop
    def run(self):
        frame_time = self.dt
        start_time = time()
        while(self.is_running):
            tick = time()

            self.y, self.dy, self.d2y = self.update_unicycle(self.y, self.dy, self.th_desired, self.dth_desired, self.dt)
            r = self.d / 2
            self.draw_background(self.canvas[0],self.y, r)
            self.draw_unicycle(self.canvas[1], self.y, r, self.l)
        
            self.time = tick - start_time 
            self.fps = 1 / frame_time
            self.draw_text(self.canvas[2], self.fps, self.time, self.y, self.dy, self.d2y, r, self.th_desired)
            
            if self.t_history is None:
                self.t_history = self.time
                self.ydyd2y_history = np.concatenate((self.y, self.dy, self.d2y))
                self.th_desired_history = self.th_desired
            else:
                self.t_history = np.append(self.t_history, self.time)
                self.ydyd2y_history = np.vstack((self.ydyd2y_history, np.concatenate((self.y, self.dy, self.d2y))))
                self.th_desired_history = np.append(self.th_desired_history, self.th_desired)
        
            if self.dt - (time() - tick) > 0:
                sleep(self.dt - (time() - tick))
            frame_time = time() - tick
            
    # handle events
    def handle_events(self, event):
        if event['key'] == 'ArrowRight':
            self.th_desired = self.th_desired + 1 / 180 * np.pi
        if event['key'] == 'ArrowLeft':
            self.th_desired = self.th_desired - 1 / 180 * np.pi
      
    # stop game           
    def stop(self):
        self.is_running = False

    # convert meters to pixels 
    def to_pixels(self, distance_in_meters):
        return distance_in_meters * self.meter_in_pixels

    # draw background
    def draw_background(self, canvas, y, r):
        r = self.to_pixels(r)
        # kinematic relation of the wheel with the ground assuming there is no slipping
        pos = 1 * self.init_pos
        pos[0] = pos[0] - y[1] * 2 * r # for following camera
        #pos = 1 * init_pos
        #pos[0] = pos[0] + y[1] * 2 * r 
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.translate(pos[0], 0)
            canvas.fill_style = 'lightgray' 
            # reference lines for every meter
            discrete_shift = int(y[1] * r / self.meter_in_pixels) * 2 * self.meter_in_pixels
            for x in np.arange(discrete_shift - self.canvas_width, discrete_shift + self.canvas_width, 2 * self.meter_in_pixels): 
                canvas.fill_rect(x, 0, self.meter_in_pixels, self.canvas_height)
            canvas.translate(-pos[0], 0)
            canvas.stroke_rect(0, 0, self.canvas_width, self.canvas_height)

            canvas.fill_style = 'gray' 
            canvas.fill_rect(0, pos[1] + r, self.canvas_width, self.canvas_height - (pos[1] + r))

    # draw unicycle, pos = horizontal (motor position), y = [theta, phi]
    def draw_unicycle(self, canvas, y, r, l, wheel_thickness=4, motor_size=7):
        r = self.to_pixels(r)
        l = self.to_pixels(l)
        # kinematic relation of the wheel with the ground assuming there is no slipping
        pos = 1 * self.init_pos
        #pos[0] = pos[0] + y[1] * 2 * r # for fixed camera
        # update canvas
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.translate(pos[0], pos[1])
            # 1. wheel:   
            # 1.1. rim
            canvas.line_width = wheel_thickness
            canvas.stroke_arc(0, 0, r, 0, np.pi * 2) 
            # 1.2. mark
            canvas.fill_style = 'black'
            canvas.rotate(y[1])
            canvas.fill_arc(0, r * 3 / 4, wheel_thickness / 2, 0, np.pi * 2)
            # 1.3. spokes
            canvas.line_width = wheel_thickness / 3
            canvas.begin_path()
            canvas.move_to(0, -r)
            canvas.line_to(0, r)
            canvas.move_to(-r, 0)
            canvas.line_to(r, 0)
            canvas.rotate(np.pi / 4)
            canvas.move_to(0, -r)
            canvas.line_to(0, r)
            canvas.move_to(-r, 0)
            canvas.line_to(r, 0)
            canvas.stroke()
            canvas.rotate(-np.pi / 4)
            canvas.rotate(-y[1]) # undo rotation  
            # 2. body:
            # 2.1. frame
            canvas.rotate(y[0])
            canvas.fill_style = 'blue'
            canvas.fill_rect(-1.5, 0, motor_size * 3 / 5, -l)
            # 2.2. motor
            canvas.fill_style = 'darkred'
            canvas.fill_arc(0, 0, motor_size, 0, np.pi * 2)
            # 2.3. load
            canvas.fill_style = 'blue'
            canvas.translate(0, -l)
            canvas.fill_rect(-motor_size, -motor_size, 2 * motor_size)
            canvas.translate(0, l) # undo translation
            canvas.rotate(-y[0]) # undo rotation
            canvas.translate(-pos[0], -pos[1]) # undo translation

    # draw text
    def draw_text(self, canvas, fps, time, y, dy, d2y, r, th_desired):
        # convert radians to degrees
        def to_degrees(radians):
            return radians / np.pi * 180

        # convert degrees into -180 +180 degrees
        def to_180degrees(degrees):
            while degrees > 180:
                degrees = degrees - 360
            while degrees < -180:
                degrees = degrees + 360
            return degrees
        
        with ipc.hold_canvas(canvas):
            pos = (5, 20)
            spacing = 14
            canvas.clear()
            canvas.font = '12px serif'
            canvas.fill_text('FPS: {:.0f}'.format(fps), pos[0], pos[1])
            canvas.fill_text('Time: {:.1f} s'.format(time), pos[0], pos[1] + spacing)
            canvas.fill_text('\u03B8: {:.1f}\u00B0'.format(to_180degrees(to_degrees(y[0]))), pos[0], pos[1] + 2 * spacing)
            #canvas.fill_text('\u03C6: {:.1f}\u00B0'.format(to_180degrees(to_degrees(y[1]))), pos[0], pos[1] + 3 * spacing)
            canvas.fill_text('pos: {:.1f} m'.format(y[1] * 2 * r), pos[0], pos[1] + 3 * spacing)
            canvas.fill_text('vel: {:.1f} m/s'.format(dy[1] * 2 * r), pos[0], pos[1] + 4 * spacing)
            canvas.fill_text('acc: {:.1f} m/s\u00B2'.format(d2y[1] * 2 * r), pos[0], pos[1] + 5 * spacing)
            pos = (265, 20)
            centering_shift = 75
            canvas.font = '14px serif'
            canvas.fill_text('Target \u03B8: {:.1f}\u00B0'.format(to_180degrees(to_degrees(th_desired))), pos[0], pos[1])
            canvas.fill_text('(Use left and right arrow keys to change.)', pos[0] - centering_shift, pos[1] + spacing)    