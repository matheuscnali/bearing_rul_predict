import os
import glob
import pickle
import time
import numpy as np
import pandas as pd
import ipdb
from scipy.linalg import hankel, svdvals


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
            with open("data/processed_data/%s/%s.pickle" % (self.name, result_name), "wb") as output:
                pickle.dump(self.results[result_name], output, protocol=pickle.HIGHEST_PROTOCOL)

    def load_r(self, name):
        """ Load all or specified result """
        if name == "all":
            for name in os.listdir("data/processed_data/%s/" % (self.name)): 
                if name.endswith(".pickle"):
                    with open("data/processed_data/%s/%s" % (self.name, name), "rb") as input_file:
                        # Removing .pickle from name and loading.
                        self.results[name[:-7]] = pickle.load(input_file)    
        else:
            self.results[name] = pickle.load("data/processed_data/%s/%s.pickle" % (self.name, name))


def csvs_merge(path, files_info, bearing):
    """ 
    Merge all .csv files in a 'folder'.
    The merged file is saved in "data/processed_data/'folder'/merged_files.csv".
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

        combined_csv.to_csv("data/processed_data/%s/%s_merged.csv" %(bearing, filename_type), index=False, encoding='utf-8-sig')


def cumsum(data):
    """ Compute the vibration cummulative sum. """

    return data.apply(lambda x: x**2).cumsum()


def step_change_point(data):
    """ Define a change point when a point p is greater than a current maximum. """

    change_points = []
    curr_max = data[0]
    
    for i, p in enumerate(data):
        if curr_max < p:
            curr_max = p
        change_points.append(curr_max)

    return change_points 


def hankel_svd(data, window_size, n_samples):
    """ Slices data in 'n_samples' and compute hankel matrix singular values with 'window_size'. """

    step_size = len(data)//n_samples
    hankel_svd = []

    for i in range(n_samples):
        sample_data = data[step_size*i : step_size*(i+1)]
        c = sample_data[0:window_size]
        r = sample_data[window_size - 1:]
        h = hankel(c, r)

        hankel_svd.append(svdvals(h))

    return hankel_svd


def correlation_coeffs(data, baseline, norm_interval):
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