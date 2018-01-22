import numpy as np
import csv
import os

def read_log_file(filename):
    epochs, loss, val_loss = [], [], []
    with open(filename, 'r') as cvsfile:    
        reader = csv.reader(cvsfile, delimiter=',')
        for count, row in enumerate(reader):
            if not row or not row[0].isnumeric(): continue
            #print('Row ', row)
            epochs.append(row[0])
            loss.append(row[1])
            val_loss.append(row[-1])
    return epochs, loss, val_loss
    
def read_manual_segmentation_oct_files(filename):
    """
      filename = '/home/ja/dev/Xnorm/experiments/oct/20171204_manual_segmentation/filenames.txt'
    """
    pids=[]
    image_prefixes=[]
    with open(filename, 'r') as cvsfile:
        reader = csv.reader(cvsfile, delimiter=',')
        for row in reader:
            if row[1]: pids.append(row[1])
            if row[2]: image_prefixes.append(row[2])
    return pids, image_prefixes
    

def read_atlas_images_files(filename):
    """
    #filename = '/home/ja/dev/Xnorm/experiments/oct/20170830_large_healthy_data_proc/cirrus_od_altas_folder_linux_iacl.txt'
    """
    folders=[]
    subfolders = []
    with open(filename, 'r') as cvsfile:
        reader = csv.reader(cvsfile, delimiter='/')
        for row in reader:
            if not row or len(row) == 0: continue
            subfolders.append(row[len(row)-1])
            folders.append('/'.join(row))
    return folders, subfolders  

def get_filenames(main_folder, subfolders, filename='deformed_layer_points.csv'):

    """
      main_folder : the name of the folder contain subfolders of layer-point files
      subfolders :  a list of subfolders' names
      filename : the name of a file containing layer points
    """
    filenames = []
    for subfolder in subfolders:
        filepath = os.path.join(main_folder, subfolder)
        filepath = os.path.join(filepath, filename)
        if os.path.exists(filepath):
          filenames.append(filepath)
    return filenames
  
import csv

def read_layer_points(filename, shuffle = False, verbose= False, n_scanlines=512, n_slices=128):

    def shuffle_points(points):
        idx = np.arange(points.shape[0])
        np.random.shuffle(idx)
        points = points[idx, :]
        return points
        
    each_layer_points = np.zeros((n_scanlines*n_slices, 3), dtype=np.float32)
    layer_points = dict()
    with open(filename, 'r') as cvsfile:
        reader = csv.reader(cvsfile, delimiter=',')
        label, row_cnt = 0, 0
        for count, row in enumerate(reader):

            if not row[0].isnumeric(): 
                if verbose: print('Not numeric ', row)
                continue
            if row[0] == label: # existing label
                each_layer_points[row_cnt, :] = np.float32(row[1:])
  
            else: # new label
                if label != 0: # safe pnts associated with previous label and create new data storage
                    if verbose: print('Safe to Dict: Row ', row, 'Label ', label, ' end point ', each_layer_points[-1, :])
                    each_layer_points = np.array(each_layer_points)
                    if shuffle: each_layer_points = shuffle_points(each_layer_points)
                    layer_points[label] = each_layer_points
                    each_layer_points = np.zeros((n_scanlines*n_slices, 3), dtype=np.float32)
                    row_cnt = 0
                #set new label and store a new point
                label = row[0]
                each_layer_points[row_cnt, :] = np.float32(row[1:])
                
            row_cnt+=1
            
        if label == row[0]:
            each_layer_points = np.array(each_layer_points)
            if shuffle: each_layer_points = shuffle_points(each_layer_points)
            layer_points[label] = each_layer_points
            
    return layer_points
    
