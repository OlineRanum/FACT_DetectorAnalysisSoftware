""" Functionality:
Select and restrict data, build ActivationMatrix

Output: 
    self.MainData:  
    Processed dataframe with col = ['N', 't', 'tot']
    Removed all excessive information, centering around the rising edge and the t_res*frames microseconds to follow               

Methods: 
    Initiate(), FindRisingEdge(), CropData(), ConstructActivationMatrix(), ResetTime():                  

NB!: Multiple methods has input variables are usually determined by param, 
but has the option as input to make compatible for current unit testing.  
"""

import numpy as np
import pandas as pd

class Setup():  
    

    def __init__(self, MainData, param):
        self.param = param
        self.MainData = MainData

        # Timebase from min and max time in main dataframe, with intervals corresponding to the detectors temporal resolution
        self.time = np.arange(self.MainData['t'].loc[np.argmin(self.MainData['t'])],self.MainData['t'].loc[np.argmax(self.MainData['t'])] + self.param.t_res, self.param.t_res)
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
        
        Return: 
            Processed dataframe  
        """

        self.FindRisingEdge(self.MainData, self.param.t_res, self.param.rising_edge, self.param.edge_buffer)
        self.CropData()
        self.ConstructActivationMatrix(self.MainData, self.param.N_fibers, self.time, self.param.t_res)
        self.ResetTime()
        self.CombineDatabases()

        return self.MainData

    def CombineDatabases(self):
        CoordinateFrame = pd.DataFrame(self.param.FiberMapper, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.MainData = pd.merge(self.MainData, CoordinateFrame, on =['N'])
        


    def FindRisingEdge(self, df, t_resolution, edge_lim, edge_buffer):
        """ Functionality:
        Finds the rising edge of activated fibers, indicating the arrival of positronium 
        where the point where the number of active fibers > edge_lim
        
        Parameters:                      
            df:                 MainDataframe
            t_resolution:       temporal resolution of detector
            edge_lim:           number of activated fibers to determine incoming particle burst/rising edge
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

        self.MainData = self.MainData[(self.MainData['t'] >= self.time[self.EdgeIndex]) &\
            (self.MainData['t'] <= self.time[EndIndex])].reset_index(drop = True)

        self.time = self.time[self.EdgeIndex: EndIndex]
        self.count = self.count[self.EdgeIndex: EndIndex]
        self.t0 = int(self.time[0])

    def ConstructActivationMatrix(self, df, N_fibers, time_frame, t_resolution):
        """  Functionallity: 
        Build binary 2D N_fibers x Time Activation matrix for animation of activated fibers
        The Activation Matrix elements are zero if a fiber is off and one if the fiber is activated.
        
        Parameters:
            df: MainDatafrane
            N_fibers: Number of fibers
            time_frame: time axis
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
        Resets the time of the time-axis and MainData to zero. 
        
        Returns:
            Data of relevant timeframe 
        """
        self.time = self.time - self.time[0]
        self.MainData['t'] = self.MainData['t']-self.MainData['t'].iloc[0]                  




