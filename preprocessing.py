import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data():

    """ Read all data from bearing B11 and store in data_B11 list """
    folder_path = '../FEMTOBearingDataSet/Learning_set/Bearing1_1/'
    # test = pd.DataFrame()
    # for i in range(1, 2803):
    #     f_num = str(i).rjust(5, '0')
    #     test = test.append(pd.read_csv(folder_path + 'acc_{}.csv'.format(f_num),
    #                     names=['hora', 
    #                              'minuto', 
    #                              'segundo', 
    #                              'm_sec', 
    #                              'h_acc', 
    #                              'v_acc']))
    test = pd.read_csv('bearing1_v_acc.csv')
    return test


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
    
    # data_B11 = read_data()
    df = read_data()
    print('read OK!')
    # df = df['v_acc']
    # df.to_csv('bearing1_v_acc.csv' )
    # fft(data_B11)