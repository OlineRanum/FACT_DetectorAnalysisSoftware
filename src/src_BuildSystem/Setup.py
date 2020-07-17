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
        self.PrepareFACTData()


        return self.MainData, self.time, self.count

    def PrepareFACTData(self):
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
       
        t   = np.array(self.MainData['t'], dtype = int)//self.param.t_res
        tot = np.array(self.MainData['tot'],  dtype = int)//self.param.t_res

        # 1. Timebase from min and max time in main dataframe, with intervals corresponding to the detectors temporal resolution
        self.time = np.arange(self.MainData['t'].loc[np.argmin(self.MainData['t'])],self.MainData['t'].loc[np.argmax(self.MainData['t'])] + self.param.t_res, self.param.t_res)
        # 1. Array to be filled with the number of activated fibers at eatch time step
        self.count = np.zeros(len(self.time))

        # 2. Count number of activated fibers at eatch time t, given from main dataframe
        for i in range(len(self.MainData)):
            self.count[t[i]: t[i]+ tot[i]] += 1

        print(' BUILD count: ', self.count) 

        # Test that file is in fact a runfile and not a claibration file
        if self.EvaluateFile() is None: return None
        

        # 3. Find index where count > param.rising_edge
        EdgeIndex = int(np.argmax(self.count >= self.param.rising_edge)) - self.param.edge_buffer
        EndIndex = EdgeIndex+int(self.param.frames) 
        print('Edge Index build', EdgeIndex)

        
        # 4. Crop Data to zones restricted by EdgeIndex and EndIndex
        self.MainData = self.MainData[(self.MainData['t'] >= self.time[EdgeIndex]) &\
            (self.MainData['t'] <= self.time[EndIndex])].reset_index(drop = True)

        self.time = self.time[EdgeIndex: EndIndex]
        self.count = self.count[EdgeIndex: EndIndex]

        try: self.t0 = int(self.time[0])
        except IndexError: self.t0 = 0 

        # 5. Build Activation matrix - Must be done before the time reset - FIX THIS 
        self.ConstructActivationMatrix(self.time)
        
        # 6. Reset Time
        self.time = self.time - self.t0
        self.MainData['t'] = self.MainData['t']-self.MainData['t'].iloc[0]  

        # 7. Make Combined Database        
        CoordinateFrame = pd.DataFrame(self.param.FiberMapper, columns = ['N', 'r', 'z'])
        CoordinateFrame['N'] = CoordinateFrame['N'].astype(int)
        self.MainData = pd.merge(self.MainData, CoordinateFrame, on =['N'])   

        return self.MainData, self.count, EdgeIndex
    
    def EvaluateFile(self):
        if np.max(self.count) < self.param.rising_edge:
            print('FileTypeError: This file is a calibration file, positronium never arrived')
            return None
        else: return 'Ok File'
        
    def ConstructActivationMatrix(self, time_frame):
        """  Functionallity: 
        Build binary 2D N_fibers x Time Activation matrix for animation of activated fibers
        The Activation Matrix elements are zero if a fiber is off and one if the fiber is activated.
        
        Parameters:
            N_fibers: Number of fibers
            time_frame: time axis
            self.param.t_res: temporal resolution of detector
        Returns:
            ActivationMatrix: 2D N_fibers x Time Activation matrix
        """ 
        # Build appropriatly sized ActivationMatrix and fill with NaN values
        self.ActivationMatrix = np.empty((self.param.N_fibers, len(time_frame)))
        self.ActivationMatrix[:] = np.NaN
    
        N   = np.array(self.MainData['N'], dtype = int)
        t   = np.array(self.MainData['t'], dtype = int)//self.param.t_res
        tot = np.array(self.MainData['tot'],  dtype = int)//self.param.t_res
        t0_ = self.t0//self.param.t_res


        # Count all active fibers
        for i in range(len(N)):
            self.ActivationMatrix[N[i], t[i]-t0_:t[i]-t0_+tot[i]] = 1

        return self.ActivationMatrix   


