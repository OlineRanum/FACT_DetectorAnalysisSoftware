import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from plot import plot
from tabulate import tabulate
from collections import Counter


class AnalysisToolBox():

    def __init__(self, data, param, build):
        self.data = data
        self.param = param
        self.build = build
        self.k = []
        self.count = []
        self.TailIndex = 0

        self.Layer_1 = pd.DataFrame()
        self.Layer_2 = pd.DataFrame()
        
    def Initiate_Standard_Analysis(self): 
        self.DefineTailData(self.param.tail_time,self.param.CoordinateMatrix, self.param.L3_min)
        cluster_L1 = self.FindClusters(self.Layer_1,self.param.t_res, self.param.Track_radius)
        cluster_L2 = self.FindClusters(self.Layer_2, self.param.t_res, self.param.Track_radius)
        df_z = self.TrackPath(cluster_L1, cluster_L2)
        return df_z

    def find_bin(self, value, bins):
        """ bins is a list of tuples, like [(0,20), (20, 40), (40, 60)],
            binning returns the smallest index i of bins so that
            bin[i][0] <= value < bin[i][1]
        """

        for i in range(0, len(bins)):
            if bins[i][0] <= value < bins[i][1]:
                return i
        return -1


    def DefineTailData(self, tail_cut, CoordinateMatrix_, layer_cut):
        self.data_ = self.data[self.data['t'] > tail_cut]
        self.data = self.data_.reset_index(drop = True)

        L1 = self.data[self.data['N'] >= layer_cut]                                                     # Inner Layer
        L2 = self.data[self.data['N'] < layer_cut]                                                      # Outer Layer
        CoordinateFrame = pd.DataFrame(CoordinateMatrix_, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.Layer_1 = pd.merge(L1, CoordinateFrame, on =['N'])
        self.Layer_2 = pd.merge(L2, CoordinateFrame, on =['N'])
        self.Layer_1['key'] = np.arange(0, len(self.Layer_1), 1)
        self.Layer_2['key'] = np.arange(0, len(self.Layer_2), 1)
        #print(self.Layer_1.to_markdown())
        #print(self.Layer_2.to_markdown())

        #P = plot(self.data, self.param, self.build)
        #P.scatter(self.Layer_2['z'], self.Layer_2['r'], self.Layer_2['t'])


        return self.data_


    def FindClusters(self, df, t_resolution, radius):
        keys = np.array([])
        t, z, r = [],[],[]
        for i in range(len(df['t'])):
            df_temp = df[(abs(df['t']-df['t'].iloc[i]) <= t_resolution) & (abs(df['z']-df['z'].iloc[i]) <= radius)]
            df_temp = df_temp[~df_temp.key.isin(keys)]
            temp_length = len(df_temp['t'])
            if temp_length > 0:
                t.append(np.sum(df_temp['t'])/temp_length)
                z.append(np.sum(df_temp['z'])/temp_length)
                r.append(np.sum(df_temp['r'])/temp_length)
                keys = np.append(keys,df_temp['key'].values)
        
        d = {'t': t, 'z': z, 'r': r}
        dfv = pd.DataFrame(data=d)
        dfv = dfv.sort_values(['t','z']).reset_index(drop = True)

        # Recombine cluster gaps
        """ It can happen that a vertex is not combined due to the isolation process above, 
        this loop runs a doubble check to make sure that all clusters are in fact isolated clusters, and recobinates in the case 
        of two neighboring events.
        """
        i = 0
        while i < len(dfv)-1:
            if (abs(dfv['t'].loc[i] - dfv['t'].loc[i+1]) <= t_resolution) and (abs(dfv['z'].loc[i] - dfv['z'].loc[i+1]) <= radius):
                dfv.loc[i] = dfv[i:i+2].mean()
                dfv = dfv.drop([i+1]).reset_index(drop = True)
            i += 1

        return dfv


    def TrackPath(self, df1, df2):
        """ 
        Assumptions:
        df1 = L1 = The layer with the smallest radius
        
        - we only concider the paths going from layer 1 to layer 2

        """

        z_pos, z_weight = [], []
        #print(df2.toz_pos, z_weight_markdown())
        #print(df1.to_markdown())
        for i in range(len(df1)):
            bar = np.where((df2['t'].values >= df1['t'].loc[i]) & (df2['t'].values <= df1['t'].loc[i] + self.param.max_travel_time))[0]
            zp, zw = self.Z_distribution(df1, df2, i, bar)
            if zp:
                for j in range(len(zp)):
                    z_pos.append(zp[j])
                    z_weight.append(zw[j])
        df_z = pd.DataFrame({'z_pos': z_pos, 'z_weight': z_weight})
        df_z = df_z.sort_values(by = 'z_pos')
        return df_z
        


    def Z_distribution(self, df1, df2, i, bar):
        z_temp = np.zeros(200)
        z_vals, z_weight = [], []
        r1 = df1['r'].loc[i]
        z1 = df1['z'].loc[i]
        tossed = 0
        for j in bar:
            r2 = df2['r'].loc[j]
            z2 = df2['z'].loc[j]
            z_pos = self.FindOriginZ_extrapolate(r1, r2, z1, z2)
            if (z_pos < self.param.last_fiber_position) and (z_pos >-self.param.last_fiber_position):
                z_vals.append(z_pos)
            else: 
                tossed  += 1

        if bar.size != tossed:
            z_weight = np.ones(len(z_vals))/(bar.size - tossed)

        return z_vals, z_weight


    def FindOriginZ(self,r1,r2,z1,z2):
        dr = r2-r1
        dz = z2-z1
        tan_theta = dz/dr
        dD = tan_theta*r2 
        z_pos = z2 - dD
        return z_pos

    def FindOriginZ_extrapolate(self,r1,r2,z1,z2):
        """ 
        #Using that f(x) = a*x + b
        """
        if z2 != z1:
            a = (r2-r1)/(z2-z1)
            b = r1 - a*z1
            return -b/a
        else: 
            return z1                
