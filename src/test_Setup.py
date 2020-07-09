import unittest
import pandas as pd 
import numpy as np
from Setup import Setup
import sys
import matplotlib.pyplot as plt
# generate random floating point values
from numpy.random import seed
from numpy.random import randint
np.set_printoptions(threshold=np.inf)

class TestSetup(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        cls.t_resolution =  5
        cls.N_fibers     =  100
        cls.N_points     =  int(1e2)
        cls.nr_seed = 142

        cls.edge_lim = cls.N_fibers//10*5
        cls.edge_buffer = 5


    def setUp(self):
        self.rnd_df, self.rnd_matrix, self.rnd_time = self.PopulateRandomDatabase()
        self.pw_df, self.pw_matrix, self.pw_time    = self.PopulatePredefinedDatabase()
        self.pw_df = self.pw_df.sort_values(by = ['t']).reset_index(drop = True)
        self.rnd_df = self.rnd_df.sort_values(by = ['t']).reset_index(drop = True)

        

    def test_ConstructActivationMatrix(self): 
        """ Module for testing construction of Activation Matrix,
        comparing to prebuilt (random/set) activation matrix given func
        func: function that sets up the test matrix and data frame.
        """
        # Set up testing environment for activation matrix
        rnd_test_build = Setup(self.rnd_df, None) 
        pw_test_build = Setup(self.pw_df, None) 
        # Build Activation matrix from module
        rnd_MatrixBuild = rnd_test_build.ConstructActivationMatrix(self.rnd_df, self.__class__.N_fibers, self.rnd_time, self.__class__.t_resolution)
        pw_MatrixBuild = pw_test_build.ConstructActivationMatrix(self.pw_df, self.__class__.N_fibers, self.pw_time, self.__class__.t_resolution)
        # MatrixBuild Cast NaN->0 for comparison
        rnd_MatrixBuild[np.isnan(rnd_MatrixBuild)] = 0
        pw_MatrixBuild[np.isnan(pw_MatrixBuild)] = 0
        # Assert shape, Assert equality of each matrix element
        self.assertEqual(np.shape(rnd_MatrixBuild),np.shape(self.rnd_matrix))
        self.assertEqual(pw_MatrixBuild.flatten().tolist(), self.pw_matrix.flatten().tolist())
             

    def test_FindRisingEdge(self):
        test_build = Setup(self.rnd_df, None)
        test_count = np.sum(self.rnd_matrix, axis = 0)
        test_EdgeIndex = int(np.argmax(test_count >= self.__class__.edge_lim))
        build_EdgeIndex, build_count = test_build.FindRisingEdge(self.rnd_df, self.__class__.t_resolution, self.__class__.edge_lim, 0)


        self.assertEqual(test_EdgeIndex, build_EdgeIndex)
        self.assertEqual(test_count.tolist(), build_count.tolist())

    def tearDown(self):
        del self.rnd_df, self.rnd_matrix, self.rnd_time, self.pw_df, self.pw_matrix, self.pw_time  

    @classmethod
    def tearDownClass(cls):
        del cls.t_resolution, cls.N_fibers, cls.N_points, cls.nr_seed, cls.edge_lim, cls.edge_buffer

    def PopulateRandomDatabase(self):
        """ Generates a random set of information with a poissonian distribution along the rise
        Poisonnian distribution simulates the rising edge.
        """
        # Set random seed
#        seed(self.__class__.nr_seed + 3)

        # Build a random raw datafile
        N = randint(0,self.__class__.N_fibers, self.__class__.N_points)
        t = np.random.poisson(10, self.__class__.N_points)*self.__class__.t_resolution
        t = t - t[np.argmin(t)]
        time = np.arange(t[np.argmin(t)], t[np.argmax(t)] + self.__class__.t_resolution, self.__class__.t_resolution)
        tot = np.random.choice(np.array([5,10]) , self.__class__.N_points)
        z = randint(0,10, self.__class__.N_points)
        r = randint(0,10, self.__class__.N_points)

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': np.arange(0, self.__class__.N_points, 1)}
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
        TEST_ActivationMatrix = np.zeros((self.__class__.N_fibers, len(time)))
        test_count = np.zeros(len(time))

        for i in range(len(df)):
            try:
                TEST_ActivationMatrix[df['N'].loc[i], df['t'].loc[i]//5: df['t'].loc[i]//5 + df['tot'].loc[i]//5] += 1
                test_count[df['t'].loc[i]//5: df['t'].loc[i]//5 + df['tot'].loc[i]//5] += 1
            except KeyError:
                TEST_ActivationMatrix[N[i], t[i]:] += 1
                test_count[t[i]//5:] += 1
                break

        return df, TEST_ActivationMatrix, time
  
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
        TEST_ActivationMatrix = np.zeros((self.__class__.N_fibers, len(time)))
        TEST_ActivationMatrix[[0], 0] = 1
        TEST_ActivationMatrix[[0,7], 1] = 1
        TEST_ActivationMatrix[[1,2,8], 3] = 1
        TEST_ActivationMatrix[[1,2,3,9], 4] = 1
        TEST_ActivationMatrix[[2,4,10], 5] = 1
        TEST_ActivationMatrix[[5,6], 7] = 1

        return df, TEST_ActivationMatrix, time

if __name__ == '__main__':
    unittest.main()