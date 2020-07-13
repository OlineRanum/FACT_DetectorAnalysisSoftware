import pandas as pd


class FileConverter():

    def __init__(self, path_settings_csv, path_settings_txt):
        # Path of where to put csv file
        self.path_settings_csv = path_settings_csv
        # Path to txt file that data is read from
        self.path_settings_txt = path_settings_txt

        # Run the file converter
        self.Txt2CSV()

    def Txt2CSV(self):
        """ Functionality:
        Convert a txt to csv file for later conversion to dataframe
        """
        # Read .txt datafile from settings path
        read_file = pd.read_table(self.path_settings_txt, header = 0, sep = ' ').T
        # Write To CSV File
        read_file.to_csv(self.path_settings_csv, index=None, header = None)

