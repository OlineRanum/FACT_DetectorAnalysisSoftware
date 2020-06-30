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

        self.M2D, self. M = 0, 0
    
    def construct(self):
        self.ActiveFibers()
        self.FindRisingEdge()

        self.Set_2D_Data()
        
        self.time = self.time - self.time[0]
        
        self.SetCoordinates()
        
        return self.data, self.M2D, self.M



    def ActiveFibers(self):
        t = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)

        for i in range(len(self.data['N'])):
            self.count[t[i]//self.t_res: (t[i]+ tot[i])//self.t_res] += 1

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

    def Set_2D_Data(self):
        self.M2D = np.empty((int(self.geometry['N_fibers'][0]),len(self.time)))
        self.M2D[:] = np.NaN
    
        N = np.array(self.data['N'], dtype = int)
        t = np.array(self.data['t'], dtype = int)
        tot = np.array(self.data['tot'],  dtype = int)
        
        for i in range(len(N)):
            self.M2D[N[i], (t[i]-self.t0)//self.t_res:(t[i]-self.t0+tot[i])//self.t_res] = 1

        return None
    
    def FindCoordinates(self):
        """ All hardcoded values r and z values are in mm
        """
        self.data['r'], self.data['z'] = np.NaN, np.NaN

        self.data.loc[self.data['N']  <= L1_max, 'r'] =  self.geometry['r1_mm'][0]
        self.data.loc[self.data['N']  <= L1_max, 'z'] = self.data['N']*1.2 + 0.6 - dist_from_center
        
        self.data.loc[(self.data['N']  >= 200) & (self.data['N'] <= 398), 'r'] = 98.0
        self.data.loc[(self.data['N']  >= 200) & (self.data['N'] <= 398), 'z'] = (self.data['N']-200)*1.2 - self.geometry['dist_from_center_mm'].iloc[0]
        
        self.data.loc[(self.data['N']  >= 400) & (self.data['N'] <= 597), 'r'] = 70.86
        self.data.loc[(self.data['N']  >= 400) & (self.data['N'] <= 597), 'z'] = (self.data['N']-400)*1.2 + 0.6 -self.geometry['dist_from_center_mm'].iloc[0]
        
        self.data.loc[self.data['N']  >= 600, 'r'] = 70.0
        self.data.loc[self.data['N']  >= 600, 'z'] = (self.data['N']-600)*1.2 - self.geometry['dist_from_center_mm'].iloc[0]

        return self.data

    def SetCoordinates(self):
        """ All hardcoded values r and z values are in mm
        """
        start = time.time()
        N = np.arange(0,self.geometry['N_fibers'][0],1)
        self.M = np.empty((len(N), 3))
        self.M[:,0] = N
        self.M[:,1:] = np.NaN


        inter_dist_fiber = self.geometry['dist_fiber_center_mm'][0]
        scew = self.geometry['layer_scew_mm'][0]
        dist_from_center = self.geometry['dist_from_center_mm'][0]
        

        self.M[self.L1_min:self.L1_max+1,1] = self.geometry['r1_mm'][0]
        self.M[self.L1_min:self.L1_max+1,2] = self.M[self.L1_min:self.L1_max + 1,0]*inter_dist_fiber+scew - dist_from_center
        
        self.M[self.L2_min:self.L2_max+1,1] = self.geometry['r2_mm'][0]
        self.M[self.L2_min:self.L2_max+1,2] = self.M[self.L1_min:self.L1_max + 2,0]*inter_dist_fiber - dist_from_center
        
        self.M[self.L3_min:self.L3_max+1,1] = self.geometry['r3_mm'][0]
        self.M[self.L3_min:self.L3_max+1,2] = self.M[self.L1_min:self.L1_max + 1,0]*inter_dist_fiber+scew - dist_from_center
        
        self.M[self.L4_min:self.L4_max+1,1] = self.geometry['r4_mm'][0]
        self.M[self.L4_min:self.L4_max+1,2] = self.M[self.L1_min:self.L1_max + 2,0]*inter_dist_fiber - dist_from_center
        
        end = time.time()
        print('SetCoordinates: %.5f' % (end - start), 's')
        return None