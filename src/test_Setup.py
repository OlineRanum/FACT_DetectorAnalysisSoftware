import unittest
import pandas as pd 
import numpy as np
from Setup import Setup
import matplotlib.pyplot as plt
# generate random floating point values
from numpy.random import seed
from numpy.random import randint

class TestSetup(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        cls.t_resolution =  5
        cls.N_fibers     =  40
        cls.N_points     =  int(1e4)
        cls.nr_seed = 142

        cls.edge_lim = cls.N_fibers//10*8
        cls.edge_buffer = 5

    def setUp(self):
        self.rnd_df, self.rnd_matrix, self.rnd_time = self.generate_random_sample()
        self.pw_df, self.pw_matrix, self.pw_time    = self.generate_preworked_sample()
        

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
             

    def FindRisingEdge(self, cls):
        test_build = Setup(self.rnd_df, None)
        test_count = np.sum(self.rnd_matrix, axis = 0)

        test_EdgeIndex = int(np.argmax(test_count >= cls.edge_lim))
        print(test_EdgeIndex)
        build_EdgeIndex, build_count = test_build.FindRisingEdge(self.rnd_df, cls.t_resolution, cls.edge_lim, 0)

        self.assertEqual(test_EdgeIndex, build_EdgeIndex)
        self.assertEqual(test_count, build_count)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def generate_random_sample(self):
        """ Generates a random set of information with a poissonian distribution along the rise
        Poisonnian distribution simulates the rising edge.
        """
        # Set random seed
        seed(self.__class__.nr_seed)

        # Build a random raw datafile
        N = randint(0,self.__class__.N_fibers, self.__class__.N_points)
        t = np.random.poisson(50, self.__class__.N_points)*self.__class__.t_resolution
        time = np.arange(0, t[np.argmax(t)] + self.__class__.t_resolution, self.__class__.t_resolution) 
        tot = (np.random.poisson(3, self.__class__.N_points)+1)*self.__class__.t_resolution
        z = randint(0,10, self.__class__.N_points)
        r = randint(0,10, self.__class__.N_points)

        d = {'N': N, 't': t, 'tot': tot, 'z': z, 'r': r, 'key': np.arange(0, self.__class__.N_points, 1)}
        df = pd.DataFrame(data=d)

        # Build Activation Matrix from randow raw data
        TEST_ActivationMatrix = np.zeros((self.__class__.N_fibers, len(time)))
        for i in range(len(df['N'])):
            TEST_ActivationMatrix[df['N'].iloc[i], df['t'].iloc[i]//self.__class__.t_resolution:(df['t'].iloc[i] + df['tot'].iloc[i])//self.__class__.t_resolution] = 1
        
        return df, TEST_ActivationMatrix, time
  
    def generate_preworked_sample(self):
        """ Generates a preworked example for futher testing
        """
        # Build Data frame base information
        N = np.arange(0, 11, 1)
        t = np.array([0,15,15,20,25,35,35,5,15,20,25])
        time = np.arange(t[0], t[np.argmax(t)] + 5, 5) 
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