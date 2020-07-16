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
import matplotlib.pyplot as plt

class Setup():  
    

    def __init__(self, MainData, param):
        self.param = param
        self.MainData = MainData

        # set natives
        self.time = np.array(0)
        self.count = np.array(0)
        # The minimum time of the main dataframe
        self.t0 = 0
        # The Index of which the number of activated fibers is above param.edge
        self.EdgeIndex = 0 
        # 2D array to be filled by N fibers x time binary values, one indicating that the fiber is active and zero that it is inactive
        # Each row in the array corresponds to a spesific fiber
        self.ActivationMatrix = np.empty((0,0))  


    def InitiateStandardBuild(self, Filename):                                        
        """ Functionality: 
        Run the BASIC SetUp Functions
        NB!: The idea behind this function is to be easily integrated with a GUI at a later time,
        more functions like this may be built to correspond to functionalities in the GUI.                
        
        Return: 
            Processed dataframe  
        """

        # Crop and clean data
        self.PrepareFactData(self.MainData, self.param.t_res, self.param.rising_edge)

        # Build Activation matrix
        self.ConstructActivationMatrix(self.MainData, self.param.N_fibers, self.time, self.param.t_res)
        
        self.time = self.time - self.time[0]
        self.MainData['t'] = self.MainData['t']-self.MainData['t'].iloc[0]  


        return self.MainData, self.time, self.count

    def PrepareFactData(self, df, t_resolution, edge_lim):
        t   = np.array(df['t'], dtype = int)//t_resolution
        tot = np.array(df['tot'],  dtype = int)//t_resolution

        # Timebase from min and max time in main dataframe, with intervals corresponding to the detectors temporal resolution
        self.time = np.arange(df['t'].loc[np.argmin(df['t'])],df['t'].loc[np.argmax(df['t'])] + self.param.t_res, self.param.t_res)
        # Array to be filled with the number of activated fibers at eatch time step
        self.count = np.zeros(len(self.time))

        
        # Count number of activated fibers at eatch time t, given from main dataframe
        for i in range(len(df)):
            self.count[t[i]: t[i]+ tot[i]] += 1

        # Test that file is in fact a runfile and not a claibration file
        if self.EvaluateFile() is None:
            return None
        

        # Find index where count > param.rising_edge
        self.EdgeIndex = int(np.argmax(self.count >= edge_lim)) -50
        EndIndex = self.EdgeIndex+int(self.param.frames) 


        # Crop Data to zones restricted by EdgeIndex and EndIndex
        self.MainData = self.MainData[(self.MainData['t'] >= self.time[self.EdgeIndex]) &\
            (self.MainData['t'] <= self.time[EndIndex])].reset_index(drop = True)

        self.time = self.time[self.EdgeIndex: EndIndex]
        self.count = self.count[self.EdgeIndex: EndIndex]

        self.t0 = int(self.time[0])

        # Reset Time

        # Make Combined Database        
        CoordinateFrame = pd.DataFrame(self.param.FiberMapper, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.MainData = pd.merge(self.MainData, CoordinateFrame, on =['N'])   

        
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

        print(t[0])

        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], t[i]-t0_:t[i]-t0_+tot[i]] = 1

        return self.ActivationMatrix   

    def EvaluateFile(self):
        if np.max(self.count) < 100:
            print('FileTypeError: This file is a calibration file, positronium never arrived')
            return None
        else:
            return 'Ok File'