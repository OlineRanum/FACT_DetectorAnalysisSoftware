""" 
Class Setup:: Loads all parameters set in Settings.csv, build Coordinate Matrix

Input:          
    path_settings_csv: path to settings.csv

Direct Output:
    CoordinateMatrix: Indepentent coordinate mapping of all fibers
-------------------------------------------------------
Functions::
    SetCoordinates: Builds indepentendt coordinate mapping and stores it in Coordinate Matrix
"""

import pandas as pd 
import numpy as np

from src_BuildSystem.FileConverter import FileConverter


class LoadData():
    """ Functionality: 
    Load all data from settings.csv into the dataframe param
    """

    def __init__(self, path_settings):
        self.path_settings = path_settings

        # Convert settings file from txt to csv
        FileConverter(self.path_settings + '.csv', self.path_settings + '.txt')

        # Read CSV file containing detection parameters
        self.geometry = pd.read_csv(self.path_settings + '.csv', header = 0).drop(1)

        # Detector Mapping Variables

        ## Layer Radius
        self.r1 = self.geometry['r1_mm'][0]                                         # [mm]  Radius of lower-inner superlayer L1            
        self.r2 = self.geometry['r2_mm'][0]                                         # [mm]  Radius of upper-inner superlayer L2
        self.r3 = self.geometry['r3_mm'][0]                                         # [mm]  Radius of lower-outer superlayer L3
        self.r4 = self.geometry['r4_mm'][0]                                         # [mm]  Radius of upper-outer superlayer L4

        ## Min and max indices for Layer L      
        self.L1_min = int(self.geometry['IL1_min'][0])                              # [# int] Index of first fiber in layer L1       
        self.L1_max = int(self.geometry['IL1_max'][0])                              # [# int] Index of last fiber in layer L1
        self.L2_min = int(self.geometry['IL2_min'][0])                              # [# int] Index of first fiber in layer L2
        self.L2_max = int(self.geometry['IL2_max'][0])                              # [# int] Index of last fiber in layer L2
        self.L3_min = int(self.geometry['IL3_min'][0])                              # [# int] Index of first fiber in layer L3
        self.L3_max = int(self.geometry['IL3_max'][0])                              # [# int] Index of last fiber in layer L3
        self.L4_min = int(self.geometry['IL4_min'][0])                              # [# int] Index of first fiber in layer L4
        self.L4_max = int(self.geometry['IL4_max'][0])                              # [# int] Index of last fiber in layer L4

        # Fiber parameters
        self.N_fibers = int(self.geometry['N_fibers'][0])                           # [# int] Number of fibers in detector
        self.last_fiber_position = self.geometry['last_fiber_position_mm'][0]       # [mm] The length from the central fiber to the outermost fiber in layer L1 and L3
        self.fiber_diameter = self.geometry['fiber_diameter_mm'][0]                 # [mm] The diameter of a single fiber thread 
        self.inter_fiber_dist = self.geometry['inter_fiber_dist_mm'][0]             # [mm] The distance between the center of each fiber
        self.layer_offset = self.geometry['layer_offset'][0]                        # [mm] The relative z-position difference between the center axis of two neighboring fibers in two separate sublayers

        # Data Selection parameters
        self.frames = int(self.geometry['frames'][0])                               # [# int] The time frame of the evaluated data, given by a frame index typically of 500
        self.rising_edge = int(self.geometry['edge'][0])                            # [# int] A number of simultaniously activated fibers indicating the incoming porsitronium burst
        self.edge_buffer = int(self.geometry['edge_buffer'][0])                     # [# int] A index indicating a concideration of additional time before the edge is encountered, set to zero if no buffer is wanted 
        self.tail = int(self.geometry['tail'][0])                                   # [# int] A number of simultaniously activated fibers indicating the region to concider for analysis on the activation curve tail
        self.tail_time = int(self.geometry['tail_time'][0])                         # [ns] A time indicating the region to concider for analysis on the activation curve tail

        # Physical parameters
        self.max_travel_time = self.geometry['max_travel_time'][0]                  # [ns] The maximum allowed and possible traveling time for the particle in concideration between the two superlayers
        self.t_res = int(self.geometry['Time_resolution_ns'][0])                    # [ns] The time resolution of the electronic readoutsystem
        self.Track_radius = self.geometry['Track_radius'][0]                        # [mm] The radius around the central axis of a singular fiber of where to look for cluster-effects
 
        # Map structure
        self.FiberMapper = np.empty((0,0))                                     # An empty matrix of where to store the coordinate system connecting the fiber number, z and r position [N, r, z]
        self.SetCoordinates()
        

    def SetCoordinates(self):
        """ Functionality:
        Set up FACT mapping, Builds a Matrix of size N_fibersX3 to give [N[i], r[i], z[i]]

        Returns:
            Full Coordinate Mapping Matrix
        """
        # Prepare Matrix
        self.FiberMapper = np.empty((self.N_fibers, 3))
        self.FiberMapper[:,0] =  np.arange(0,self.N_fibers,1)
        self.FiberMapper[:,1:] = np.NaN

        # Fill Matrix
        self.FiberMapper[self.L1_min:self.L1_max+1,1] = self.r1
        self.FiberMapper[self.L1_min:self.L1_max+1,2] = self.FiberMapper[self.L1_min:self.L1_max + 1,0]*self.inter_fiber_dist+ self.layer_offset - self.last_fiber_position

        self.FiberMapper[self.L2_min:self.L2_max+1,1] = self.r2
        self.FiberMapper[self.L2_min:self.L2_max+1,2] = self.FiberMapper[self.L1_min:self.L1_max + 2,0]*self.inter_fiber_dist - self.last_fiber_position

        self.FiberMapper[self.L3_min:self.L3_max+1,1] = self.r3
        self.FiberMapper[self.L3_min:self.L3_max+1,2] = self.FiberMapper[self.L1_min:self.L1_max + 1,0]*self.inter_fiber_dist+self.layer_offset - self.last_fiber_position

        self.FiberMapper[self.L4_min:self.L4_max+1,1] = self.r4
        self.FiberMapper[self.L4_min:self.L4_max+1,2] = self.FiberMapper[self.L1_min:self.L1_max + 2,0]*self.inter_fiber_dist - self.last_fiber_position
        


if __name__ == '__main__':
    SetCoordinates()