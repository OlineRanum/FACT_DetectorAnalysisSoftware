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

NB!: Multiple functions has input variables are usually determined by param, 
     but has the option as input to make compatible for current unit testing.
        
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
        # The Index of which the number of activated fibers is above param.edge
        self.EdgeIndex = 0
        # 2D array to be filled by N fibers x time binary values, one indicating that the fiber is active and zero that it is inactive
        # Each row in the array corresponds to a spesific fiber
        self.ActivationMatrix = np.empty((0,0))  


    def InitiateStandardBuild(self):                                        
        """ Functionality: 
        Run the BASIC SetUp Functions
        NB!: The idea behind this function is to be easily integrated with a GUI at a later time,
        more functions like this may be built to correspond to functionalities in the GUI.                
        
        Parameters:  
            Is Instance
        Return: 
            Processed dataframe  
        """

        self.FindRisingEdge(self.data, self.param.t_res, self.param.rising_edge, self.param.edge_buffer)
        self.CropData()
        self.ConstructActivationMatrix(self.data, self.param.N_fibers, self.time, self.param.t_res)
        self.ResetTime()
        self.CombineDatabases()

        return self.data

    def CombineDatabases(self):
        CoordinateFrame = pd.DataFrame(self.param.CoordinateMatrix, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.data = pd.merge(self.data, CoordinateFrame, on =['N'])
        


    def FindRisingEdge(self, df, t_resolution, edge_lim, edge_buffer):
        """ Functionality:
        Finds the point where the number of active fibers > edge_lim
        
        Parameters:                      
            df:                 main dataframe
            t_resolution:       temporal resolution of detector
            edge_lim:           number of activated fibers to determine incoming particle burst
            edge_buffer:        the index of witch to start the current analysis of the data
        Return:
            EdgeIndex:          Index where rising edge (N_fibers activated > treshold edge_lim) is found
            Count:              Array containing the number of activated fibers at each time t
        """

        t   = np.array(df['t'], dtype = int)//t_resolution
        tot = np.array(df['tot'],  dtype = int)//t_resolution
        
        # Count number of activated fibers at eatch time t, given from main dataframe
        for i in range(len(df)):
            self.count[t[i]: t[i]+ tot[i]] += 1

        # Find index where count > param.rising_edge and give buffer = param.edge_buffer
        self.EdgeIndex = int(np.argmax(self.count >= edge_lim)-edge_buffer)

        return self.EdgeIndex, self.count

    def CropData(self):
        """ Functionality:
        Crop data to only contain data where t > t(rising_edge) - t(edge_buffer) to t < t(N_frames)
        
        Returns:
            Cropped main dataframe, timebase and count
        """
        
        EndIndex = self.EdgeIndex+int(self.param.frames)

        self.data = self.data[(self.data['t'] >= self.time[self.EdgeIndex]) &\
            (self.data['t'] <= self.time[EndIndex])].reset_index(drop = True)

        self.time = self.time[self.EdgeIndex: EndIndex]
        self.count = self.count[self.EdgeIndex: EndIndex]
        self.t0 = int(self.time[0])

    def ConstructActivationMatrix(self, df, N_fibers, time_frame, t_resolution):
        """  Functionallity: 
        Build binary 2D N_fibers x Time Activation matrix

        Parameters:
            df: main dataframe
            N_fibers: Number of fibers
            time_frame: time base
            t_resolution: temporal resolution of detector
        Returns:
            ActivationMatrix: 2D N_fibers x Time Activation matrix
        
        """ 
        # Build appropriatly sized ActivationMatrix and fill with NaN values
        self.ActivationMatrix = np.empty((N_fibers, len(time_frame)))
        self.ActivationMatrix[:] = np.NaN
    
        N   = np.array(df['N'], dtype = int)
        t   = np.array(df['t'], dtype = int)//t_resolution
        tot = np.array(df['tot'],  dtype = int)//t_resolution
        t0_ = self.t0//t_resolution

        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], t[i]-t0_:t[i]-t0_+tot[i]] = 1

        return self.ActivationMatrix

    def ResetTime(self):
        """ Functionality: 
        Resets the time of the time base and main dataframe to zero. 
        
        Returns:
            Data of relevant timeframe 
        """
        self.time = self.time - self.time[0]
        self.data['t'] = self.data['t']-self.data['t'].iloc[0]                  




