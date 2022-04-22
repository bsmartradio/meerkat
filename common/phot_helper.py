import glob
import numpy as np


def load_phot_table(channel_name):
    return np.load(channel_name, allow_pickle=True)


def get_chan_list(location):
    return glob.glob(location + "phot_table*.npy")