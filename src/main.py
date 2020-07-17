""" DOC. 
The main.py file initiates and runs all sub-system mechanics for builds, setup, analysis & visulaizations.
"""

from src_VisualisationTools.plot import plot
from src_BuildSystem.LoadSettings import LoadSettings
from src_Analysis.RunAnalysis import RunAnalysis

import time



""" Set Path Settings
    MainDir:            Project Directory
    FolderData:         Folder containing N datafiles for analysis
    PathSettings:       The subdir the file the settings are read from, append tail of 'txt/csv'.


    Settings: The settings.txt file is a list of detector (FACT) spesific parameters,
    stating the geometry of the detector and several physical properties described elsewhere. 
"""

MainDir           = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
FolderData        = 'Data/'
PathSettings  = '../settings/settings'

# Start timer for duration of program run
start = time.time()

# Load data from settings-file into Pandas dataframe 
param = LoadSettings(PathSettings)
 

# --------------------------------------------------------------------------------------------------------------

""" Initiate Standard Analysis:
    Can either run for multiple files simultaniously (RA.RunMultiFileAnalysis) 
    or for single file evaluation (RA.RunSingleFileAnalysis).

    Input:  Location of raw datafiles (path = MainDir + FolderData) and detector paramteres param
    Output: Dataframe df containing the vertex information [z_position, z_weight]
"""

RA = RunAnalysis(param, MainDir, FolderData)
df = RA.RunSingleFileAnalysis('169613_11.txt')
#df = RA.RunMultiFileAnalysis()

# --------------------------------------------------------------------------------------------------------------
""" Plotting commands
P.hist(df): plots the z_position, z_weight histogram
"""
P = plot(None, param, None)
P.hist(df)

# --------------------------------------------------------------------------------------------------------------


# Print total time spent on running the program, with plot-time
end = time.time()
print('Full Run: %.5f' % (end - start), 's')