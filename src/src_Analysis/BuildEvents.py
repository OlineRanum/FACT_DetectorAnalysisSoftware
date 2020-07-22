import sys
sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/")
from src_VisualisationTools.plot import plot

import numpy as np 
import pandas as pd 
import unittest, os
import matplotlib.pyplot as plt

from src_UnitTest.BuildTestingMaterial import BuildTestingMaterial
from src_UnitTest.LoadSettings_testing import LoadSettings_testing




class BuildEvents():
    #Define superlayer lower (I) and upper (U)
    Layer_I = pd.DataFrame()
    Layer_U = pd.DataFrame()


    def __init__(self, MainData, param, build, time, count):
        self.MainData = MainData
        self.param = param
        self.build = build
        self.time = time
        self.count = count

        
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
        self.SetTail(self.param.start_time, self.param.stop_time,self.param.FiberMapper, self.param.L3_min)

        # Find all clusters in layer 1 and 2
        cluster_L1 = self.FindClusters(self.Layer_I,self.param.t_res, self.param.Track_radius)
        cluster_L2 = self.FindClusters(self.Layer_U, self.param.t_res, self.param.Track_radius)

        # Track all paths between clusters in layer 1 and clusters in layer 2
        return cluster_L1, cluster_L2


    def SetTail(self, tail_start, tail_stop, FiberMapper_, layer_cut):
        """ Functionalities:
            Find and set the fraction of the data corresponding to the tail of the activation curve

            Parameters:
                tail_cut: the time set of where to begin the evaluation of the tail region
                FiberMapper_: The detector mapping matrix
                layer_cut: The index N seperating the fibers in the lower super layer from the ones in the upper superlayer

            Returns:
                data_: A dataframe containing only the events occuring after the tail_cut marking
        """
        self.time = np.arange(0, np.max(self.MainData['t'].values), 5)
        # Select only tail data
        self.MainData_ = self.MainData[(self.MainData['t'] > tail_start) & (self.MainData['t'] < tail_stop)].sort_values('t').reset_index(drop = True)
        self.time_ = self.time[tail_start//5: tail_stop//5]
        self.count_ = self.count[tail_start//5: tail_stop//5]
        #plt.plot(self.time_, self.count_[:len(self.time_)])
        #plt.show()
        
        # Make the detector mapping matrix to a mapping dataframe and merge with layer structures
        if 'key' not in self.MainData_.columns:
            self.MainData = self.MainData_.join(pd.DataFrame({'key': np.arange(0, len(self.MainData_), 1)}))

        # Set lower (Layer_I) & upper superlayer (Layer_U)
        self.Layer_I = self.MainData[self.MainData['N'] >= layer_cut].reset_index(drop = True)                                                   
        self.Layer_U = self.MainData[self.MainData['N'] < layer_cut].reset_index(drop = True)         

        return self.MainData


    def FindClusters(self, df, t_resolution, radius):
        """ Functionalities:  
            Find all clusters. 
            When two or more neighboring fibers are activated simultaniously, 
            whithin the restrictions from the temporal resolution of the detector,
            they can be concidered to come from the samme particle passing the layers. 

                Clusters: The binning of two or more neighboring fibers being simultaneously activated 

                Cluster Filters for fiber i and j in one super layer: 
                    1) t(i) - t(j) <= 5 ns   - Whitin two neighboring timebins
                    2) z(i) - z(j) = 1.2 mm
                    3) Has not been assumed part of another cluster

            """
        
        df = df.sort_values('t')

        process_keys = np.array([])
        t, z, r = [],[],[]

        # Itterate through entire dataframe to find clusters in one given superlayer
        for i in range(len(df)):
            # Select data within the restrictions of filter 1,2 and 3
            df_tempT = df[
                (abs(df['t']-df['t'].loc[i]) <= t_resolution) &\
                (~df.key.isin(process_keys))]
            for j in range(len(df_tempT)):
                df_tempZ = df_tempT[abs(df_tempT['z'] - df_tempT['z'].iloc[j]) < radius]
                if len(df_tempZ) != 0:
                    if len(df_tempZ) > 1:
                        z_ =  np.sum(df_tempZ['z'].values)/len(df_tempZ)
                        df_temp = df_tempT[abs(df_tempT['z'] - z_) < radius]
                    else: 
                        df_temp = df_tempZ

                    t.append(np.sum(df_temp['t'])/len(df_temp))
                    z.append(np.sum(df_temp['z'])/len(df_temp))
                    r.append(np.sum(df_temp['r'])/len(df_temp))
                    # Mark that data has already been processed
                    process_keys = np.append(process_keys,df_temp['key'].values)
   

        df_verticies = pd.DataFrame({'t': t, 'z': z, 'r': r}).sort_values(['t','z']).reset_index(drop = True)
  
        
        # Recombine cluster gaps
        """ FIX THIS SHIT It can happen that a potential cluster is not combined in the itteration process above
        The following loop runs a doubble check to make sure that all clusters are in fact isolated clusters, 
        and performs a combination in the case of two neighboring events.
        """
        #print(df_verticies)
        
        i  =  0
        while i < (len(df_verticies)-1):
           # print(df_verticies['t'].loc[i])
           # print('-----------------------------')
            if (abs(df_verticies['t'].loc[i] - df_verticies['t'].loc[i+1]) <= t_resolution)\
                and (abs(df_verticies['z'].loc[i] - df_verticies['z'].loc[i+1]) <= radius):           # If in fact cluster
                df_verticies.loc[i] = df_verticies[i:i+2].mean()                                  # Take the average of the two neighbooring events and overwrite the first event
                df_verticies = df_verticies.drop([i+1]).reset_index(drop = True)                  # Drop the latter of the two events from the dataframe and reset index
            i += 1
        return df_verticies
            

class TestSetup(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        cls.BTM = BuildTestingMaterial()
        cls.rnd_df, cls.rnd_matrix, cls.rnd_time = cls.BTM.PopulateRandomDatabase()
        cls.pw_df,  cls.pw_matrix,  cls.pw_time  = cls.BTM.PopulatePredefinedDatabase()
        cls.pw_df = cls.pw_df.sort_values(by = ['t']).reset_index(drop = True)
        cls.rnd_df =cls.rnd_df.sort_values(by = ['t']).reset_index(drop = True)
        cls.param = LoadSettings_testing()   

    def setUp(self):
        self.vertex_dat = df = pd.DataFrame({'z': [5/3, 14/3, 7/2, 6/4, 14/4, 5, 2], 'r': [ 1/3,1/3, 1, 1/2, 1/2, 1/2,0]})
        self.raw_dat = pd.read_csv("Example_Data/ex1_rawdata.csv")
        self.ActivationMatrix = pd.read_csv('Example_Data/ex1_ActivationMatrix.csv').values

        count = np.sum(self.ActivationMatrix, axis = 0)
        time = np.arange(0, np.max(self.raw_dat['t']), 5)
        self.ATB = BuildEvents(self.raw_dat, None, None, count, time)
        
    def test_SetTail(self):
        CoordinateMatrix_ = self.raw_dat[['N', 'r', 'z']].copy()
        
        layer_cut_predefined = 5
        tail_cut_predefined  = 20 
        
        
        testing_df = self.ATB.SetTail(tail_cut_predefined, CoordinateMatrix_.values, layer_cut_predefined)
        # NBNBNB! This shit is dependent on something else, likely to be set in settings parameter
        self.assertEqual(CoordinateMatrix_[4:]['N'].values.tolist(), testing_df['N'].values.tolist())
        self.assertEqual(CoordinateMatrix_[4:]['r'].values.tolist(), testing_df['r'].values.tolist())
        self.assertEqual(CoordinateMatrix_[4:]['z'].values.tolist(), testing_df['z'].values.tolist())


    def test_FindCluster(self):
        df = self.ATB.FindClusters(self.raw_dat, 5.1, 1.1)
        self.assertEqual(df['z'].values.tolist(), self.vertex_dat['z'].values.tolist())
        self.assertEqual(df['r'].values.tolist(), self.vertex_dat['r'].values.tolist())
    
    def tearDown(self):
        del self.vertex_dat, self.raw_dat, self.ActivationMatrix

    @classmethod
    def tearDownClass(cls):
        pass
        #del self.__class__.t_resolution, cls.N_fibers, cls.N_points, cls.nr_seed, cls.edge_lim, cls.edge_buffer

if __name__ == '__main__':
    unittest.main()



def __repr__(self):
    return "AnalysisToolBox:\nCurrent Dataframe: \n'{}'\n'{}'\n".format(self.MainData, [print(i, ': ', self.param.__dict__[i]) for i in self.param.__dict__])

def __str__(self):
    return "\nCurrent Dataframe: 'n'{}'\n'{}'\n ".format(self.MainData, [print(i, ': ', self.param.__dict__[i]) for i in self.param.__dict__])
