import data_helper as helper

class Channel:
    name = None
    hdul = None
    image_data = None
    frequency = None
    channel_number = None
    channel_photometry = None

    def __init__(self, path, channel_number):
        self.name = helper.get_name(path)
        self.channel_number = channel_number
        self.image_data, self.hdul = helper.get_image(path)
        self.frequency = self.get_frequency(self.hdul)

    @staticmethod
    def get_frequency(hdul):
        frequency = hdul['OBSFREQ']
        return frequency
