from src_VisualisationTools.plot import plot

import numpy as np 
import pandas as pd 


class BuildEvents():
    #Define superlayer 1 and 2
    Layer_1 = pd.DataFrame()
    Layer_2 = pd.DataFrame()


    def __init__(self, MainData, param, build):
        self.MainData = MainData
        self.param = param
        self.build = build

        
    def Initiate_Standard_Analysis(self): 
        """ Functionality: 
            Run the BASIC Analysis Functions
            NB!: The idea behind this function is to be easily integrated with a GUI at a later time,
            more functions like this may be built to correspond to functionalities in the GUI.                
            
            Parameters:  
                Is Instance
            Return: 
                Processed dataframe  
        """
        # Find data region to conider as the tail region of the data set
        self.GetTailData(self.param.tail_time,self.param.FiberMapper, self.param.L3_min)

        # Find all clusters in layer 1 and 2
        cluster_L1 = self.FindClusters(self.Layer_1,self.param.t_res, self.param.Track_radius)
        cluster_L2 = self.FindClusters(self.Layer_2, self.param.t_res, self.param.Track_radius)

        # Track all paths between clusters in layer 1 and clusters in layer 2
        df_z = self.TrackPath(cluster_L1, cluster_L2)
        return df_z


    def GetTailData(self, tail_cut, FiberMapper_, layer_cut):
        """ Functionalities:
            Find and set the fraction of the data corresponding to the tail of the activation curve

            Parameters:
                tail_cut: the time set of where to begin the evaluation of the tail region
                FiberMapper_: The detector mapping matrix
                layer_cut: The index N seperating the fibers in the lower super layer from the ones in the upper superlayer

            Returns:
                data_: A dataframe containing only the events occuring after the tail_cut marking
        """
        # Select only tail data
        self.MainData_ = self.MainData[self.MainData['t'] > tail_cut].reset_index(drop = True)
        # Make the detector mapping matrix to a mapping dataframe and merge with layer structures
        self.MainData = self.MainData_.join(pd.DataFrame({'key': np.arange(0, len(self.MainData_), 1)}))

        # Make dataframe for lower superlayer
        self.Layer_1 = self.MainData[self.MainData['N'] >= layer_cut].reset_index(drop = True)                                                   
        # Make dataframe for upper suself,self,self,self,perlayer
        self.Layer_2 = self.MainData[self.MainData['N'] < layer_cut].reset_index(drop = True)         
      

        #P = plot(self.MainData, self.param, self.build)
        #P.scatter(self.Layer_2['z'], self.Layer_2['r'], self.Layer_2['t'])


        return self.MainData_


    def FindClusters(self, df, t_resolution, radius):
        """ Functionalities:
            Find all clusters. 
            When two or more neighboring fibers are activated simultaniously, 
            whithin the restrictions from the temporal resolution of the detector,
            they can be concidered to come from the samme particle passing the layers. 

                Clusters: The binning of two or more neighboring fibers being simultaneously activated 

                Cluster Filters for fiber i and j in one super layer: 
                    1) t(i) - t(j) <= 5 ns
                    2) z(i) - z(j) = 1.2 mm
                    3) Has not been assumed part of another cluster

            """
        
        keys = np.array([])
        t, z, r = [],[],[]

        # Itterate through entire dataframe to find clusters in one given superlayer
        for i in range(len(df)):
            # Select data within the restrictions of filter 1,2 and 3
            df_temp = df[(abs(df['t']-df['t'].iloc[i]) <= t_resolution) &\
                (abs(df['z']-df['z'].iloc[i]) <= radius) & (~df.key.isin(keys))]
            print(df_temp)
            print('----------------------------------------------')
            temp_length = len(df_temp['t'])

            # If the dataframe is not empty -> Process data
            if temp_length > 0:
                t.append(np.sum(df_temp['t'])/temp_length)
                z.append(np.sum(df_temp['z'])/temp_length)
                r.append(np.sum(df_temp['r'])/temp_length)

                # Mark that data has already been processed
                keys = np.append(keys,df_temp['key'].values)

        df_verticies = pd.DataFrame({'t': t, 'z': z, 'r': r}).sort_values(['t','z']).reset_index(drop = True)

        # Recombine cluster gaps
        """ It can happen that a potential cluster is not combined in the itteration process above
        The following loop runs a doubble check to make sure that all clusters are in fact isolated clusters, 
        and performs a combination in the case of two neighboring events.
        """
        for i in range(len(df_verticies)-1):
            if (abs(df_verticies['t'].loc[i] - df_verticies['t'].loc[i+1]) <= t_resolution)\
                and (abs(df_verticies['z'].loc[i] - df_verticies['z'].loc[i+1]) <= radius):           # If in fact cluster
                df_verticies.loc[i] = df_verticies[i:i+2].mean()                                  # Take the average of the two neighbooring events and overwrite the first event
                df_verticies = df_verticies.drop([i+1]).reset_index(drop = True)                  # Drop the latter of the two events from the dataframe and reset index

        return df_verticies


    def TrackPath(self, df1, df2):
        """ 
        Assumptions:
        df1 = L1 = The layer with the smallest radius
        
        - we only concider the paths going from layer 1 to layer 2

        """

        z_pos, z_weight = [], []
        # Itterate over cluster database
        for i in range(len(df1)):
            potential_vertecies = np.where((df2['t'].values >= df1['t'].loc[i]) & (df2['t'].values <= df1['t'].loc[i] + self.param.max_travel_time))[0]
            zp, zw = self.Z_distribution(df1, df2, i, potential_vertecies)
            if zp:
                for j in range(len(zp)):
                    z_pos.append(zp[j])
                    z_weight.append(zw[j])
        df_z = pd.DataFrame({'z_pos': z_pos, 'z_weight': z_weight})
        df_z = df_z.sort_values(by = 'z_pos')
        return df_z
        


    def Z_distribution(self, df1, df2, i, potential_vertecies):
        z_vals, z_weight = [], []
        r1 = df1['r'].loc[i]
        z1 = df1['z'].loc[i]
        tossed = 0
        for j in potential_vertecies:
            r2 = df2['r'].loc[j]
            z2 = df2['z'].loc[j]
            if z1 != z2:
                z_pos = self.FindOriginZ_extrapolate(r1, r2, z1, z2)
            else: 
                z_pos = z2
            if (z_pos < self.param.last_fiber_position) and (z_pos >-self.param.last_fiber_position):
                z_vals.append(z_pos)
            else: 
                tossed  += 1

        if potential_vertecies.size != tossed:
            z_weight = np.ones(len(z_vals))/(potential_vertecies.size - tossed)

        return z_vals, z_weight

    @staticmethod
    def FindOriginZ(r1,r2,z1,z2):
        """ z_pos = z2 - dz/dr*r2 = z2 - than(theta)*r2
        """
        return z2 - (z2-z1)/(r2-r1)*r2


    @staticmethod
    def FindOriginZ_extrapolate(r1,r2,z1,z2):
        """ Using that f(x) = a*x + b
        """
        a = (r2-r1)/(z2-z1)
        return -(r1 - a*z1)/a
            

    def __repr__(self):
        return "AnalysisToolBox:\nCurrent Dataframe: \n'{}'\n'{}'\n".format(self.MainData, [print(i, ': ', self.param.__dict__[i]) for i in self.param.__dict__])
    
    def __str__(self):
        return "\nCurrent Dataframe: 'n'{}'\n'{}'\n ".format(self.MainData, [print(i, ': ', self.param.__dict__[i]) for i in self.param.__dict__])
        