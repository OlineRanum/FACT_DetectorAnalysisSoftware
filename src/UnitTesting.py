import unittest
import pandas as pd 
import numpy as np
from Setup import Setup
import matplotlib.pyplot as plt
# generate random floating point values
from numpy.random import seed
from numpy.random import randint


class UnitTesting(unittest.TestCase):

    def SetupTestingEnvironment(self):
        t_resolution =  5
        N_fibers     =  20
        N_points     =  int(1e4)

        # Test Preworked Matrix Sample
        df, TEST_ActivationMatrix, time = self.generate_preworked_sample()
        test_build = Setup(df, None)
        self.test_ConstructActivationMatrix(test_build, df, time, TEST_ActivationMatrix, t_resolution)

        # Test Random Matrix Sample
        df, TEST_ActivationMatrix, time = self.generate_random_sample(N_points, N_fibers)
        test_build = Setup(df, None)
        self.test_ConstructActivationMatrix(test_build, df, time, TEST_ActivationMatrix,t_resolution)


    def generate_random_sample(self, n_size, n_fibers):
        seed(142)
        N = randint(0,n_fibers, n_size)
        t = np.random.poisson(50, n_size)*5
        time = np.arange(0, t[np.argmax(t)] + 5, 5) 
        tot = (np.random.poisson(3, n_size)+1)*5
        z = randint(0,10, n_size)
        r = randint(0,10, n_size)

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': N}
        df = pd.DataFrame(data=d)

        TEST_ActivationMatrix = np.zeros((len(df['N']), len(time)))
        for i in range(len(df['N'])):
            TEST_ActivationMatrix[df['N'].iloc[i], df['t'].iloc[i]//5:(df['t'].iloc[i] + df['tot'].iloc[i])//5] = 1
        
        count = np.sum(TEST_ActivationMatrix, axis = 0)
        plt.plot(time, count)
        plt.show()

        return df, TEST_ActivationMatrix, time

    
    def generate_preworked_sample(self):
        N = np.arange(0, 11, 1)
        t = np.array([0,15,15,20,25,35,35,5,15,20,25])
        time = np.arange(t[0], t[np.argmax(t)] + 5, 5) 
        tot = np.array([10, 10, 15, 5, 5, 5,5 ,5, 5, 5, 5])
        z = np.array([5,6,9,2,1,4,5,4,5,6,2])
        r = np.array([1,1,1,1,1,1,1,2,2,2,2])

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': N}
        df = pd.DataFrame(data=d)
        
        TEST_ActivationMatrix = np.zeros((len(df['N']), len(time)))
        TEST_ActivationMatrix[[0], 0] = 1
        TEST_ActivationMatrix[[0,7], 1] = 1
        TEST_ActivationMatrix[[1,2,8], 3] = 1
        TEST_ActivationMatrix[[1,2,3,9], 4] = 1
        TEST_ActivationMatrix[[2,4,10], 5] = 1
        TEST_ActivationMatrix[[5,6], 7] = 1

        return df, TEST_ActivationMatrix, time
        


    def test_ConstructActivationMatrix(self, test_build, df, time, test_matrix, t_resolution):  

        MatrixBuild = test_build.ConstructActivationMatrix(df, len(df['N']), time, t_resolution)
  #     MatrixBuild Cast NaN->0 for comparison
        where_are_NaNs = np.isnan(MatrixBuild)
        MatrixBuild[where_are_NaNs] = 0
        self.assertEqual(MatrixBuild.flatten().tolist(), test_matrix.flatten().tolist())


        

    def test_FindRisingEdge(self, df, t_resolution):
        edge_lim = 1
        edge_buffer = 1 
        test_build.FindRisingEdge(df, t_resolution, edge_lim, edge_buffer)