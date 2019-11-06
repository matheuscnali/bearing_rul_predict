import os
import pickle
import pandas as pd
import time

def b_load(name):
    return pickle.load("data/binaries/" + name)

def b_save(name, data,):
    with open("data/Binaries/" + name, 'wb') as output:
        pickle.dump(data, output, protocol=pickle.HIGHEST_PROTOCOL)

def cumsum_derv(vib_data, vib_direction):

    def five_pt_derv(h, f):
        # Based on http://web.media.mit.edu/~crtaylor/calculator.html
        
        f = f[:(len(f)//5) * 5]
        return [(-25*f[i+0]+48*f[i+1]-36*f[i+2]+16*f[i+3]-3*f[i+4])/(12*h) for i, _ in enumerate(f[:-4])]

    # Vibration cummulative sum.
    vib_cumsum = { '1' : [], '2' : [], '3' : [] }

    ini =  time.time()
    print("Cumsum = " + time.time() - ini)
    for i, bearing in enumerate(vib_data):
        v_acc_power2 = vib_data[bearing][vib_direction].apply(lambda x: x**2)
        vib_cumsum[bearing[1]].append(v_acc_power2.cumsum())
    print("Cumsum = " + time.time() - ini)

    # Derivative 
    derv = { '1' : [], '2' : [], '3' : [] }
    h = 39*10**-6 # Distance between points - It's in original data in u-sec column.


    for condition in vib_cumsum:
        for bearing in vib_cumsum[condition]:
            bearing_derv = five_pt_derv(h, bearing.values)
            maxx = 0; tmp = []
            for i, _ in enumerate(bearing_derv):
                if maxx < bearing_derv[i]:
                    maxx = bearing_derv[i]
                tmp.append(maxx)
            derv[condition].append(tmp)
    
    return vib_cumsum, derv

def csvs_merge():
    """ 
    Merge all csvs files of each bearing in FEMTO dataset.
    This function expects bearing folders (e.g. Bearingx_y) in "data/FEMTO_Original/".
    The merged file is saved in "data/FEMTO_MergedCSV/".
    """

    path = "data/FEMTO_Original/"

    # For each bearing.
    for bearing_folder in os.listdir(path):
        vib = []; temp = []
        # For all files in each bearing.
        for csv_file in sorted(os.listdir(path + '/' + bearing_folder)):
            
            # Checking for ';' or ',' separator.
            if len(pd.read_csv(path + '/' + bearing_folder + '/' + csv_file).values[0]) == 1:
                separator = ';'
            else:
                separator = ','

            # Checking for vibration or temperature .csv file.
            if csv_file[0] == 'a':
                vib.append(pd.read_csv(path + '/' + bearing_folder + '/' + csv_file, sep=separator, usecols=[0,1,2,4,5], names=["hour", "min", "seg", "h_acc", "v_acc"], header=None))
            elif csv_file[0] == 't':
                temp.append(pd.read_csv(path + '/' + bearing_folder + '/' + csv_file, sep=separator, usecols=[0,1,2,4], names=["hour", "min", "seg", "temp"], header=None))
        
        # Writting files out.
        pd.concat(vib).to_csv("data/FEMTO_MergedCSV/" + bearing_folder + "_merged_vib.csv", index=False, encoding='utf-8-sig')
        
        # Some bearings don't have temperature measuraments.
        if temp != []:
            pd.concat(temp).to_csv("data/FEMTO_MergedCSV/" + bearing_folder + "_merged_temp.csv", index=False, encoding='utf-8-sig')

def read_merged_csv(data_kind, bearings_to_read):
    """ Reads all .csv in "data/FEMTO_MergedCSV/'data_kind'" returning a dict (Folder = Bearingx_y | Dict key = Bxy) """
    
    vib_data = {}
    for bearing in os.listdir("data/FEMTO_MergedCSV/vibration"):
        name = 'B' + bearing[7] + bearing[9]

        if name not in bearings_to_read:
            continue
        
        # Organizing by B{Condition}{Bearing Number
        vib_data[name] = pd.read_csv("data/FEMTO_MergedCSV/" + data_kind + "/" + bearing)

    return vib_data