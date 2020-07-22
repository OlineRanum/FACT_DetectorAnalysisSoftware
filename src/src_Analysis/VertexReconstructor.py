import numpy as np 
import pandas as pd 
import unittest

import sys

sys.path.append("/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/src/")

from src_UnitTest.LoadSettings_testing import LoadSettings_testing

class VertexReconstructor():

    def __init__(self, Layer_I, Layer_U, param):
        self.Layer_I = Layer_I
        self.Layer_U = Layer_U
        self.param = param

    def TrackPath(self):
        """ 
        Assumptions:
        self.Layer_I is the inner layer with the smaller radius
        - we only concider the paths going from layer 1 to layer 2
        """
        z_pos, z_weight, z_time = [], [], []
        # Itterate over cluster database
        for i in range(len(self.Layer_I)):
            # Select events occuring within the same time binnings, np.wer
            potential_vertecies = np.where(self.Layer_U['t'].values == self.Layer_I['t'].loc[i])[0]
            #potential_vertecies = np.where((self.Layer_U['t'].values >= self.Layer_I['t'].loc[i]) &\
            #    (self.Layer_U['t'].values <= self.Layer_I['t'].loc[i] + self.param.max_travel_time))[0]
            # Calculate the events that relates in time to the i'th lower layer event
            zp, zw, zt = self.Z_distribution(i, potential_vertecies)
            # If zp is not empty -> I.e. a particle crossed both layers 
            if zp:
                for j in range(len(zp)):
                    z_pos.append(zp[j])
                    z_weight.append(zw[j])
                    z_time.append(zt)

        # Put everything back into a dataframe
        df_z = pd.DataFrame({'z_pos': z_pos, 'z_weight': z_weight,  'z_time': z_time})
        return df_z
        


    def Z_distribution(self, i, potential_vertecies):
        """ 
        Input:
            i:                      index of lower layer cluster for which to compare with upper layer clusters
            potential_vertecies:    list of indices of locations for potential vertecies

        Tracks and locates vertecies 
        """
     
        z_vals, z_weight = [], []
        # Lock the i'th data
        r1 = self.Layer_I['r'].loc[i]
        z1 = self.Layer_I['z'].loc[i]
        t1 = self.Layer_I['t'].loc[i]
        tossed = 0
        # TOSS Large Combinatorics
        if len(potential_vertecies) < 5:
            for j in potential_vertecies:
                r2 = self.Layer_U['r'].loc[j]
                z2 = self.Layer_U['z'].loc[j]
                if z1 != z2:
                    z_pos = self.FindOriginZ_extrapolate(r1, r2, z1, z2)
                else: 
                    z_pos = z2
                # Toss z from outside the detector 
                if (z_pos < self.param.last_fiber_position) and (z_pos >-self.param.last_fiber_position):
                    z_vals.append(z_pos)
                else: 
                    tossed  += 1

        if potential_vertecies.size != tossed:
            z_weight = np.ones(len(z_vals))/(potential_vertecies.size - tossed)

        return z_vals, z_weight, t1

    @staticmethod
    def FindOriginZ_trigonometric(r1,r2,z1,z2):
        """ z_pos = z2 - dz/dr*r2 = z2 - than(theta)*r2
        """
        return z2 - (z2-z1)/(r2-r1)*r2


    @staticmethod
    def FindOriginZ_extrapolate(r1,r2,z1,z2):
        """ Finds the point z along the central axis r = 0 where x = -b/a 
        Using that f(x) = a*x + b
        """
        a = (r2-r1)/(z2-z1)
        return -(r1 - a*z1)/a



class test_VertexReconstructor(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.param = LoadSettings_testing()       

    def test_TrackPath(self):
        Layer_I_test = pd.DataFrame({'t': [0,5,5,15,20,25], 'z': [1,0,-3,2,5,-1], 'r': [1,1,1,1,1,1]})
        Layer_U_test = pd.DataFrame({'t': [0,5,5,10,15,20], 'z': [1,3,2,5,-4,1], 'r': [2,2,2,2,2,2]})
        build = VertexReconstructor(Layer_I_test, Layer_U_test, self.param)
        solution_pos = [1, -3, -2, -9, -8, 8, 9]
        solution_weight = [1,0.5,0.5,0.5,0.5,1,1]
        build_solution = build.TrackPath()
        self.assertEqual(build_solution['z_pos'].values.tolist(), solution_pos)
        self.assertEqual(build_solution['z_weight'].values.tolist(), solution_weight)



    def test_Z_distribution(self):
        Layer_I_test = pd.DataFrame({'t': [0], 'z': [1], 'r': [1]})
        Layer_U_test = pd.DataFrame({'t': [0,0,10,0,10], 'z': [1,-2,8,3,9] , 'r': [2,2,2,2,2]}) 
        potential_vertecies = np.array([0,1,3])
        build = VertexReconstructor(Layer_I_test, Layer_U_test, self.param)
        build_vertecies = build.Z_distribution(0, potential_vertecies)
        actual_vertecies = [1, 4, -1]
        self.assertEqual(build_vertecies[0], actual_vertecies)

    def test_FindOriginZ_extrapolate(self):
        build = VertexReconstructor(None, None, None)
        self.assertEqual(build.FindOriginZ_extrapolate(1, 2, 1, 2), 0)
        self.assertEqual(build.FindOriginZ_extrapolate(2, 8, 5, 9), 11/3)
        self.assertEqual(build.FindOriginZ_extrapolate(-2, 3, -4, 0), -12/5)


    def test_FindOriginZ_trigonometric(self):
        build = VertexReconstructor(None, None, None)
        self.assertAlmostEqual(build.FindOriginZ_trigonometric(1, 2, 1, 2), 0, places = 5)
        self.assertAlmostEqual(build.FindOriginZ_trigonometric(2, 8, 5, 9), 11/3, places = 5)
        self.assertAlmostEqual(build.FindOriginZ_trigonometric(-2, 3, -4, 0), -12/5, places = 5)

         

    def tearDown(self):
        pass #del 
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()


    