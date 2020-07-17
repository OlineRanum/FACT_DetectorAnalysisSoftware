
import sys
sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/src_UnitTest")
from LoadSettings_testing import LoadSettings_testing

from numpy.random import seed
from numpy.random import randint
import pandas as pd 
import numpy as np  

class BuildTestingMaterial():

    def __init__(self):
        self.t_resolution =  5
        self.N_fibers     =  100
        self.N_points     =  int(1e2)
        self.nr_seed = 142
        self.edge_lim = self.N_fibers//10*5
        self.edge_buffer = 5

    def PopulateRandomDatabase(self):
        """ Generates a random set of information with a poissonian distribution along the rise
        Poisonnian distribution simulates the rising edge.
        """
        # Set random seed
        #        seed(self.nr_seed + 3)

        # Build a random raw datafile
        N = randint(0,self.N_fibers, self.N_points)
        t = np.random.poisson(10, self.N_points)*self.t_resolution
        t = t - t[np.argmin(t)]
        time = np.arange(t[np.argmin(t)], t[np.argmax(t)] + self.t_resolution, self.t_resolution)
        tot = np.random.choice(np.array([5,10]) , self.N_points)
        z = randint(0,10, self.N_points)
        r = randint(0,10, self.N_points)

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': np.arange(0, self.N_points, 1)}
        df = pd.DataFrame(data=d)
        df = df.sort_values(['t']).reset_index(drop = True)
        
        # Remove all doubly active fibers - Model the Actual Detector
        drop_index = []       

        for i in range(len(df)):
            df_temp = df[(df['N'] == df['N'].loc[i]) &(df['t'] > df['t'].loc[i]) & (df['t'] < df['t'].loc[i] + df['tot'].loc[i] + 10)]
            if len(df_temp) > 0:
                for j in df_temp.index.values:
                    drop_index.append(j)

            df_temp = df[(df['N'] == df['N'].loc[i]) &(df['t'] == df['t'].loc[i])]
            if len(df_temp) > 1:
                for j in df_temp.index.values:
                    drop_index.append(j)


        drop_index = np.unique(np.array(drop_index)).tolist()
        df = df.drop(drop_index).reset_index(drop = True)
        self.N_points = len(df)
        df = df.sort_values(['t']).reset_index(drop = True)

        # Build Activation Matrix from random raw data
        TEST_ActivationMatrix = np.zeros((self.N_fibers, len(time)))
        test_count = np.zeros(len(time))

        for i in range(len(df)):
            try:
                TEST_ActivationMatrix[df['N'].loc[i], df['t'].loc[i]//5: df['t'].loc[i]//5 + df['tot'].loc[i]//5] += 1
                test_count[df['t'].loc[i]//5: df['t'].loc[i]//5 + df['tot'].loc[i]//5] += 1
            except KeyError:
                TEST_ActivationMatrix[N[i], t[i]:] += 1
                test_count[t[i]//5:] += 1
                break

        return df.sort_values(['t']).reset_index(drop = True), TEST_ActivationMatrix, time
  
    def PopulatePredefinedDatabase(self):
        """ Generates a preworked example for futher testing
        """
        # Build Data frame base information
        N = np.arange(0, 11, 1)
        t = np.array([0,15,15,20,25,35,35,5,15,20,25])
        time = np.arange(0, t[np.argmax(t)] + 5, 5) 
        tot = np.array([10, 10, 15, 5, 5, 5,5 ,5, 5, 5, 5])
        z = np.array([5,6,9,2,1,4,5,4,5,6,2])
        r = np.array([1,1,1,1,1,1,1,2,2,2,2])

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': N}
        df = pd.DataFrame(data=d)
        
        # Build TEST_ActivationMatrix Elements
        TEST_ActivationMatrix = np.zeros((self.N_fibers, len(time)))
        TEST_ActivationMatrix[[0], 0] = 1
        TEST_ActivationMatrix[[0,7], 1] = 1
        TEST_ActivationMatrix[[1,2,8], 3] = 1
        TEST_ActivationMatrix[[1,2,3,9], 4] = 1
        TEST_ActivationMatrix[[2,4,10], 5] = 1
        TEST_ActivationMatrix[[5,6], 7] = 1

        return df, TEST_ActivationMatrix, time

    
    def build_param_testing(self):
        self.param = LoadSettings_testing()