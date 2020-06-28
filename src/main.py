from ReadFiles import ReadFiles
from Setup import Setup
from plot import plot

import time

start = time.time()

PathData = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
folder   = 'Data/'
RF = ReadFiles(PathData, folder)
data = RF.ToCSV()

src = Setup(data)
data = src.construct() 

#P = plot(data)
#P.plot_FACT()


end = time.time()
print('Full Run: %.2f' % (end - start), 's')


