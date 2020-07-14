import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns
import numpy as np

class plot():

    def __init__(self, data, param, build):
        self.data = data
        self.param = param
        self.build = build
        self.line = []

        self.fsize = 20                     # Fontsize
        self.psize = 25                     # Padding size
        self.tpsize = 30                    # Titlepaddingsize
        
        self.detector_xrange = (-120, 120)
        self.detector_yrange =(68, 100)

    def scatter(self, x, y, time):
        fig = plt.figure(figsize = (self.fsize,10))
        sns.set_style("darkgrid")
        ax = plt.axes(xlim=self.detector_xrange, ylim = (69.9, 71))
        ax.set_xlabel('z [mm]', fontsize = self.fsize,  labelpad =self.psize)
        ax.set_ylabel('r [mm]', fontsize = self.fsize, labelpad =self.psize)
        ax.tick_params(axis='both', which='major', labelsize=self.fsize)
        ax.tick_params(axis='both', which='minor', labelsize=self.fsize)
        ax.set_title('FACT Detector', fontsize =self.psize, pad = self.tpsize)
        plt.scatter(x,y,c = time, cmap='Reds', s = 40)
        plt.colorbar()
        plt.show()
        pass

    def initAnimation(self):
        r = self.param.CoordinateMatrix[:,1]*self.build.ActivationMatrix[:,0]
        z = self.param.CoordinateMatrix[:,2]*self.build.ActivationMatrix[:,0]
        self.line.set_data(z,r)
        return self.line

    def Animate(self, i):
        r = self.param.CoordinateMatrix[:,1]*self.build.ActivationMatrix[:,i]
        z = self.param.CoordinateMatrix[:,2]*self.build.ActivationMatrix[:,i]
        self.line.set_data(z,r)
        return self.line

    def plot_FACT_live(self):            
        fig = plt.figure(figsize = (self.fsize,10))
        sns.set_style("darkgrid")
        ax = plt.axes(xlim=self.detector_xrange, ylim = self.detector_yrange)
        ax.set_xlabel('z [mm]', fontsize = self.fsize,  labelpad =self.psize)
        ax.set_ylabel('r [mm]', fontsize = self.fsize, labelpad =self.psize)
        ax.tick_params(axis='both', which='major', labelsize=self.fsize)
        ax.tick_params(axis='both', which='minor', labelsize=self.fsize)
        ax.set_title('FACT Detector', fontsize =self.psize, pad = self.tpsize)
        self.line, = ax.plot([], [], '-ro', lw = 2)
        r = self.param.CoordinateMatrix[:,1]*self.build.ActivationMatrix[:,0]
        z = self.param.CoordinateMatrix[:,2]*self.build.ActivationMatrix[:,0]
        self.line.set_data(z,r)
        anim = animation.FuncAnimation(fig, self.Animate, init_func=self.initAnimation,frames=self.param.frames, interval=self.fsize)
        """ Moviemaker: (NB VERY Slow)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        anim.save('im.mp4', writer=writer)
        """
        plt.show()

    def hist(self, df_z):
        plt.hist(df_z.z_pos, weights=df_z.z_weight, bins = np.arange(-120,120,2))
        plt.title('')
        ax = plt.axes()
        ax.set_xlabel('z [mm]', fontsize = self.fsize,  labelpad =self.psize)
        ax.set_ylabel('Count', fontsize = self.fsize, labelpad =self.psize)
        ax.tick_params(axis='both', which='major', labelsize=self.fsize)
        ax.tick_params(axis='both', which='minor', labelsize=self.fsize)
        ax.set_title('FACT Detector Vertex count', fontsize =self.psize, pad = self.tpsize)
        plt.show()