import sys 
sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/")


from src_BuildSystem.Setup import Setup
from src_UnitTest.BuildTestingMaterial import BuildTestingMaterial

import unittest
import pandas as pd 
import numpy as np
from numpy.random import seed
from numpy.random import randint

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
        self.BTM = BuildTestingMaterial()
        self.rnd_df, self.rnd_matrix, self.rnd_time = self.BTM.PopulateRandomDatabase()
        self.pw_df, self.pw_matrix, self.pw_time    = self.BTM.PopulatePredefinedDatabase()
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

if __name__ == '__main__':
    unittest.main()