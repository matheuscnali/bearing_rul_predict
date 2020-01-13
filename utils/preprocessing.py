import scipy
import numpy as np
import pandas as pd
import pyhht


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
        h = scipy.linalg.hankel(c, r)

        hankel_svd.append(scipy.linalg.svdvals(h))

    return hankel_svd


def correlation_coeffs(data, baseline, norm_interval, filter_window_size, filter_polyorder):
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
    return scipy.signal.savgol_filter(R, filter_window_size, filter_polyorder)


def get_explosion_index(df, target):
    
    highest = 0
    target_index = 0

    for i in range(target-200, target):
        if df.hankel_v.iloc[i] < 0.95:
            if highest < df.hankel_v.iloc[i]:
                highest = df.hankel_v.iloc[i]
                target_index = i

    return target_index


def step_change_point(data):

    """ Define a change point when a point p is greater than a current maximum. """

    change_points = []
    curr_max = data[0]
    
    for p in data:
        if curr_max < p:
            curr_max = p
        change_points.append(curr_max)

    return change_points 


def fft_spectrogram(data, slice_window_size, recording_time, fs):

    T = recording_time / fs
    freq = []; time = []; spec = []

    for i in range(len(data) // slice_window_size):
        fft_res = scipy.fft(data[i * slice_window_size : (i + 1) * slice_window_size])
        spec.append(2.0 / slice_window_size * np.abs(fft_res[0 : slice_window_size // 2]))
        freq.append(np.linspace(0.0, 1.0 / (2.0 * T), slice_window_size // 2))

    for i in range(len(spec)):
        time.append(np.repeat(i, slice_window_size // 2))

    return freq, time, spec


def rms(data, slice_window_size):

    rms = []
    for i in range(len(data) // slice_window_size):
        rms.append(np.sqrt(np.mean((data[i*slice_window_size:(i+1)*slice_window_size])**2)))
    
    return rms


def imfs_decomposition(data, slice_window_size):
    
    data_imfs = []
    for i in range(len(data)//slice_window_size):
        decomposer = pyhht.emd.EMD(data[i*slice_window_size:(i+1)*slice_window_size])
        data_imfs.append(decomposer.decompose())

    return data_imfs