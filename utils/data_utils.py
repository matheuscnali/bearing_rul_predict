import os
import glob
import pickle
import time
import numpy as np
import pandas as pd
import ipdb
import matplotlib.pyplot as plt
import pyhht
import scipy.fftpack
import plotly
import plotly.graph_objects as go

from scipy.linalg import hankel, svdvals
from scipy.signal import spectrogram
from scipy import signal


class Bearing:

    def __init__(self, name, dataset, condition, data, fault_kind = None, restore_results=False):
        self.name = name
        self.dataset = dataset              
        self.condition = condition          
        self.data = data 
        self.fault_kind = fault_kind
        self.results = {}

        if restore_results:
            self.load_r('all')

    def save_r(self):
        """ Save 'self.results' in binary format """
        for result_name in self.results.keys():
            with open("data/processed_data/%s/%s/%s.pickle" % (self.dataset, self.name, result_name), "wb") as output:
                pickle.dump(self.results[result_name], output, protocol=pickle.HIGHEST_PROTOCOL)

    def load_r(self, name):
        """ Load all or specified result """
        if name == "all":
            for name in os.listdir("data/processed_data/%s/%s/" % (self.dataset, self.name)): 
                if name.endswith(".pickle"):
                    with open("data/processed_data/%s/%s/%s" % (self.dataset, self.name, name), "rb") as input_file:
                        # Removing .pickle from name and loading.
                        self.results[name[:-7]] = pickle.load(input_file)    
        else:
            self.results[name] = pickle.load("data/processed_data/%s/%s/%s.pickle" % (self.dataset, self.name, name))


def csvs_merge(path, files_info, bearing, dataset):
    """ 
    Merge all .csv files in a 'folder'.
    The merged file is saved in "data/processed_data/'dataset'/'folder'/merged_files.csv".
    """

    for filename_type in files_info.keys():
        csv_files = sorted(glob.glob('%s/%s*.csv' % (path, filename_type)))
        
        # Some folders don't have all types.
        if csv_files == []:
            continue

        # Determining separator type with the first file.
        reader = pd.read_csv(csv_files[0], sep= None, iterator= True, engine='python')
        inferred_sep = reader._engine.data.dialect.delimiter

        combined_csv = pd.concat([pd.read_csv("%s" %(f), 
                                  sep=inferred_sep, 
                                  usecols=files_info[filename_type]['usecols'], 
                                  names=files_info[filename_type]['names'], header=None, engine='c') for f in csv_files])

        combined_csv.to_csv("data/processed_data/%s/%s/%s_merged.csv" %(dataset, bearing, filename_type), index=False, encoding='utf-8-sig')


def cumsum(data):
    """ Compute the vibration cummulative sum. """

    return data.apply(lambda x: x**2).cumsum()


def step_change_point(data):
    """ Define a change point when a point p is greater than a current maximum. """

    change_points = []
    curr_max = data[0]
    
    for p in data:
        if curr_max < p:
            curr_max = p
        change_points.append(curr_max)

    return change_points 


def hankel_svd(data, hankel_window_size, slice_window_size):
    """ Slices data in 'slice_window_size' and compute hankel matrix singular values with 'hankel_window_size'. """

    step_size = len(data)//slice_window_size
    hankel_svd = []

    for i in range(slice_window_size):
        sample_data = data[step_size*i : step_size*(i+1)]
        c = sample_data[0:hankel_window_size]
        r = sample_data[hankel_window_size - 1:]
        h = hankel(c, r)

        hankel_svd.append(svdvals(h))

    return hankel_svd


def correlation_coeffs2(data, baseline, norm_interval):
    """ Normalizes data, select baseline data and compute the correlation coefficients. """

    a, b = norm_interval
    diff = b - a

    MIN = min([min(x) for x in data])
    MAX = max([max(x) for x in data])
    DIFF = MAX - MIN

    data_norm = [diff*(x - MIN)/(DIFF) + a for x in data]
        
    x = data_norm[baseline]

    R = [sum(np.multiply(x, y))/(np.sqrt(sum(x**2)*sum(y**2))) for y in data_norm]

    return R


def correlation_coeffs(data, baseline_percentage, norm_interval):
    """ Normalizes data, select baseline data and compute the correlation coefficients. """

    a, b = norm_interval
    diff = b - a

    MIN = min([min(x) for x in data])
    MAX = max([max(x) for x in data])
    DIFF = MAX - MIN

    data_norm = [diff*(x - MIN)/(DIFF) + a for x in data]
        
    x = np.mean(data_norm[:int(len(data_norm)*baseline_percentage/100)], axis=0)

    R = [sum(np.multiply(x, y))/(np.sqrt(sum(x**2)*sum(y**2))) for y in data_norm]

    return R


def fft_spectrogram(data, window_size=2560*2, fs=25600):


    T = 1.0 / fs
    freq = []; time = []; spec = []

    for i in range(len(data)//window_size):
        fft_res = scipy.fftpack.fft(data[i*window_size:(i+1)*window_size])
        spec.append(2.0/window_size * np.abs(fft_res[0:window_size//2]))
        freq.append(np.linspace(0.0, 1.0/(2.0*T), window_size//2))

    for i in range(len(spec)):
        time.append(np.repeat(i, window_size//2))

    return freq, time, spec


def rms(data, window_size):

    rms = []
    for i in range(len(data)//window_size):
        rms.append(np.sqrt(np.mean((data[i*window_size:(i+1)*window_size])**2)))
    
    return rms


def imfs_decomposition(data, window_size):
    
    data_imfs = []
    for i in range(len(data)//window_size):
        decomposer = pyhht.emd.EMD(data[i*window_size:(i+1)*window_size])
        data_imfs.append(decomposer.decompose())

    return data_imfs


def cross_correlation(data, lag=1):


    data_lag = data.shift(lag).values
    return np.correlate(data.values, data_lag, "full")


def scatter3d_plot(filename, x, y, z, cmin=0, cmax=0.2):
   
   
    fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y*2,
    z=z,
    mode='markers',
    marker=dict(
        size=1.5,
        cmin=0,
        cmax=0.05,
        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.5
        ),

    )])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), 
                      scene=dict(
                      xaxis_title='Frequency (Hz)',
                      yaxis_title='Recording',
                      zaxis_title='Magnititude'))
            
    plotly.offline.plot(fig, filename=filename)