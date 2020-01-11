import numpy as np
import pandas as pd
from scipy.linalg import hankel, svdvals
from scipy.signal import savgol_filter


def cumsum(data):
    """ Compute the cummulative sum """

    return data.apply(lambda x: x**2).cumsum()


def hankel_svdvals(data, hankel_window_size, slice_window_size):
    """ Slices data in 'slice_window_size' and compute hankel matrix singular values with 'hankel_window_size' """

    n_slices = len(data)//slice_window_size
    hankel_svd = []

    for i in range(n_slices):
        sample_data = data[slice_window_size*i : slice_window_size*(i+1)]
        c = sample_data[0:hankel_window_size]
        r = sample_data[hankel_window_size - 1:]
        h = hankel(c, r)

        hankel_svd.append(svdvals(h))

    return hankel_svd


def correlation_coeffs(data, baseline, norm_interval, filter_window, filter_polyorder):
    """ Normalizes data, select baseline data and compute the correlation coefficients """

    a, b = norm_interval
    diff = b - a

    MIN = min([min(x) for x in data])
    MAX = max([max(x) for x in data])
    DIFF = MAX - MIN

    data_norm = [diff*(x - MIN)/(DIFF) + a for x in data]
    
    x = data_norm[baseline]
    
    R = [sum(np.multiply(x, y))/(np.sqrt(sum(x**2)*sum(y**2))) for y in data_norm]

    # Passing savgol filter
    return savgol_filter(R, filter_window, filter_polyorder)


def correlation_coeffs_old(data, baseline, norm_interval, filter_window, filter_polyorder):
    """ Normalizes data, select baseline data and compute the correlation coefficients """

    a, b = norm_interval
    diff = b - a

    MIN = min([min(x) for x in data])
    MAX = max([max(x) for x in data])
    DIFF = MAX - MIN

    data_norm = [diff*(x - MIN)/(DIFF) + a for x in data]
        
    x = data_norm[baseline]

    R = [sum(np.multiply(x, y))/(np.sqrt(sum(x**2)*sum(y**2))) for y in data_norm]

    # Passing savgol filter

    return savgol_filter(R, filter_window, filter_polyorder)


def get_explosion_index(df, target):
    
    highest = 0
    target_index = 0

    for i in range(target-200, target):
        if df.hankel_v.iloc[i] < 0.95:
            if highest < df.hankel_v.iloc[i]:
                highest = df.hankel_v.iloc[i]
                target_index = i

    return target_index