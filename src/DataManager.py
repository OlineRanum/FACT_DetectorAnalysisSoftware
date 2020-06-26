import pandas as pd
import numpy as np

class DataManager():
    def __init__(self, data):
        self.data = data

    def SetTime(self, t0, tmax):
        self.data = self.data[(self.data['t'] >= t0) & (self.data['t'] <= tmax)].reset_index(drop = True)


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