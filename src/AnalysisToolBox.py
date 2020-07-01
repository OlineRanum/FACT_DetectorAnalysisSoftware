import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from Setup import Setup


class AnalysisToolBox():

    def __init__(self, data, ActivationMatrix, CoordinateMatrix):
        self.data = data
        self.ActivationMatrix = ActivationMatrix
        self.CoordinateMatrix = CoordinateMatrix

        self.geometry = pd.read_csv('settings/settings.csv', header = 0)
        self.t_res = self.geometry['Time_resolution_ns'][0]
        self.maxTravelT = self.geometry['max_travel_time'][0]

        self.count = np.nansum(self.ActivationMatrix, axis = 0)
        self.TailIndex = 0
        self.TailTime = int(self.geometry['tail_time'][0]//5*5)
        
    def Initiate_Standard_Analysis(self):
        self.DefineTaleData()

    
    def DefineTaleData(self):
        self.data = self.data[self.data['t'] > self.TailTime].reset_index(drop = True)
        self.Track()

    def Track(self):
        N1 = self.data[self.data['N'] < 200]
        N2 = self.data[(self.data['N'] < 400) & (self.data['N'] >= 200)]
        N3 = self.data[(self.data['N'] < 600) & (self.data['N'] >= 400)]
        N4 = self.data[self.data['N'] >=  600]
        t = self.data['t'].values

        self.compare(N3, N4)

        #for i in range(len(t)):
         #   temp = self.data[(self.data['t'] <=  self.data['t'][i] + self.maxTravelT) & (self.data['t'] >= self.data['t'][i]-self.maxTravelT)]
            
                

        
    def compare(self, df1, df2):
        z_pos, z_weight = [], []
        for i in range(len(df1)):
            bar = np.where((df2['t'].values >= df1['t'].iloc[i] - self.maxTravelT) & (df2['t'].values <= df1['t'].iloc[i] + self.maxTravelT))[0]
            zp, zw = self.Z_distribution(df1, df2, i, bar)
            if zp:
                z_pos.append(zp)
                z_weight.append(zw)
        print(z_pos)


    def Z_distribution(self, df1, df2, i, bar):
        z_temp = np.zeros(200)
        z_vals = []
        z_weight = []
        for j in bar:
            r1 = self.CoordinateMatrix[int(df1['N'].iloc[i]),1]
            r2 = self.CoordinateMatrix[int(df2['N'].iloc[j]),1]
            z1 = self.CoordinateMatrix[int(df1['N'].iloc[i]),2]
            z2 = self.CoordinateMatrix[int(df2['N'].iloc[j]),2]
            z_pos1 = self.FindOriginZ_extrapolate(r1, r2, z1, z2)
            z_pos2 = self.FindOriginZ(r1, r2, z1, z2)
            z_pos = z_pos1
            if (z_pos < 500000 and z_pos >-5000000):
                z_vals.append(z_pos)
                z_weight.append(1/bar.size)
        return z_vals, z_weight


    def FindOriginZ(self,r1,r2,z1,z2):
        dr = r2-r1
        dz = z2-z1
        tan_theta = dz/dr
        dD = tan_theta*r2 
        z_pos = z2 - dD
        return z_pos

    def FindOriginZ_extrapolate(self,r1,r2,z1,z2):
        """ Using that f(x) = a*x + b
        """
        a = (r2-r1)/(z2-z1)
        b = r1 - a*z1
        z_pos = -b/a
        return z_pos

    def Crawler(self):
        return 0 

    def ClusterLocator(self):
        return 0




    def FindTail(self):
        EdgeIndex = np.argmax(self.count >= self.geometry['edge'][0])
        self.TailIndex = np.argmax(self.count[EdgeIndex:] <= self.geometry['tail'][0]) + EdgeIndex
        return None
