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
        # Run SetUp Modules
        self.FindRisingEdge()
        self.CropData()
        self.ConstructActivationMatrix()
        self.ResetTime()

        return self.data, self.ActivationMatrix

    def FindRisingEdge(self):
        t   = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)

        for i in range(len(self.data['N'])):
            self.count[t[i]//self.param.t_res: (t[i]+ tot[i])//self.param.t_res] += 1
        
        # Find index where count > param.rising_edge and give buffer = param.edge_buffer
        self.EdgeIndex = int(np.argmax(self.count >= self.param.rising_edge)-self.param.edge_buffer)

    def CropData(self):
        EndIndex = self.EdgeIndex+int(self.param.frames)
        tmin = self.time[self.EdgeIndex]
        tmax = self.time[EndIndex]

        self.time = self.time[self.EdgeIndex: EndIndex]
        self.count = self.count[self.EdgeIndex: EndIndex]
        self.t0 = int(self.time[0])

        self.data = self.data[(self.data['t'] >= tmin) & (self.data['t'] <= tmax)].reset_index(drop = True)


    def ConstructActivationMatrix(self):
        self.ActivationMatrix = np.empty((self.param.N_fibers,len(self.time)))
        self.ActivationMatrix[:] = np.NaN
    
        N = np.array(self.data['N'], dtype = int)
        t = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)

        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], (t[i]-self.t0)//self.param.t_res:(t[i]-self.t0+tot[i])//self.param.t_res] = 1


    def ResetTime(self):
        self.time = self.time - self.time[0]
        self.data['t'] = self.data['t']-self.data['t'].iloc[0]