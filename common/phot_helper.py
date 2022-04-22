import glob
import numpy as np


def load_phot_table(channel_name):
    phot_table = np.load(channel_name, allow_pickle=True)
    return phot_table


def get_chan_list(location):
    channel_list = glob.glob(location + "phot_table*.npy")
    return channel_list