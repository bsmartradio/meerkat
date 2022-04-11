import common.data_helper as helper
import numpy as np

class Channel:
    name = None
    header = None
    image_data = None
    frequency = None
    channel_number = None
    channel_photometry = None
    photometry_errors = None

    def __init__(self, path):
        self.name = path
        self.image_data, self.header = helper.get_image(path)
        self.frequency = self.get_frequency(self.header)
        self.channel_photometry = self.image_data*np.nan
        self.photometry_error = self.image_data * np.nan

    @staticmethod
    def get_frequency(header):
        frequency = header['OBSFREQ']
        return frequency
