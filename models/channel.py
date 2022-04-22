import common.data_helper as helper
import numpy as np
import logging


class Channel:
    path = None
    header = None
    data = None
    frequency = None
    channel_number = None
    channel_photometry = None
    photometry_errors = None

    def __init__(self, path):
        self.path = path
        self.data, self.header = helper.get_image(path)
        self.frequency = self.get_frequency(self.header)
        self.channel_photometry = self.data * np.nan
        self.photometry_error = self.data * np.nan

    @staticmethod
    def get_frequency(header):
        try:
            frequency = header['OBSFREQ']
            return frequency

        except KeyError as ke:
            logging.warning(msg='Channel has no frequency value', exc_info=ke)
