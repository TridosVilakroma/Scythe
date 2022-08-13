import sys,pickle
from os import path

def save(data,slot):
    with open(rf'save_data\file{slot}_data', 'wb') as write_file:
        pickle.dump(data, write_file)

def load(slot):
        if path.exists(rf'save_data\file{slot}_data'):
            with open(rf'save_data\file{slot}_data', 'rb') as read_file:
                data = pickle.load(read_file)
            return data