import numpy as np
import matplotlib.pyplot as plt

class DataAnalyzer():

    def __init__(self, data):
        self.data = data
        self.time, self.count = [],[]

    def Count_ActiveFibers(self):
        self.time = np.arange(self.data['t'].iloc[0],self.data['t'].iloc[-1], 5)
        self.count = np.empty(len(self.time))
        for i in range(len(self.data['N'])):
            idx = self.data['t'].iloc[i]//5
            itt = self.data['tot'].iloc[i]//5
            self.count[idx:idx+itt] += 1
            

    def FindRisingEdge(self):
        idx0 = np.argmax(self.count >= 700)
        t0   = self.time[idx0]
        tmax = self.time[idx0+500]
        self.time = self.time[idx0: idx0+500]
        self.count = self.count[idx0: idx0 + 500]
        plt.plot(self.time, self.count)
        plt.show()
        return t0, tmax, self.time, self.count
