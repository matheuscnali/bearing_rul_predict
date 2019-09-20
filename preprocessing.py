import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data():

    """ Read all data from bearing B11 and store in data_B11 list """
    folder_path = './data/FEMTOBearingDataSet/Learning_set/Bearing1_1/'
    files_path = sorted(os.listdir(folder_path))
    
    data_B11 = []
    for file_path in files_path:
        if file_path.endswith(".csv"):
            # Reading horizontal [4] and vertical [5] vibration.
            data_B11.append(pd.read_csv(folder_path + '/' + file_path, usecols=[4, 5], names=['h','v'], header=None).values)

    return np.array(data_B11)


def fft(data):
    
    N = data[0][:,0].size       # Number of samples in a record.
    fs = 25600                  # Sampling frequency.
    f = np.linspace(0, fs, N)   # Frequency vector.

    # Compute FFT from horizontal and vertical vibration data. Select half of data.
    fft_x = np.abs(np.fft.fft(data[:, :, 0])[:, N//2:])
    fft_y = np.abs(np.fft.fft(data[:, :, 1])[:, N//2:])

    bins = 50

    # Compute histogram.
    """ Check upper and lower limit """
    hist_fft_x = np.array([np.histogram(x, bins, (0, 1000))[0] for x in fft_x])
    hist_fft_y = np.array([np.histogram(y, bins, (0, 1000))[0] for y in fft_y])
    
    # Split histogram data and plot.
    num_split = 10

    split_range = 0

    for hist_fft_part in np.array_split(hist_fft_x, num_split):
        split_range += len(hist_fft_part)
        plt.title('Horizontal Data - Range: [{}, {}]'.format(split_range - split_range//num_split, split_range))
        plt.imshow(hist_fft_part.T, aspect="auto")
        plt.show()

    split_range = 0
    for hist_fft_part in np.array_split(hist_fft_y, num_split):
        split_range += len(hist_fft_part)
        plt.title('Vertical Data - Range: [{}, {}]'.format(split_range - split_range//num_split, split_range))
        plt.imshow(hist_fft_part.T, aspect="auto")
        plt.show()

    # Plotting all histogram data.
    plt.imshow(hist_fft_x.T, aspect="auto")
    plt.colorbar()
    plt.title('Horizontal Data - All Data')
    plt.xlabel('Horizontal Vibration Samples')
    plt.ylabel('Bins')
    plt.show()

    plt.imshow(hist_fft_y.T, aspect="auto")
    plt.colorbar()
    plt.title('Vertical Data - All Data')
    plt.xlabel('Vertical Vibration Samples')
    plt.ylabel('Bins')
    plt.show()
    
    """
    size = 200
    for step in range(0, len(hist_fft_x), size):
        print('Range: {} : {}'.format(step, step+size))
        plt.imshow(np.array(hist_fft_x)[step:step+size,:20].T, aspect="auto")
        plt.show()
    """

if __name__ == "__main__":
    
    data_B11 = read_data()
    fft(data_B11)