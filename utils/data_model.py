import os
import pickle
import pandas as pd

class Bearing:

    def __init__(self, name, data_path, data_to_load):

        self.name = name             
        self.data = self.load_data(data_path, data_to_load)
        self.data_path = data_path

    def save_data(self):
        """ Save 'self.data' items in binary format """

        for data_name, data in self.data.items():
            with open('%s/%s.pickle' % (self.data_path, data_name), "wb") as output:
                pickle.dump(data, output, protocol=pickle.HIGHEST_PROTOCOL)

    def load_data(self, data_path, data_to_load):
        """ Load all or specified data """

        data = {}
        for data_name in os.listdir(data_path):
            
            # Getting name without extension
            name = os.path.splitext(data_name)[0]

            if data_to_load == 'all' or name in data_to_load:
               
                # Loading serialized data
                if data_name.endswith('.pickle'):
                    with open("%s/%s" % (data_path, data_name), 'rb') as input_file:    
                        data[name] = pickle.load(input_file)    
                
                # Loading .csv data
                elif data_name.endswith('.csv'):
                    data[name] = pd.read_csv('%s/%s' % (data_path, data_name))
        
        return data


def load(dataset_path, bearings_to_load, data_to_load):
    
    bearings = []
    for bearing in os.listdir(dataset_path):
    
        if bearings_to_load == 'all' or bearing in bearings_to_load:
            
            data_path = '%s/%s' % (dataset_path, bearing)
            bearings.append(Bearing(name=bearing, data_path=data_path, data_to_load=data_to_load))

    return bearings