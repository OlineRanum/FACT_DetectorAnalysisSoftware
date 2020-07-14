from src_BuildSystem.ReadFiles import ReadFiles
from src_BuildSystem.Setup import Setup
from src_Analysis.AnalysisToolBox import AnalysisToolBox
from src_VisualisationTools.plot import plot
import sys

import pandas as pd
import numpy as np
import os



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

        # Itterate through all files in directory
        for filename in os.listdir(self.path + self.folder):
            verticies = verticies.append(self.RunSingleFileAnalysis(filename))

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
        MainData  = build.InitiateStandardBuild() 

        # Analyse file
        ATB = AnalysisToolBox(MainData, self.param, build)
        vertecies_onefile = ATB.Initiate_Standard_Analysis()

        # Plot Live action activation
        P = plot(MainData, self.param, build)
        P.plot_FACT_live()
        
        return vertecies_onefile