from src_VisualisationTools.plot import plot
from src_BuildSystem.LoadData import LoadData
from src_BuildSystem.FileConverter import FileConverter
from src_Analysis.RunAnalysis import RunAnalysis

import time



""" Set Path Settings
MainDir:            Project Directory
FolderData:         Folder containing N datafiles for analysis
PathSettings_txt:   The subdir + txt file the settings are read from.
PathSettings_csv:   The subdir + csv file the csv file is written to.

Settings: The settings.txt file is a list of detector (FACT) spesific parameters,
stating the geometry of the detector and several physical properties described elsewhere. 
"""

MainDir           = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
FolderData        = 'Data/'
PathSettings  = '../settings/settings'


start = time.time()

# Load Data from CSV file into Pandas dataframe 
param = LoadData(PathSettings)
 

# --------------------------------------------------------------------------------------------------------------

""" Initiate Analysis:
Can either run for multiple files simultaniously or for single file evaluation.

Input:  Data location
Output: Dataframe df containing the vertex information [z_position, z_weight]

"""
RA = RunAnalysis(param, MainDir, FolderData)
df = RA.RunSingleFileAnalysis('172011_26.txt')
#df = RA.RunMultiFileAnalysis()

# --------------------------------------------------------------------------------------------------------------
""" What information to plot

P.hist(df): plots the z_position, z_weight histogram
"""
#P = plot(None, param, None)
#P.hist(df)



# Print total time spent on running the program, with plot-time
end = time.time()
print('Full Run: %.5f' % (end - start), 's')


# --------------------------------------------------------------------------------------------------------------
