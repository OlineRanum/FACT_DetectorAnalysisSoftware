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

        z_pos, z_weight = [], []
        # Itterate over cluster database
        for i in range(len(self.Layer_I)):
            potential_vertecies = np.where((self.Layer_U['t'].values >= self.Layer_I['t'].loc[i]) &\
                (self.Layer_U['t'].values <= self.Layer_I['t'].loc[i] + self.param.max_travel_time))[0]
            zp, zw = self.Z_distribution(i, potential_vertecies)
            if zp:
                for j in range(len(zp)):
                    z_pos.append(zp[j])
                    z_weight.append(zw[j])
        df_z = pd.DataFrame({'z_pos': z_pos, 'z_weight': z_weight})
        df_z = df_z.sort_values(by = 'z_pos')
        return df_z
        


    def Z_distribution(self, i, potential_vertecies):
        """ 
        Input:
            i:                      index of 
            potential_vertecies:    list of poential verte
        """
     
        z_vals, z_weight = [], []
        r1 = self.Layer_I['r'].loc[i]
        z1 = self.Layer_I['z'].loc[i]
        tossed = 0
        for j in potential_vertecies:
            r2 = self.Layer_U['r'].loc[j]
            z2 = self.Layer_U['z'].loc[j]
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

    def test_Z_distribution(self):
        Layer_I_test = pd.DataFrame({'t': [0], 'z': [1], 'r': [1]})
        Layer_U_test = pd.DataFrame({'t': [0,0,10,0,10], 'z': [1,-2,8,3,9] , 'r': [2,2,2,2,2]}) 
        potential_vertecies = np.array([0,1,3])
        i = 0
        build = VertexReconstructor(Layer_I_test, Layer_U_test, self.param)
        build_vertecies = build.Z_distribution(i, potential_vertecies)
        actual_vertecies = [1, 4, -1]
        self.assertAlmostEqual(build_vertecies[0], actual_vertecies)

    def test_FindOriginZ_extrapolate(self):
        build = VertexReconstructor(None, None, None)
        self.assertEqual(build.FindOriginZ_extrapolate(1, 2, 1, 2), 0)
        self.assertEqual(build.FindOriginZ_extrapolate(2, 8, 5, 9), 11/3)
        self.assertEqual(build.FindOriginZ_extrapolate(-2, 3, -4, 0), -12/5)


    def test_FindOriginZ_trigonometric(self):
        build = VertexReconstructor(None, None, None)
        self.assertEqual(np.round(build.FindOriginZ_trigonometric(1, 2, 1, 2), 5), 0)
        self.assertEqual(np.round(build.FindOriginZ_trigonometric(2, 8, 5, 9),5), np.round(11/3,5))
        self.assertEqual(np.round(build.FindOriginZ_trigonometric(-2, 3, -4, 0),5), np.round(-12/5,5))

         

    def tearDown(self):
        pass #del 
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()


    