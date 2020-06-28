import numpy as np
import matplotlib.pyplot as plt

class Setup():

    def __init__(self, data):
        self.data = data
        self.time = np.arange(self.data['t'].iloc[0],self.data['t'].iloc[-1], 5)
        self.count = np.empty(len(self.time))
        self.frame = 500
    
    def construct(self):
        self.ActiveFibers()
        tmin, tmax = self.FindRisingEdge()
        self.SetTime(tmin, tmax)
        M2D = self.Set_2D_Data()
        data = self.FindCoordinates()
        return data


    def ActiveFibers(self):
        for i in range(len(self.data['N'])):
            t = self.data['t'].iloc[i]
            self.count[t//5: (t+ self.data['tot'].iloc[i])//5] += 1

    def FindRisingEdge(self):
        ix = np.argmax(self.count >= 700)-100
        ixm = ix+self.frame
        tmin = self.time[ix]
        tmax = self.time[ixm]

        self.time = self.time[ix: ixm]
        self.count = self.count[ix: ixm]
        
        return tmin, tmax

        
    def SetTime(self, t0, tmax):
        self.data = self.data[(self.data['t'] >= t0) & (self.data['t'] <= tmax)].reset_index(drop = True)


    def Set_2D_Data(self):
        dat = np.empty((800,len(self.time)))
        for i in range(len(self.data['N'])):
            itt = int(self.data['tot'][i]/5)
            dat[self.data['N'][i], int((self.data['t'][i]-self.time[0])/5): int((self.data['t'][i]-self.time[0])/5)+ itt] += 1
        return dat



    def FindCoordinates(self):
        """ All hardcoded values r and z values are in mm
        """
        dist_center = 118.8
        self.data['r'], self.data['z'] = np.NaN, np.NaN

        
        self.data.loc[self.data['N']  <= 197, ('z','r')] =  98.86
        self.data.loc[self.data['N']  <= 197, 'z'] = self.data['N']*1.2 + 0.6 - dist_center
        
        self.data.loc[(self.data['N']  >= 200) & (self.data['N'] <= 398), 'r'] = 98.0
        self.data.loc[(self.data['N']  >= 200) & (self.data['N'] <= 398), 'z'] = (self.data['N']-200)*1.2 - dist_center
        
        self.data.loc[(self.data['N']  >= 400) & (self.data['N'] <= 597), 'r'] = 70.86
        self.data.loc[(self.data['N']  >= 400) & (self.data['N'] <= 597), 'z'] = (self.data['N']-400)*1.2 + 0.6 - dist_center
        
        self.data.loc[self.data['N']  >= 600, 'r'] = 70.0
        self.data.loc[self.data['N']  >= 600, 'z'] = (self.data['N']-600)*1.2 - dist_center

   

        return self.data