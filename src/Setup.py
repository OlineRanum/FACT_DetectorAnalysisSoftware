""" 
Class Setup:: Restricts data to selected segment, build ActivationMatrix

Input:          
    data:  Single runfile (runnumber.txt)
    param: List of specified parameters from class LoadData

Direct Output:
    Activation Matrix: 2D array size N_fibers X timebin                                  /// TOSPARSE 

Indirect Output:
    Cropped data: Dataset reduced to list within edge, frame and tail restrictions from LoadData
-------------------------------------------------------
Functions::

Initiate:                    Initiate basic functions
FindRisingEdge:              Finds point in time when particles arrive
CropData:                    Restrict data to 
ConstructActivationMatrix:   Builds matrix for animation of activated fibers
ResetTime:                   Sets time frames to 0 at the given time before the rising edge
"""

import numpy as np
import pandas as pd

class Setup():

    def __init__(self, data, param):
        # Imports
        self.param = param
        self.data = data

        # Of Instance
        self.time = np.arange(self.data['t'].iloc[0],self.data['t'].iloc[-1], 5)
        self.count = np.empty(len(self.time))
        self.t0 = 0
        self.EdgeIndex = 0
        self.ActivationMatrix = np.empty((0,0))
    

    def Initiate(self):
        # The module called from main, that run the BASIC SetUp Modules
        self.FindRisingEdge(self.data, self.param.t_res, self.param.rising_edge, self.param.edge_buffer)
        self.CropData()
        self.ConstructActivationMatrix(self.data, self.param.N_fibers, self.time, self.param.t_res)
        self.ResetTime()

        return self.data

    def FindRisingEdge(self, df, t_resolution, edge_lim, edge_buffer):
        t   = np.array(df['t'], dtype = int)
        tot = np.array(df['tot'],  dtype = int)

        for i in range(len(df['N'])):
            self.count[t[i]//t_resolution: (t[i]+ tot[i])//t_resolution] = 1
        
        # Find index where count > param.rising_edge and give buffer = param.edge_buffer
        self.EdgeIndex = int(np.argmax(self.count >= edge_lim)-edge_buffer)

    def CropData(self):
        EndIndex = self.EdgeIndex+int(self.param.frames)
        tmin = self.time[self.EdgeIndex]
        tmax = self.time[EndIndex]

        self.time = self.time[self.EdgeIndex: EndIndex]
        self.count = self.count[self.EdgeIndex: EndIndex]
        self.t0 = int(self.time[0])

        self.data = self.data[(self.data['t'] >= tmin) & (self.data['t'] <= tmax)].reset_index(drop = True)


    def ConstructActivationMatrix(self, df, N_fibers, time_frame, t_resolution):
        self.ActivationMatrix = np.empty((N_fibers, len(time_frame)))
        self.ActivationMatrix[:] = np.NaN
    
        N = np.array(df['N'], dtype = int)
        t = np.array(df['t'], dtype = int)
        tot = np.array(df['tot'],  dtype = int)
        t0_ = int(time_frame[0])
        print(t0_)
        
        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], (t[i]-t0_)//t_resolution:(t[i]-self.t0+tot[i])//t_resolution] = 1

        return self.ActivationMatrix

    def ResetTime(self):
        self.time = self.time - self.time[0]
        self.data['t'] = self.data['t']-self.data['t'].iloc[0]