from astropy.wcs import WCS
import common.vot_helper
from models.channel import Channel
import common.data_helper as helper
from models.backgrounds import Backgrounds


class Image:
    channels = []
    background = []
    rms = []
    vot_table = None
    folder_name = None
    vot_location = None
    positions = None
    location = None

    def __init__(self, path, single_channel=None):

        files = helper.find_channels(path)
        background_files = helper.find_backgrounds(path, background=True)
        rms_files = helper.find_backgrounds(path, rms=True)

        self.location = path
        self.folder_name = helper.get_name(path)
        self.vot_location = common.vot_helper.get_vot_location(path)
        self.vot_table = common.vot_helper.read_vot(self.vot_location + self.folder_name + '_Mosaic_Mom0_comp.vot')

        if not single_channel:
            self.channels = self.get_channels(files)
            self.background = self.get_backgrounds(background_files)
            self.rms = self.get_backgrounds(rms_files)

        if single_channel:
            self.channels = self.get_channels(files[single_channel])
            self.background = self.get_backgrounds(background_files[single_channel])
            self.rms = self.get_backgrounds(rms_files[single_channel])

        w = WCS(self.channels[0].header, naxis=2)
        self.positions = helper.unify_coords(self.vot_table, w)

    @staticmethod
    def get_channels(files):
        cube = []

        if type(files) is list:

            for file in files:
                cube.append(Channel(file))

        if type(files) is str:
            cube.append(Channel(files))

        return cube

    @staticmethod
    def get_backgrounds(files):
        cube_backgrounds = []

        if type(files) is list:

            for file in files:
                cube_backgrounds.append(Backgrounds(file))

        if type(files) is str:
            cube_backgrounds.append(Backgrounds(files))

        return cube_backgrounds
