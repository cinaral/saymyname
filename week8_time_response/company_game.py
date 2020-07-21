import ipycanvas as ipc
#import ipyevents as ipe
from ipywidgets import Image

from time import time, sleep
from threading import Thread

import numpy as np

class Game(Thread):
    def __init__(self, x0, dx0, company_fun, invest_fun, t0=0, fps=60, last_n_days=40, canvas_width=600, canvas_height=300):        
        self.dt = 1 / fps # simulation timestep
        self.fps = fps
        self.x0 = x0
        self.dx0 = dx0
        self.company_fun = company_fun
        self.invest_fun = invest_fun
        
        self.t0 = t0
        self.is_running = True

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.init_pos = np.array([self.canvas_width / 2, self.canvas_height * 3 / 4])
        self.canvas = ipc.MultiCanvas(3, width=self.canvas_width, height=self.canvas_height)
        #self.event = ipe.Event(source=self.canvas, watched_events=['keydown'])
        #self.event.on_dom_event(self.handle_events) 
        
        self.t_hist = None
        self.xdxd2x_hist = None
        self.invest_hist = None

        # not sure if there is another way, Image.width etc are empty?!
        self.background = Image.from_file('sprites/background.png')
        self.background_dim = [0.5, 1024 - 2, 1024] # scale, width, height (-2 for for seamless connections)
        self.office = Image.from_file('sprites/office_building.png')
        self.office_dim = [0.2, 869, 960] # scale, width, height
        self.info_bg = Image.from_file('sprites/info_bg.png')
        self.info_bg_dim = [0.4, 499, 299] # scale, width, height
        self.info_bg_padding = 25      
        self.plot_bg = Image.from_file('sprites/plot_bg.png')
        self.plot_bg_dim = [0.4, 523, 499] # scale, width, height
        self.plot_bg_padding = 25  
        # some arbitrary padding parameters
        self.font = '14px sans-serif'
        self.text_spacing = 16
        self.fps_pos = (5, 20)
        self.text_bottom_padding = 10
        self.info_padding = (15, 25)
        
        self.plot_origin_offset = (34, 170)
        self.xlabel_offset = (141, 4)
        self.ylabel_offset = (-9, -146)
        self.xtick0_offset = (-5, 19)
        self.xtick1_offset = (131, 19)
        self.ytick0_offset = (-28, 4)
        self.ytick1_offset = (-28, -127)
        
        # plot options
        self.xmin_default = 0
        self.ymin_default = 0
        self.ymax_default = 1
        self.line_color_input = '#00a8ff'
        self.line_color_output = '#ff8800'
        self.line_width = 3
        self.line_sample_size = 100
        self.data_tip_offset = (0, -10)
        self.last_n_days = last_n_days
        # draw background
        self.draw_background(self.canvas[0])
        # init thread
        super(Game, self).__init__()

    # main loop
    def run(self):
        fps = 0
        x = self.x0 
        dx = self.dx0
        t = self.t0
        frame_time = self.dt
        start_time = time() - self.t0
        while(self.is_running):
            tick = time()
            
            investment = self.invest_fun(t, frame_time)
            x, dx, d2x, self.m, self.c, self.k, self.employee_array, self.perf_array = self.company_fun(x, dx, investment, frame_time)
            #print('x:{:.1f} dx: {:.1f} d2x: {:.1f}'.format(x, dx, d2x))
            if self.t_hist is None:
                self.t_hist = t
                self.xdxd2x_hist = np.array([x, dx, d2x])
                self.invest_hist = investment
                x_hist = x
            else:
                self.t_hist = np.append(self.t_hist, t)
                self.xdxd2x_hist = np.vstack((self.xdxd2x_hist, np.array([x, dx, d2x])))
                self.invest_hist = np.append(self.invest_hist, investment)
                x_hist = np.append(x_hist, x)
            
            self.draw_plots(self.canvas[2], t, self.t_hist, self.invest_hist, x_hist)
            self.draw_text(self.canvas[1], fps, t)

            if self.dt - (time() - tick) > 0:
                sleep(self.dt - (time() - tick))
            frame_time = time() - tick
            fps = 1 / frame_time
            t = t + frame_time
            
    # handle events
    def handle_events(self, event):
        # change invest_fun
        pass
        """
        if event['key'] == 'ArrowRight':
            self.th_desired = self.th_desired + 1 / 180 * np.pi
        if event['key'] == 'ArrowLeft':
            self.th_desired = self.th_desired - 1 / 180 * np.pi
        """
    # stop game           
    def stop(self):
        self.is_running = False

    # draw plots
    def draw_plots(self, canvas, t, t_hist, invest_hist, x_hist):
        # last n days
        if t > 0:
            last_n_idx = self.last_n_days * self.fps - 1
            t_hist = t_hist[-last_n_idx:-1]
            invest_hist = invest_hist[-last_n_idx:-1]
            x_hist = x_hist[-last_n_idx:-1]
        
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.font = self.font
            canvas.translate(self.canvas_width / 2, self.canvas_height)  
            canvas.translate(-(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_dim[0] * self.plot_bg_dim[1] + self.plot_bg_padding), -(self.plot_bg_dim[0] * self.plot_bg_dim[2] + self.plot_bg_padding))
            canvas.translate(self.plot_origin_offset[0], self.plot_origin_offset[1])
            #canvas.fill_text('Test', 0 , 0) 
            ####################
            #### input plot ####
            ####################
            xlim_min = max(np.amin(t_hist), self.xmin_default)
            xlim_max = t
            ylim_min = min(np.amin(invest_hist), self.ymin_default)
            ylim_max = max(np.amax(invest_hist), self.ymax_default)
            ylim_multiplier = 1
            while ylim_max >= 10 or ylim_min <= -10:
                ylim_max = ylim_max / 10
                ylim_min = ylim_min / 10
                ylim_multiplier = ylim_multiplier * 10
            xlim = [xlim_min, xlim_max]
            ylim = [ylim_min, ylim_max]     
            
            canvas.stroke_style = self.line_color_input
            canvas.line_width = self.line_width
            if t > 0:
                canvas.begin_path()
                for i in range(0, len(invest_hist)):
                    if i > 0:
                        canvas.line_to(self.xtick1_offset[0] * (t_hist[i] - xlim_min) / (xlim_max - xlim_min), self.ytick1_offset[1] * (invest_hist[i] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier))
                    else:
                        canvas.move_to(self.xtick1_offset[0] * (t_hist[i] - xlim_min) / (xlim_max - xlim_min), self.ytick1_offset[1] * (invest_hist[i] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier))
                canvas.stroke()   
                canvas.fill_style = self.line_color_input
                canvas.fill_text('{:.1f}'.format(invest_hist[-1] / ylim_multiplier), self.xtick1_offset[0] + self.data_tip_offset[0], self.ytick1_offset[1] * (invest_hist[-1] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier) + self.data_tip_offset[1])
                canvas.fill_style = 'black'
            
            canvas.fill_text('{:.0f}'.format(xlim[0]), self.xtick0_offset[0] , self.xtick0_offset[1]) 
            canvas.fill_text('{:.0f}'.format(xlim[1]), self.xtick1_offset[0] , self.xtick1_offset[1]) 
            canvas.fill_text('{:.1f}'.format(ylim[0]), self.ytick0_offset[0] , self.ytick0_offset[1]) 
            canvas.fill_text('{:.1f}'.format(ylim[1]), self.ytick1_offset[0] , self.ytick1_offset[1])
            canvas.fill_text('${:.0f}'.format(ylim_multiplier), self.ylabel_offset[0], self.ylabel_offset[1])
            canvas.fill_text('days', self.xlabel_offset[0], self.xlabel_offset[1])
                
            ####################
            ####################
            #canvas.fill_style = 'black'
            canvas.translate(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_dim[0] * self.plot_bg_dim[1] + self.plot_bg_padding, 0)
            canvas.translate(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_padding, 0)
            #canvas.fill_text('Test2', 0 , 0)
            
            #####################
            #### output plot ####
            #####################
            xlim_min = max(np.amin(t_hist), self.xmin_default)
            xlim_max = t
            ylim_min = min(np.amin(x_hist), self.ymin_default)
            ylim_max = max(np.amax(x_hist), self.ymax_default)
            ylim_multiplier = 1
            while ylim_max >= 10 or ylim_min <= -10:
                ylim_max = ylim_max / 10
                ylim_min = ylim_min / 10
                ylim_multiplier = ylim_multiplier * 10
            xlim = [xlim_min, xlim_max]
            ylim = [ylim_min, ylim_max]
                
            canvas.stroke_style = self.line_color_output
            canvas.line_width = self.line_width
            if t > 0:
                canvas.begin_path()
                for i in range(0, len(x_hist)):
                    if i > 0:
                        canvas.line_to(self.xtick1_offset[0] * (t_hist[i] - xlim_min) / (xlim_max - xlim_min), self.ytick1_offset[1] * (x_hist[i] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier))
                    else:
                        canvas.move_to(self.xtick1_offset[0] * (t_hist[i] - xlim_min) / (xlim_max - xlim_min), self.ytick1_offset[1] * (x_hist[i] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier))
                canvas.stroke()
                canvas.fill_style = self.line_color_output
                canvas.fill_text('{:.1f}'.format(x_hist[-1] / ylim_multiplier), self.xtick1_offset[0] + self.data_tip_offset[0], self.ytick1_offset[1] * (x_hist[-1] - ylim_min * ylim_multiplier) / ((ylim_max - ylim_min) * ylim_multiplier) + self.data_tip_offset[1])
                canvas.fill_style = 'black'
            
            canvas.fill_text('{:.0f}'.format(xlim[0]), self.xtick0_offset[0] , self.xtick0_offset[1])   
            canvas.fill_text('{:.0f}'.format(xlim[1]), self.xtick1_offset[0] , self.xtick1_offset[1]) 
            canvas.fill_text('{:.1f}'.format(ylim[0]), self.ytick0_offset[0] , self.ytick0_offset[1])
            canvas.fill_text('{:.1f}'.format(ylim[1]), self.ytick1_offset[0] , self.ytick1_offset[1]) 
            canvas.fill_text('${:.0f}'.format(ylim_multiplier), self.ylabel_offset[0], self.ylabel_offset[1])
            canvas.fill_text('days', self.xlabel_offset[0], self.xlabel_offset[1]) 
            
            #####################
            #####################
            
            canvas.translate(-self.plot_origin_offset[0], -self.plot_origin_offset[1])
            canvas.translate(-(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_padding), self.plot_bg_dim[0] * self.plot_bg_dim[2] + self.plot_bg_padding)
            canvas.translate(-self.canvas_width / 2, -self.canvas_height)  
    
    # draw text
    def draw_text(self, canvas, fps, t):
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.font = self.font
            # fps counter (top left)
            canvas.fill_text('FPS: {:.0f}'.format(fps), self.fps_pos[0], self.fps_pos[1])
            canvas.fill_text('Time: {:.1f} days'.format(t), self.fps_pos[0], self.fps_pos[1] + self.text_spacing)
            
            canvas.translate(self.canvas_width / 2, self.canvas_height)  
            canvas.translate(- self.info_bg_dim[0] * self.info_bg_dim[1] / 2,  -(self.office_dim[0] * self.office_dim[2] + self.info_bg_dim[0] * self.info_bg_dim[2] + self.info_bg_padding))
            #canvas.fill_text('Test3', 0 , 0)
            # company info
            canvas.fill_text('Number of Managers: {:.0f}'.format(self.employee_array[0]), self.info_padding[0], self.info_padding[1])
            canvas.fill_text('Number of Lawyers: {:.0f}'.format(self.employee_array[1]), self.info_padding[0], self.info_padding[1] + self.text_spacing)
            canvas.fill_text('Number of Workers: {:.0f}'.format(self.employee_array[2]), self.info_padding[0], self.info_padding[1] + 2 * self.text_spacing)
            canvas.fill_text(' ' * 19 + '1', self.info_padding[0], self.info_padding[1] + 3.5 * self.text_spacing)
            canvas.fill_text('{:6.3g}s\u00B2 + {:6.3g}s + {:6.3g}'.format(self.m, self.c, self.k), self.info_padding[0], self.info_padding[1] + 5 * self.text_spacing)
            canvas.translate(self.info_bg_dim[0] * self.info_bg_dim[1] / 2,  (self.office_dim[0] * self.office_dim[2] + self.info_bg_dim[0] * self.info_bg_dim[2] + self.info_bg_padding))
            canvas.translate(-self.canvas_width / 2, -self.canvas_height)  
    
    def draw_background(self, canvas):
        with ipc.hold_canvas(canvas):
            canvas.clear()
            canvas.font = self.font
            # bg
            canvas.scale(self.background_dim[0])
            for i in range(0, int(canvas.width / (self.background_dim[0] * self.background_dim[1]))+1):
                canvas.draw_image(self.background, i * self.background_dim[1], 0)
            canvas.scale(1 / self.background_dim[0])
            # office (middle)
            canvas.translate(self.canvas_width / 2, self.canvas_height)  
            canvas.scale(self.office_dim[0])
            canvas.draw_image(self.office, -self.office_dim[1] / 2, -self.office_dim[2])
            canvas.scale(1 / self.office_dim[0])
            # info bg (above office)
            canvas.translate(- self.info_bg_dim[0] * self.info_bg_dim[1] / 2,  -(self.office_dim[0] * self.office_dim[2] + self.info_bg_dim[0] * self.info_bg_dim[2] + self.info_bg_padding))
            canvas.scale(self.info_bg_dim[0])
            canvas.draw_image(self.info_bg, 0, 0)
            canvas.scale(1 / self.info_bg_dim[0])
            canvas.fill_text('Company Information (System)', 0 , -self.text_bottom_padding)
            canvas.translate(self.info_bg_dim[0] * self.info_bg_dim[1] / 2,  (self.office_dim[0] * self.office_dim[2] + self.info_bg_dim[0] * self.info_bg_dim[2] + self.info_bg_padding))
            # plot bg (left of office)
            canvas.translate(-(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_dim[0] * self.plot_bg_dim[1] + self.plot_bg_padding), -(self.plot_bg_dim[0] * self.plot_bg_dim[2] + self.plot_bg_padding))
            canvas.scale(self.plot_bg_dim[0])
            canvas.draw_image(self.plot_bg, 0, 0)
            canvas.scale(1 / self.plot_bg_dim[0])
            canvas.fill_text('Investment (Input)', 0 , -self.text_bottom_padding)
            canvas.translate(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_dim[0] * self.plot_bg_dim[1] + self.plot_bg_padding, 0)
            # plot bg (right of office)
            canvas.translate(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_padding, 0)
            canvas.scale(self.plot_bg_dim[0])
            canvas.draw_image(self.plot_bg, 0, 0)
            canvas.scale(1 / self.plot_bg_dim[0])
            canvas.fill_text('Total Profit (Output)', 0 , -self.text_bottom_padding)
            # restore
            canvas.translate(-(self.office_dim[0] * self.office_dim[1] / 2 + self.plot_bg_padding), 0)
            canvas.translate(-self.canvas_width / 2, -self.canvas_height)  