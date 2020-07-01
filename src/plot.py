import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns

class plot():

    def __init__(self, data, param, ActivationMatrix, CoordinateMatrix):
        self.data = data
        self.param = param
        self.ActivationMatrix = ActivationMatrix
        self.CoordinateMatrix = CoordinateMatrix
        self.line = []

        self.fsize = 20                     # Fontsize
        self.psize = 25                     # Padding size
        self.tpsize = 30                    # Titlepaddingsize
        
        self.detector_xrange = (-120, 120)
        self.detector_yrange =(68, 100)


    def initAnimation(self):
        r = self.CoordinateMatrix[:,1]*self.ActivationMatrix[:,0]
        z = self.CoordinateMatrix[:,2]*self.ActivationMatrix[:,0]
        self.line.set_data(z,r)
        return self.line

    def Animate(self, i):
        r = self.CoordinateMatrix[:,1]*self.ActivationMatrix[:,i]
        z = self.CoordinateMatrix[:,2]*self.ActivationMatrix[:,i]
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
        r = self.CoordinateMatrix[:,1]*self.ActivationMatrix[:,0]
        z = self.CoordinateMatrix[:,2]*self.ActivationMatrix[:,0]
        self.line.set_data(z,r)
        anim = animation.FuncAnimation(fig, self.Animate, init_func=self.initAnimation,frames=self.param.frames, interval=self.fsize)
        plt.show()