def load_data(bearings_to_load):
    """ Reads all .csv of each bearing specified in bearings_to_load (list) and saves in a dictionary. """

    def read_csv(folder_path):
        """ Reads all .csv in the path (String) """

        files_path = sorted(os.listdir(folder_path))
        
        data = []
        for file_path in files_path:
            if file_path.endswith(".csv"):
                data.append(pd.read_csv(folder_path + '/' + file_path, usecols=[0, 1, 2, 4, 5],
                    names=['hour', 'minutes', 'sec', 'h', 'v'], header=None).values)

        return np.array(data)

    # Creating a dict with empty lists to save bearings data.
    data = dict(zip(bearings_to_load, [[]]*len(bearings_to_load)))

    for bearing in bearings_to_load:
        data[bearing] = read_csv('./data/FEMTOBearingDataSet/Bearing'+bearing[1]+'_'+bearing[2])

    return data

def imgs_to_video():
    """ Generate video from images in the './results/vibration_histogram/' directory"""

    import cv2

    image_folder = './results/vibration_histogram/'
    video_name = 'histogram.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 20, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def histogram(data):
    """ Generates a histogram for each entry in data (list / np) and save in .png format """
    
    plt.style.use('classic')
    plt.style.use('seaborn-poster')

    for i in range(len(data)):
        f = plt.figure()
        plt.hist(data[i], bins='auto', density=True, color='blue', alpha=0.7)
        plt.xlabel('Acceleration [g]')
        plt.ylabel('Probability Density')
        f.savefig("histogram"+str(i)+'.png', bbox_inches='tight')
        plt.close()

def fft_picture(data):
    """ Get an image from histograms of fft which are computed from each data (list / np) entry. """

    N = data[0][:,0].size       # Number of samples in a record.
    #fs = 25600                  # Sampling frequency.
    #f = np.linspace(0, fs, N)   # Frequency vector.

    # Compute FFT from horizontal and vertical vibration data. Select half of data.
    fft_x = np.abs(np.fft.fft(data[:, :, 0])[:, N//2:])
    fft_y = np.abs(np.fft.fft(data[:, :, 1])[:, N//2:])

    bins = 50

    # Compute histogram.
    """ Check upper and lower limit! """
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

def merge_csv(path):
    """ Process all .csv inside path (String) into one csv. """

    all_files = sorted(glob.glob(path + "/*.csv"))
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, usecols=[0, 1, 2, 4, 5], header=None)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv('./data/FEMTOBearingDataSet/CSV_Merged/Compressed.csv', header=['hour', 'minutes', 'sec', 'h', 'v'], index=False)
