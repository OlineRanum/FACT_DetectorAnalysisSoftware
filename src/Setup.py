import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time



class Setup():

    def __init__(self, data):
        self.data = data
        self.time = np.arange(self.data['t'].iloc[0],self.data['t'].iloc[-1], 5)
        self.count = np.empty(len(self.time))
        self.t0 = 0

        self.geometry = pd.read_csv('settings/settings.csv', header = 0)
        self.t_res = int(self.geometry['Time_resolution_ns'][0])
        self.L1_min = int(self.geometry['IL1_min'][0])
        self.L1_max = int(self.geometry['IL1_max'][0])
        self.L2_min = int(self.geometry['IL2_min'][0])
        self.L2_max = int(self.geometry['IL2_max'][0])
        self.L3_min = int(self.geometry['IL3_min'][0])
        self.L3_max = int(self.geometry['IL3_max'][0])
        self.L4_min = int(self.geometry['IL4_min'][0])
        self.L4_max = int(self.geometry['IL4_max'][0])

        self.ActivationMatrix, self.CoordinateMatrix = 0, 0
    
    def construct(self):
        self.ActiveFibers()
        self.FindRisingEdge()
        self.ConstructActivationMatrix()

        self.time = self.time - self.time[0]
        
        self.SetCoordinates()
        
        return self.data, self.ActivationMatrix, self.CoordinateMatrix



    def ActiveFibers(self):
        t = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)

        for i in range(len(self.data['N'])):
            self.count[t[i]//self.t_res: (t[i]+ tot[i])//self.t_res] += 1

        return None

    def FindRisingEdge(self):

        ix = int(np.argmax(self.count >= self.geometry['edge'][0])-self.geometry['edge_buffer'][0])
        ixm = ix+int(self.geometry['frame'][0])
        tmin = self.time[ix]
        tmax = self.time[ixm]

        self.time = self.time[ix: ixm]
        self.count = self.count[ix: ixm]
        self.t0 = int(self.time[0])


        self.data = self.data[(self.data['t'] >= tmin) & (self.data['t'] <= tmax)].reset_index(drop = True)

        return None

    def ConstructActivationMatrix(self):
        self.ActivationMatrix = np.empty((int(self.geometry['N_fibers'][0]),len(self.time)))
        self.ActivationMatrix[:] = np.NaN
    
        N = np.array(self.data['N'], dtype = int)
        t = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)
        
        for i in range(len(N)):
            self.ActivationMatrix[N[i], (t[i]-self.t0)//self.t_res:(t[i]-self.t0+tot[i])//self.t_res] = 1

        return None

    def SetCoordinates(self):
        """ All hardcoded values r and z values are in mm
        """
        start = time.time()
        N = np.arange(0,self.geometry['N_fibers'][0],1)
        self.CoordinateMatrix = np.empty((len(N), 3))
        self.CoordinateMatrix[:,0] = N
        self.CoordinateMatrix[:,1:] = np.NaN


        inter_dist_fiber = self.geometry['dist_fiber_center_mm'][0]
        scew = self.geometry['layer_scew_mm'][0]
        dist_from_center = self.geometry['dist_from_center_mm'][0]
        

        self.CoordinateMatrix[self.L1_min:self.L1_max+1,1] = self.geometry['r1_mm'][0]
        self.CoordinateMatrix[self.L1_min:self.L1_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 1,0]*inter_dist_fiber+scew - dist_from_center
        
        self.CoordinateMatrix[self.L2_min:self.L2_max+1,1] = self.geometry['r2_mm'][0]
        self.CoordinateMatrix[self.L2_min:self.L2_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 2,0]*inter_dist_fiber - dist_from_center
        
        self.CoordinateMatrix[self.L3_min:self.L3_max+1,1] = self.geometry['r3_mm'][0]
        self.CoordinateMatrix[self.L3_min:self.L3_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 1,0]*inter_dist_fiber+scew - dist_from_center
        
        self.CoordinateMatrix[self.L4_min:self.L4_max+1,1] = self.geometry['r4_mm'][0]
        self.CoordinateMatrix[self.L4_min:self.L4_max+1,2] = self.CoordinateMatrix[self.L1_min:self.L1_max + 2,0]*inter_dist_fiber - dist_from_center
        
        end = time.time()
        print('SetCoordinates: %.5f' % (end - start), 's')
        return None