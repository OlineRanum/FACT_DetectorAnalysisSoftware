import unittest
import pandas as pd 
import numpy as np

import sys 
sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/")

from src_Analysis.BuildEvents import BuildEvents



class TestSetup(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        cls.t_resolution =  5
        cls.N_fibers     =  10
        cls.N_points     =  19
        cls.nr_seed      = 142

        cls.edge_lim = 8
        cls.edge_buffer = 2

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

        self.assertEqual(CoordinateMatrix_[17:]['N'].values.tolist(), testing_df['N'].values.tolist())
        self.assertEqual(CoordinateMatrix_[17:]['r'].values.tolist(), testing_df['r'].values.tolist())
        self.assertEqual(CoordinateMatrix_[17:]['z'].values.tolist(), testing_df['z'].values.tolist())


    def test_FindCluster(self):
        df = self.ATB.FindClusters(self.raw_dat, 5.1, 1.1)
        self.assertEqual(df['z'].values.tolist(), self.vertex_dat['z'].values.tolist())
        self.assertEqual(df['r'].values.tolist(), self.vertex_dat['r'].values.tolist())
    
    def tearDown(self):
        del self.vertex_dat, self.raw_dat, self.ActivationMatrix

    @classmethod
    def tearDownClass(cls):
        del cls.t_resolution, cls.N_fibers, cls.N_points, cls.nr_seed, cls.edge_lim, cls.edge_buffer

if __name__ == '__main__':
    unittest.main()