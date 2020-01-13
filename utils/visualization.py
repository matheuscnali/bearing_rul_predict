import plotly
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def scatter3d_plot(filename, x, y, z, cmin=0, cmax=0.2):
   
   
    fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=1.5,
        cmin=0,
        cmax=0.07,
        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.5
        ),

    )])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                      template='plotly_dark', 
                      scene=dict(
                      xaxis_title='Frequency (Hz)',
                      yaxis_title='Recording',
                      zaxis_title='Magnititude'))
            
    plotly.offline.plot(fig, filename=filename)


def imgs_to_video():

    """ Generate video from images in the 'image_folder' directory """

    import cv2

    image_folder = './results/'
    video_name = 'results.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 20, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def histogram(data):
    """ Generates a histogram for each entry in data (list or numpy) and save in .png format """

    plt.style.use('classic')
    plt.style.use('seaborn-poster')

    for i in range(len(data)):
        f = plt.figure()
        plt.hist(data[i], bins='auto', density=True, color='blue', alpha=0.7)
        plt.xlabel('Acceleration [g]')
        plt.ylabel('Probability Density')
        f.savefig("histogram"+str(i)+'.png', bbox_inches='tight')
        plt.close()
