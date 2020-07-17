from src_BuildSystem.ReadFiles import ReadFiles
from src_BuildSystem.Setup import Setup
from src_Analysis.BuildEvents import BuildEvents
from src_VisualisationTools.plot import plot
from src_Analysis.VertexReconstructor import VertexReconstructor

import sys, os
import pandas as pd
import numpy as np


class RunAnalysis():

    def __init__(self, param, path, folder):
        self.param = param
        self.path = path
        self.folder = folder


    def RunMultiFileAnalysis(self):
        """ Functionality:
        Running itteratively the multiple files located in path + folder = data directory,
        using RunSingleFieldAnalysis
        
        Returns:
            A dataframe containing z_pos and z_weight from all analysed runfiles
                z_pos: The position of all the extrapolated annihilation vertecies on the central z-axis
                z_weight: The weight, or count number, of the z_pos vertecies
        """

        # Empty df for filling with z_pos, z_weight information
        verticies = pd.DataFrame(columns = ['z_pos', 'z_weight'])

        # Itterate through all files in directory'
        FileCount = 0
        for filename in os.listdir(self.path + self.folder):
            print(filename)
            vert = self.RunSingleFileAnalysis(filename)
            if vert is not None:
                verticies = verticies.append(vert)
            FileCount += 1
            print(FileCount)

        return verticies.reset_index(drop = True)
    
    def RunSingleFileAnalysis(self, Filename):
        """ 
        Input: 
            Filename: Name of the file in path + folder
        output:
            The z_pos, z_weight combinations from the singular files
        """
        # Read single file
        RF = ReadFiles(self.path, self.folder, Filename)
        data = RF.GetCSV()

        # Build data setup for file
        build = Setup(data, self.param)
        MainData, time, count  = build.InitiateStandardBuild(Filename) 
        if MainData is None:
            return None

        # Find Clusters in superlayer 1 + 2 
        events = BuildEvents(MainData, self.param, build, time, count)
        CL1, CL2 = events.Initiate_Standard_Analysis()

        # Perform a track reconstruction between clusters
        construct = VertexReconstructor(CL1, CL2, self.param)
        vertecies_onefile = construct.TrackPath()

        # Plot Live action activation
        #P = plot(MainData, self.param, build)
        #P.plot_FACT_live()
        
        return vertecies_onefile