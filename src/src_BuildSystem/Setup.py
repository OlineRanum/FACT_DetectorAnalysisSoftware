""" 
Main Function:: Select and restrict data, build ActivationMatrix

Constructor input:          
    data:  Single runfile (runnumber.txt)
    param: List of specified parameters from class LoadData

Output:
    self.data:  Processed dataframe with col = ['N', 't', 'tot']
                Removed all excessive information, centering around the rising edge and the 2 microseconds to follow               

-------------------------------------------------------
Functions::

    Initiate():                    Run basic analysis functions

    FindRisingEdge():              Finds the rising edge of activated fibers, indicating the arrival of positronium

    CropData():                    Restrict data to range given by rising edge and positronium decay time

    ConstructActivationMatrix():   Builds matrix for animation of activated fibers
                                   The Activation Matrix is a binary 2D matrix of N_fibers X Time, that is zero if a fiber is off
                                   and one if the fiber is activated.

    ResetTime():                   Resets the time to 0, given an index param.edge_buffer before the rising edge
"""

import numpy as np
import pandas as pd

class Setup():

    def __init__(self, data, param):
        self.param = param
        self.data = data

        # Timebase from min and max time in main dataframe, with intervals corresponding to the detectors temporal resolution
        self.time = np.arange(self.data['t'].loc[np.argmin(self.data['t'])],self.data['t'].loc[np.argmax(self.data['t'])] + self.param.t_res, self.param.t_res)
        # Array to be filled with the number of activated fibers at eatch time step
        self.count = np.zeros(len(self.time))
        # The minimum time of the main dataframe
        self.t0 = 0
        # 
        self.EdgeIndex = 0
        self.ActivationMatrix = np.empty((0,0))    

    def Initiate(self):
        # The module called from main, that run the BASIC SetUp Modules
        self.FindRisingEdge(self.data, self.param.t_res, self.param.rising_edge, self.param.edge_buffer)
        self.CropData()
        self.ConstructActivationMatrix(self.data, self.param.N_fibers, self.time, self.param.t_res)
        self.ResetTime()
        print(self.data.to_markdown())
        return self.data

    def FindRisingEdge(self, df, t_resolution, edge_lim, edge_buffer):
        t   = np.array(df['t'], dtype = int)//t_resolution
        tot = np.array(df['tot'],  dtype = int)//t_resolution
        for i in range(len(df['N'])):
            self.count[t[i]: t[i]+ tot[i]] += 1
        
        # Find index where count > param.rising_edge and give buffer = param.edge_buffer
        self.EdgeIndex = int(np.argmax(self.count >= edge_lim)-edge_buffer)
        return self.EdgeIndex, self.count

    def CropData(self):
        EndIndex_ = self.EdgeIndex+int(self.param.frames)
        tmin = self.time[self.EdgeIndex]
        tmax = self.time[EndIndex_]
        self.time = self.time[self.EdgeIndex: EndIndex_]
        self.count = self.count[self.EdgeIndex: EndIndex_]
        self.t0 = int(self.time[0])

        self.data = self.data[(self.data['t'] >= tmin) & (self.data['t'] <= tmax)].reset_index(drop = True)


    def ConstructActivationMatrix(self, df, N_fibers, time_frame, t_resolution):
        self.ActivationMatrix = np.empty((N_fibers, len(time_frame)))
        self.ActivationMatrix[:] = np.NaN
    
        N = np.array(df['N'], dtype = int)
        t = np.array(df['t'], dtype = int)
        tot = np.array(df['tot'],  dtype = int)
        t0_ = int(time_frame[0])

        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], (t[i]-t0_)//t_resolution:(t[i]-self.t0+tot[i])//t_resolution] = 1

        return self.ActivationMatrix

    def ResetTime(self):
        self.time = self.time - self.time[0]
        self.data['t'] = self.data['t']-self.data['t'].iloc[0]