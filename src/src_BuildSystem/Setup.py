""" Functionality:
Select and restrict data, build ActivationMatrix

Output: 
    self.MainData:  
    Processed/cropped/cleaned dataframe with col = ['N', 't', 'tot', 'z', 'r']
    Removed all excessive information, centering around the rising edge and the t_res*frames microseconds to follow 

    If DataFrame does not detect a rising edge, the file is currently tossed away as an calibration file                              

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
        # 2D array to be filled by N fibers x time binary values, one indicating that the fiber is active and zero that it is inactive
        # Each row in the array corresponds to a spesific fiber
        self.ActivationMatrix = np.empty((0,0))  

    def InitiateStandardBuild(self, Filename):                                        
        """ Functionality: 
        Run the BASIC SetUp Functions

        NB!: The idea behind this function is to be easily integrated with a GUI at a later time,
        more functions like this may be built to correspond to functionalities in the GUI.    

        NOTE_: Fix the time-frame dependency of the Activation Matrix buiild,
        so that the function can be placed anywhere            
        
        Return: 
            Processed dataframe  
        """

        # Crop and clean data
        self.PrepareFACTData(self.MainData, self.param.t_res, self.param.rising_edge)




        return self.MainData, self.time, self.count

    def PrepareFACTData(self, df, t_resolution, edge_lim):
        """ Functionalities:
        Prepares and crops the FACT data of a single runfile
        
        1. Set up time- and count-axis 1D arrays
        2. counts all the active fibers at all timesteps in 
        3. Use count-array to locate rising edge - positronium arrival
        4. Restrict data to apropriate area around edge 
        5. Build activation matrix (Should be moved out of this module as soon as time dependency is fixxed)
        6. Set the first hit to be at t = 0
        7. Combine Root file data with coordinate matrix 
        """
        t   = np.array(df['t'], dtype = int)//t_resolution
        tot = np.array(df['tot'],  dtype = int)//t_resolution

        # 1. Timebase from min and max time in main dataframe, with intervals corresponding to the detectors temporal resolution
        self.time = np.arange(df['t'].loc[np.argmin(df['t'])],df['t'].loc[np.argmax(df['t'])] + self.param.t_res, self.param.t_res)
        # 1. Array to be filled with the number of activated fibers at eatch time step
        self.count = np.zeros(len(self.time))

        # 2. Count number of activated fibers at eatch time t, given from main dataframe
        for i in range(len(df)):
            self.count[t[i]: t[i]+ tot[i]] += 1

        # Test that file is in fact a runfile and not a claibration file
        if self.EvaluateFile() is None: return None
        

        # 3. Find index where count > param.rising_edge
        EdgeIndex = int(np.argmax(self.count >= edge_lim)) - self.param.edge_buffer
        EndIndex = EdgeIndex+int(self.param.frames) 


        # 4. Crop Data to zones restricted by EdgeIndex and EndIndex
        self.MainData = self.MainData[(self.MainData['t'] >= self.time[EdgeIndex]) &\
            (self.MainData['t'] <= self.time[EndIndex])].reset_index(drop = True)

        self.time = self.time[EdgeIndex: EndIndex]
        self.count = self.count[EdgeIndex: EndIndex]

        self.t0 = int(self.time[0])

        # 5. Build Activation matrix - Must be done before the time reset - FIX THIS 
        self.ConstructActivationMatrix(self.MainData, self.param.N_fibers, self.time, self.param.t_res)

        # 6. Reset Time
        self.time = self.time - self.t0
        self.MainData['t'] = self.MainData['t']-self.MainData['t'].iloc[0]  

        # 7. Make Combined Database        
        CoordinateFrame = pd.DataFrame(self.param.FiberMapper, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.MainData = pd.merge(self.MainData, CoordinateFrame, on =['N'])   

        return self.MainData
    
    def EvaluateFile(self):
        if np.max(self.count) < 100:
            print('FileTypeError: This file is a calibration file, positronium never arrived')
            return None
        else: return 'Ok File'
        
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
