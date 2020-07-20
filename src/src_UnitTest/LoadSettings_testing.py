import pandas as pd 
import numpy as np 

class LoadSettings_testing():


    def __init__(self):

        self.nr_seed = 142

        ## Layer Radius
        self.r1 = 0                                         # [mm]  Radius of lower-inner superlayer L1            
        self.r2 = 0                                         # [mm]  Radius of upper-inner superlayer L2
        self.r3 = 0                                         # [mm]  Radius of lower-outer superlayer L3
        self.r4 = 0                                         # [mm]  Radius of upper-outer superlayer L4

        ## Min and max indices for Layer L      
        self.L1_min = 0                              # [# int] Index of first fiber in layer L1       
        self.L1_max = 0                              # [# int] Index of last fiber in layer L1
        self.L2_min = 0                              # [# int] Index of first fiber in layer L2
        self.L2_max = 0                              # [# int] Index of last fiber in layer L2
        self.L3_min = 0                              # [# int] Index of first fiber in layer L3
        self.L3_max = 0                              # [# int] Index of last fiber in layer L3
        self.L4_min = 0                              # [# int] Index of first fiber in layer L4
        self.L4_max = 0                              # [# int] Index of last fiber in layer L4

        # Fiber parameters
        self.N_fibers            = 100                         # [# int] Number of fibers in detector
        self.N_points            = int(1e2)
        self.last_fiber_position = 10                         # [mm] The length from the central fiber to the outermost fiber in layer L1 and L3
        self.fiber_diameter      = 0                 # [mm] The diameter of a single fiber thread 
        self.inter_fiber_dist    = 0                    #[mm] The distance between the center of each fiber
        self.layer_offset        = 0                        # [mm] The relative z-position difference between the center axis of two neighboring fibers in two separate sublayers

        # Data Selection parameters
        self.frames      = 5                               # [# int] The time frame of the evaluated data, given by a frame index typically of 500
        self.rising_edge = 5                            # [# int] A number of simultaniously activated fibers indicating the incoming porsitronium burst
        self.edge_buffer = 0
        self.tail        = 0                                   # [# int] A number of simultaniously activated fibers indicating the region to concider for analysis on the activation curve tail
        self.tail_time   = 0                             # [% 0-100] A time indicating the region to concider for analysis on the activation curve tail

        # Physical parameters
        self.max_travel_time = 0                  # [ns] The maximum allowed and possible traveling time for the particle in concideration between the two superlayers
        self.t_res           = 5                    # [ns] The time resolution of the electronic readoutsystem
        self.Track_radius    = 0                        # [mm] The radius around the central axis of a singular fiber of where to look for cluster-effects


        self.FiberMapper = pd.DataFrame({'N': np.arange(0, self.N_fibers, 1), 'r': np.arange(0, self.N_fibers, 1), 'z': np.arange(0, self.N_fibers, 1)})