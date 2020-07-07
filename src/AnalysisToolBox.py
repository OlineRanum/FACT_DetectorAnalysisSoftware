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
        self.count = np.nansum(self.build.ActivationMatrix, axis = 0)
        self.TailIndex = 0

        self.Layer_1 = pd.DataFrame()
        self.Layer_2 = pd.DataFrame()
        
    def Initiate_Standard_Analysis(self):
        self.DefineTailData()
        self.FindClusters(self.Layer_1)
        self.FindClusters(self.Layer_2)

    
    def DefineTailData(self):
        self.data = self.data[self.data['t'] > self.param.tail_time].reset_index(drop = True)

        L1 = self.data[self.data['N'] < self.param.L3_min]
        L2 = self.data[self.data['N'] >= self.param.L3_min]
        CoordinateFrame = pd.DataFrame(self.param.CoordinateMatrix, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.Layer_1 = pd.merge(L1, CoordinateFrame, on =['N'])
        self.Layer_2 = pd.merge(L2, CoordinateFrame, on =['N'])
        self.Layer_1['key'] = np.arange(0, len(self.Layer_1), 1)
        self.Layer_2['key'] = np.arange(0, len(self.Layer_2), 1)

        #P = plot(self.data, self.param, self.build)
        #P.scatter(self.Layer_2['z'], self.Layer_2['r'], self.Layer_2['t'])


    def FindClusters(self, df):
        keys = np.array([])
        t, z, r = [],[],[]
        for i in range(len(df['t'])):
            df_temp = df[(abs(df['t']-df['t'].iloc[i]) <= self.param.t_res) & (abs(df['z']-df['z'].iloc[i]) <= self.param.Track_radius)]
            df_temp = df_temp[~df_temp.key.isin(keys)]
            temp_length = len(df_temp['t'])
            if temp_length > 0:
                t.append(np.sum(df_temp['t'])/temp_length)
                z.append(np.sum(df_temp['z'])/temp_length)
                r.append(np.sum(df_temp['r'])/temp_length)
                keys = np.append(keys,df_temp['key'].values)
        
        d = {'t': t, 'z': z, 'r': r}
        return pd.DataFrame(data=d)

"""
        while i < len(df):
            z = df['z'].iloc[i]
            temp_df_z = df[(df['z'] <= z+self.param.Track_radius) & (df['z'] >= z-self.param.Track_radius)]

            temp_len_z = len(temp_df_z)
            if temp_len_z > 1:
                r_, z_, t_ = self.ResolveTimeCluster(temp_df_z)
                for j in range(len(r_)):
                    values.append([r_[j],z_[j],t_[j]])
            else: 
                values.append([temp_df_z['r'].iloc[0], temp_df_z['z'].iloc[0], temp_df_z['t'].iloc[0]])
                self.k.append(temp_df_z['key'].iloc[0])
            i += temp_len_z

        
        k = np.sort(np.array(self.k))
        print(k)
        Occurences = pd.DataFrame(np.vstack(values), columns = ['r', 'z', 't'])
        print(Occurences.to_markdown())

    def ResolveTimeCluster(self, df):
        df = df.sort_values('t').reset_index(drop = True)
        j = 0
        r_, z_, t_ = [],[],[]
        while j < len(df):
            t = df['t'].iloc[j]
            temp_df_t = df[(df['t'] <= t + self.param.t_res) & (df['t'] >= t-self.param.t_res)]
            temp_len_t = len(temp_df_t)
            if temp_len_t > 1:
                r_.append(np.sum(temp_df_t['r'].values)/temp_len_t)
                z_.append(np.sum(temp_df_t['z'].values)/temp_len_t)
                t_.append(np.sum(temp_df_t['t'].values)/temp_len_t)
                for key in temp_df_t['key'].values:
                    self.k.append(key)
            else: 
                if temp_df_t['key'].iloc[0] not in self.k:    
                    r_.append(temp_df_t['r'].iloc[0])   
                    z_.append(temp_df_t['z'].iloc[0])   
                    t_.append(temp_df_t['t'].iloc[0])   
                    self.k.append(temp_df_t['key'].iloc[0])
            j += temp_len_t
        return r_, z_, t_

"""
"""
    def FindClusters(self, df):
        values = []
        i = 0
        df = df.sort_values('z').reset_index(drop = True)
        df['key'] = np.arange(0, len(df['N']),1)
        while i < len(df):
            z = df['z'].iloc[i]
            temp_df_z = df[(df['z'] <= z+self.param.Track_radius) & (df['z'] >= z-self.param.Track_radius)]

            temp_len_z = len(temp_df_z)
            if temp_len_z > 1:
                r_, z_, t_ = self.ResolveTimeCluster(temp_df_z)
                for j in range(len(r_)):
                    values.append([r_[j],z_[j],t_[j]])
            else: 
                values.append([temp_df_z['r'].iloc[0], temp_df_z['z'].iloc[0], temp_df_z['t'].iloc[0]])
                self.k.append(temp_df_z['key'].iloc[0])
            i += temp_len_z

        
        k = np.sort(np.array(self.k))
        print(k)
        Occurences = pd.DataFrame(np.vstack(values), columns = ['r', 'z', 't'])
        print(Occurences.to_markdown())

    def ResolveTimeCluster(self, df):
        df = df.sort_values('t').reset_index(drop = True)
        j = 0
        r_, z_, t_ = [],[],[]
        while j < len(df):
            t = df['t'].iloc[j]
            temp_df_t = df[(df['t'] <= t + self.param.t_res) & (df['t'] >= t-self.param.t_res)]
            temp_len_t = len(temp_df_t)
            if temp_len_t > 1:
                r_.append(np.sum(temp_df_t['r'].values)/temp_len_t)
                z_.append(np.sum(temp_df_t['z'].values)/temp_len_t)
                t_.append(np.sum(temp_df_t['t'].values)/temp_len_t)
                for key in temp_df_t['key'].values:
                    self.k.append(key)
            else: 
                if temp_df_t['key'].iloc[0] not in self.k:    
                    r_.append(temp_df_t['r'].iloc[0])   
                    z_.append(temp_df_t['z'].iloc[0])   
                    t_.append(temp_df_t['t'].iloc[0])   
                    self.k.append(temp_df_t['key'].iloc[0])
            j += temp_len_t
        return r_, z_, t_

        #self.compare(N3, N4)




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
#Using that f(x) = a*x + b
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
"""