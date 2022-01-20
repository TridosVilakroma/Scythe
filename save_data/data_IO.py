import sys,pickle
from os import path

def save(data,slot):
    pickle_out = open(rf'save_data\file{slot}_data', 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()

def load(slot):
        if path.exists(rf'save_data\file{slot}_data'):
            pickle_in = open(rf'save_data\file{slot}_data', 'rb')
            data = pickle.load(pickle_in)
            pickle_in.close()
            return data