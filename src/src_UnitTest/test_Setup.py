import sys 
sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/")


from src_BuildSystem.Setup import Setup
from src_UnitTest.LoadSettings_testing import LoadSettings_testing
from src_UnitTest.BuildTestingMaterial import BuildTestingMaterial

import unittest
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import seed
from numpy.random import randint

class TestSetup(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.BTM = BuildTestingMaterial()
        self.rnd_df, self.rnd_matrix, self.rnd_time = self.BTM.PopulateRandomDatabase()
        self.pw_df, self.pw_matrix, self.pw_time    = self.BTM.PopulatePredefinedDatabase()
        self.pw_df = self.pw_df.sort_values(by = ['t']).reset_index(drop = True)
        self.rnd_df = self.rnd_df.sort_values(by = ['t']).reset_index(drop = True)
        self.param = LoadSettings_testing()        

    def test_ConstructActivationMatrix(self): 
        """ Test Activation Matrix build,
        comparing to prebuilt (random/set) activation matrix
        """

        # TEST RANDOM MATRIX
        rnd_test_build = Setup(self.rnd_df, self.param)                                           # Set up testing environment for activation matrix
        rnd_MatrixBuild = rnd_test_build.ConstructActivationMatrix(self.rnd_time)                 # Build Activation matrix from module
        rnd_MatrixBuild[np.isnan(rnd_MatrixBuild)] = 0                                            # MatrixBuild Cast NaN -> 0 for assertion purposes
        self.assertEqual(np.shape(rnd_MatrixBuild),np.shape(self.rnd_matrix))                     # Assert shape, Assert equality of each matrix element

        # TEST PREDEFINED SYSTEM
        pw_test_build = Setup(self.pw_df, self.param) 
        pw_MatrixBuild = pw_test_build.ConstructActivationMatrix(self.pw_time)
        pw_MatrixBuild[np.isnan(pw_MatrixBuild)] = 0
        self.assertEqual(pw_MatrixBuild.flatten().tolist(), self.pw_matrix.flatten().tolist())
             
    def test_PrepareFACTData(self):

        test_build = Setup(self.rnd_df, self.param)
        test_count = np.sum(self.rnd_matrix, axis = 0)
        self.param.rising_edge = np.max(test_count)/10*8

        test_EdgeIndex = int(np.argmax(test_count >= self.param.rising_edge))
        self.param.frames = len(test_count) - test_EdgeIndex - 1
        build_df, build_count, build_EdgeIndex = test_build.PrepareFACTData()

        test_count = test_count[test_EdgeIndex:test_EdgeIndex + len(build_count)]

        self.assertEqual(test_EdgeIndex, build_EdgeIndex)
        self.assertEqual(test_count.tolist(), build_count.tolist())


    def tearDown(self):
        del self.rnd_df, self.rnd_matrix, self.rnd_time, self.pw_df, self.pw_matrix, self.pw_time, self.param

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()