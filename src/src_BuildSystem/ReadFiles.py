import pandas as pd
import numpy as np 

class ReadFiles():
    def __init__(self, path, folder, filename):
        self.path = path
        self.folder = folder
        self.filename = filename
        

    def GetCSV(self):  
        """ Functionality:
        Read a singular file of the raw FACT data files

        Returns:
            df: The main data frame of the analysis
        """
        # Read the data from raw txt file
        read_file = pd.read_table(self.path + self.folder + self.filename, header=None)
        # Push data to csv
        read_file.to_csv (self.path+'Data.csv', index=None, header = None)

        """ NOTE_: The intention here is to push all incoming data to the same CSV data file,
        so that all the data will always be readily avilable from the GUI system to perform analysis
        """
        
        # Store in a pandas dataframe structure
        df = pd.read_csv(self.path+'Data.csv', sep=",", names = ["N","t","tot"])
        # Set the time base to begin at t = 0
        df['t'] -= df['t'].loc[np.argmin(df['t'].values)]

        return df