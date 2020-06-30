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
data, M2D, M = src.construct() 

P = plot(data, M2D,M)
#P.plot_FACT()
P.plot_FACT_live()

end = time.time()
print('Full Run: %.5f' % (end - start), 's')


