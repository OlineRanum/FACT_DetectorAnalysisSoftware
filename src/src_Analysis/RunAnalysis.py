from src_BuildSystem.ReadFiles import ReadFiles
from src_BuildSystem.Setup import Setup
from src_Analysis.AnalysisToolBox import AnalysisToolBox

import pandas as pd
import numpy as np
import os



class RunAnalysis():

    def __init__(self, param, path, folder):
        self.param = param
        self.path = path
        self.folder = folder
        self.ReadFiles = ReadFiles
        self.Setup = Setup


    def RunMultiFileAnalysis(self):
        """ 
        """
        df = pd.DataFrame(columns = ['z_pos', 'z_weight'])
        for filename in os.listdir(self.path + self.folder):
            df_z = self.RunSingleFileAnalysis(filename)
            df = df.append(df_z)
        df = df.reset_index(drop = True)
        return df
    
    def RunSingleFileAnalysis(self, Filename):
        """ 
        Input: 
            Filename: Name of the file in path + folder
        output:
        """
        RF = self.ReadFiles(self.path, self.folder, Filename)
        data = RF.GetCSV()

        build = Setup(data, self.param)
        data  = build.Initiate() 

        ATB = AnalysisToolBox(data, self.param, build)
        df_z = ATB.Initiate_Standard_Analysis()

        #P = plot(data, param, build)
        #P.plot_FACT_live()

        return df_z