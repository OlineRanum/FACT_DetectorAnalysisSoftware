import matplotlib.pyplot as plt 
import matplotlib.animation as animation

class plot():

    def __init__(self, data, M2D, M):
        self.data = data
        self.M2D = M2D
        self.M = M
        self.line = []


    def plot_FACT(self):      
        plt.scatter(self.data['z'], self.data['r'])
        plt.plot
        plt.show()
        


    def init(self):
        r = self.M[:,1]*self.M2D[:,0]
        z = self.M[:,2]*self.M2D[:,0]
        self.line.set_data(z,r)
        return self.line

    def Animate(self, i):
        r = self.M[:,1]*self.M2D[:,i]
        z = self.M[:,2]*self.M2D[:,i]
        self.line.set_data(z,r)
        return self.line

    def plot_FACT_live(self):            
        fig = plt.figure(figsize = (20,10))
        ax = plt.axes(xlim=(-120, 120), ylim=(68, 100))
        ax.set_xlabel('z [mm]', fontsize = 20,  labelpad = 25)
        ax.set_ylabel('r [mm]', fontsize = 20, labelpad = 25)
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.tick_params(axis='both', which='minor', labelsize=20)
        ax.set_title('FACT Detector', fontsize = 25, pad = 30)
        self.line, = ax.plot([], [], '-ro', lw = 2)
        r = self.M[:,1]*self.M2D[:,0]
        z = self.M[:,2]*self.M2D[:,0]
        self.line.set_data(z,r)
        anim = animation.FuncAnimation(fig, self.Animate, init_func=self.init,
                               frames=500, interval=20)
        plt.show()