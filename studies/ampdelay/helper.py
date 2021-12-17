import h5py
import numpy
import os
from matplotlib import pyplot

def get_file_comment(dir):
    # input: string
    # output: list of [filename string, comment string]
    
    files = os.listdir(dir)
    files.sort()
    file_comment = []

    for f in files:
        h5file = h5py.File(dir + f, 'r')
        comment = h5file['attrs'].attrs['comment']
        # One data point is broken. I'm lazy, fix it.
        if comment[-4:] == '8 kV':
            file_comment.append([dir + f, 2.48])
        else:
            file_comment.append([dir + f, float(comment[-4:])])
            
    return file_comment