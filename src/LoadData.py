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


class LoadData():
    """ Load all data
    """

    def __init__(self, path_settings_csv):
        self.path_settings_csv = path_settings_csv
        self.geometry = pd.read_csv(path_settings_csv, header = 0)

        # Detector Mapping Variables

        ## Layer Radius
        self.r1 = self.geometry['r1_mm'][0]                                    # mm
        self.r2 = self.geometry['r2_mm'][0]                                    # mm
        self.r3 = self.geometry['r3_mm'][0]                                    # mm
        self.r4 = self.geometry['r4_mm'][0]                                    # mm

        ## Min and max indices for Layer L
        self.L1_min = int(self.geometry['IL1_min'][0])
        self.L1_max = int(self.geometry['IL1_max'][0])
        self.L2_min = int(self.geometry['IL2_min'][0])
        self.L2_max = int(self.geometry['IL2_max'][0])
        self.L3_min = int(self.geometry['IL3_min'][0])
        self.L3_max = int(self.geometry['IL3_max'][0])
        self.L4_min = int(self.geometry['IL4_min'][0])
        self.L4_max = int(self.geometry['IL4_max'][0])

        # Fiber parameters
        self.N_fibers = int(self.geometry['N_fibers'][0])
        self.last_fiber_position = self.geometry['last_fiber_position_mm'][0]
        self.fiber_diameter = self.geometry['fiber_diameter_mm'][0]
        self.inter_fiber_dist = self.geometry['inter_fiber_dist_mm'][0]
        self.layer_offset = self.geometry['layer_offset'][0]

        # Data Selection parameters
        self.frames = int(self.geometry['frames'][0])
        self.rising_edge = int(self.geometry['edge'][0])
        self.edge_buffer = int(self.geometry['edge_buffer'][0])
        self.tail = int(self.geometry['tail'][0])
        self.tail_time = int(self.geometry['tail_time'][0])

        # Physical parameters
        self.max_travel_time = self.geometry['max_travel_time'][0]
        self.t_res = int(self.geometry['Time_resolution_ns'][0])

        # Map structure
        self.CoordinateMatrix = np.empty((0,0))

    def Initiate(self):
        """ Construct detector environment
        SetCoordinates: Builds the detector mapping
        """
        self.SetCoordinates()

    def SetCoordinates(self):
        """ Set up FACT mapping
        Builds a Matrix of size N_fibersX3, 
        holding respectivly fiber-number i, r(i) position, z(i) position
        """
        N = np.arange(0,self.N_fibers,1)
        self.CoordinateMatrix = np.empty((len(N), 3))
        self.CoordinateMatrix[:,0] = N
        self.CoordinateMatrix[:,1:] = np.NaN


        self.CoordinateMatrix[self.L1_min:self.L1_max+1,1] = self.r1
        self.CoordinateMatrix[self.L1_min:self.L1_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 1,0]*self.inter_fiber_dist+ self.layer_offset - self.last_fiber_position

        self.CoordinateMatrix[self.L2_min:self.L2_max+1,1] = self.r2
        self.CoordinateMatrix[self.L2_min:self.L2_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 2,0]*self.inter_fiber_dist - self.last_fiber_position

        self.CoordinateMatrix[self.L3_min:self.L3_max+1,1] = self.r3
        self.CoordinateMatrix[self.L3_min:self.L3_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 1,0]*self.inter_fiber_dist+self.layer_offset - self.last_fiber_position

        self.CoordinateMatrix[self.L4_min:self.L4_max+1,1] = self.r4
        self.CoordinateMatrix[self.L4_min:self.L4_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 2,0]*self.inter_fiber_dist - self.last_fiber_position


        return None

