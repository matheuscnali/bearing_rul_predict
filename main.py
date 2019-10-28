#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from utils.data_utils import csvs_merge, read_merged_csv, cumsum_derv

mpl.style.use('default')

#%% 
# Merge all csvs files of a bearing in FEMTO dataset.
# csvs_merge()

# Reading data. "vibration" or "temperature".
bearings_to_read = ["B11", "B12", "B21", "B22", "B31", "B32"]
vib_data = read_merged_csv('vibration', bearings_to_read)

# Computing vib_data cumsum and 5 point derivative.
vib_cumsum, derv = cumsum_derv(vib_data)

# %%
# Plotting derv.
ax = plt.subplot()
[ax.plot(x) for x in derv['1']]
#ax.set_ylim(0, 0.15*10**7)
plt.show()