# def read_layer_points(filename, shuffle = False, verbose= False, n_scanlines=512, n_slices=128):

    # def shuffle_points(points):
        # idx = np.arange(points.shape[0])
        # np.random.shuffle(idx)
        # points = points[idx, :]
        # return points
        
    # each_layer_points = np.zeros((n_scanlines*n_slices, 3), dtype=np.float32)
    # layer_points = dict()
    # with open(filename, 'r') as cvsfile:
        # reader = csv.reader(cvsfile, delimiter=',')
        # label, row_cnt = 0, 0
        # for count, row in enumerate(reader):

            # if not row[0].isnumeric(): 
                # if verbose: print('Not numeric ', row)
                # continue
            # if row[0] == label: # existing label
                # each_layer_points[row_cnt, :] = np.float32(row[1:])
  
            # else: # new label
                # if label != 0: # safe pnts associated with previous label and create new data storage
                    # if verbose: print('Safe to Dict: Row ', row, 'Label ', label, ' end point ', each_layer_points[-1, :])
                    # each_layer_points = np.array(each_layer_points)
                    # if shuffle: each_layer_points = shuffle_points(each_layer_points)
                    # layer_points[label] = each_layer_points
                    # each_layer_points = np.zeros((n_scanlines*n_slices, 3), dtype=np.float32)
                    # row_cnt = 0
                # #set new label and store a new point
                # label = row[0]
                # each_layer_points[row_cnt, :] = np.float32(row[1:])
                
            # row_cnt+=1
            
        # if label == row[0]:
          # each_layer_points = np.array(each_layer_points)
          # if shuffle: each_layer_points = shuffle_points(each_layer_points)
          # layer_points[label] = each_layer_points
            
    # return layer_points

  
def get_atlas_layer_points(filenames, shuffle=False, verbose = False, n_scanlines=512, n_slices=128):
    
    """
        filenames : a list of filename containing layer points
        return: atlas_layer_points -- a dict with label being a key and its value is a [Np x dim] of points 
    """
    atlas_layer_points = dict()
    n_files = len(filenames)
    n_points_per_file =n_scanlines*n_slices
    n_points = n_files*n_points_per_file
    start_indx, end_indx = 0,0
    
    for file_cnt, filename in enumerate(filenames):
        if verbose: print('File number ', file_cnt, ' filename ', filename)
        layer_points = read_layer_points(filename, shuffle=shuffle, verbose=verbose)
        
        for label, points in layer_points.items():

            # if label not exist, allocate array for the label in dict
            if label not in atlas_layer_points:
                atlas_layer_points[label] = np.zeros((n_points, 3), dtype=np.float32)
                end_indx = n_points_per_file
                
            # assign point
            atlas_layer_points[label][start_indx:end_indx, :] = layer_points[label]
            if verbose: print('Label ', label, '\nPoints\n', points[:2, :],'\nAssignedPnts: \n', atlas_layer_points[label][start_indx:start_indx+2, :])
            
        #debug
        if verbose: 
            print('-------------Finish one file---------------------\n')
            tmp_label = str(file_cnt+1)
            if file_cnt == 0:
                print('Label', tmp_label)
                print('Start \n', atlas_layer_points[tmp_label][start_indx:start_indx+2, :])
                print('End \n', atlas_layer_points[tmp_label][end_indx-2:end_indx, :])
            else:
                print('Label', tmp_label)
                print('Start \n', atlas_layer_points[tmp_label][start_indx-2:start_indx+2, :])
                print('End \n', atlas_layer_points[tmp_label][end_indx-2:end_indx, :])
        
        #update indices
        start_indx = end_indx
        end_indx += n_points_per_file
        if verbose: print('Start index ',start_indx, ' end index ', end_indx)
        
    return atlas_layer_points
    
def get_layer_points_for_pids(pids, atlas_subfolders, shuffle, main_folder, 
                              number_of_atlas, deformed_layer_pnt_filename = 'deformed_layer_points.csv'):
    """
    pids : a list containing strings pid
    shuffle: true or false
    
    return each patient having dict of label as a key & a list of points as a value
    """
    deformed_layer_shuffle_points4pids = dict()
    
    def shuffle_points(labeled_points):
        deformed_layer_each_pid = dict()
        for label, points in labeled_points.items():
            #print('Shape', points.shape)
            idx = np.arange(points.shape[0])
            np.random.shuffle(idx)
            points = points[idx, :]
            deformed_layer_each_pid[label] = points;
        return deformed_layer_each_pid

    for number, pid in enumerate(pids):
        filenames = []
        for indx, atlas_subfolder in enumerate(atlas_subfolders):
            if indx >= number_of_atlas: 
                print('Using %d atlases' % indx)
                break;
            filename = '/'.join([pid, atlas_subfolder, deformed_layer_pnt_filename])
            filename = os.path.join(main_folder, filename)
            filenames.append(filename)
        print('Using %d atlases' % len(filenames))

        labeled_points = get_atlas_layer_points(filenames, shuffle)
        #if shuffle: labeled_points = shuffle_points(labeled_points)
            
        deformed_layer_shuffle_points4pids[pid] = labeled_points
        
    return deformed_layer_shuffle_points4pids