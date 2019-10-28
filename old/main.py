#%%
import pandas as pd
import numpy as np
import multiprocessing as mp
from PyEMD import EMD

def emd_parallel(data, output):
    
    imfs = []
    for data_part in np.array_split(data, 12):
        emd = EMD()
        imfs.append(emd(data_part))

    output.put(imfs)

def load_data(bearings):

    """ Return a dict with bearings data """
    data = {}
    for bearing in bearings:
        data[bearing] = (pd.read_csv('./data/FEMTOBearingDataSet/CSV_Merged/Bearing'
                                    + bearing[1] + '_' + bearing[2] + '.csv'))
    return data

# Loading data.
data = load_data(bearings=['B11'])

#%%
# Splitting data for multiprocessing.
data['B11'] = np.array_split(data['B11'], 8)

output = mp.Queue()
processes = [mp.Process(target=emd_parallel, args=(data['B11'][x]['v'].values, output)) for x in range(8)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

#%%
