import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from plot import plot
from tabulate import tabulate


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
        self.FindClusters(self.Layer_1,self.param.t_res, self.param.Track_radius)
        self.FindClusters(self.Layer_2, self.param.t_res, self.param.Track_radius)


    
    def DefineTailData(self, tail_cut, CoordinateMatrix_, layer_cut):
        self.data_ = self.data[self.data['t'] > tail_cut]
        self.data = self.data_.reset_index(drop = True)

        L1 = self.data[self.data['N'] < layer_cut]
        L2 = self.data[self.data['N'] >= layer_cut]
        CoordinateFrame = pd.DataFrame(CoordinateMatrix_, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.Layer_1 = pd.merge(L1, CoordinateFrame, on =['N'])
        self.Layer_2 = pd.merge(L2, CoordinateFrame, on =['N'])
        self.Layer_1['key'] = np.arange(0, len(self.Layer_1), 1)
        self.Layer_2['key'] = np.arange(0, len(self.Layer_2), 1)
        

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


"""

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
            r1 = self.param.CoordinateMatrix[int(df1['N'].iloc[i]),1]
            r2 = self.param.CoordinateMatrix[int(df2['N'].iloc[j]),1]
            z1 = self.param.CoordinateMatrix[int(df1['N'].iloc[i]),2]
            z2 = self.param.CoordinateMatrix[int(df2['N'].iloc[j]),2]
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
"""