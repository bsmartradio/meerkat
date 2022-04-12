from astropy.wcs import WCS

from common.channel import Channel
import common.data_helper as helper
from common.backgrounds import Backgrounds


class Image:
    channels = []
    background = []
    rms = []
    vot_table = None
    folder_name = None
    vot_location = None
    positions = None
    location = None

    def __init__(self, path):
        files = helper.find_files(path)
        background_files = helper.find_backgrounds(path, background=True)
        rms_files = helper.find_backgrounds(path, rms=True)

        self.location = path
        self.channels= self.get_channels(files)
        self.folder_name = helper.get_name(path)
        self.vot_location = helper.get_vot_location(path)
        self.vot_table = helper.read_info(self.vot_location + self.folder_name +
                                          '_Mosaic_Mom0_comp.vot')
        w = WCS(self.channels[1].header, naxis=2)
        self.positions = helper.unify_coords(self.vot_table, w)
        self.background = self.get_backgrounds(background_files)
        self.rms = self.get_backgrounds(rms_files)

    def get_channels(self,files):
        cube = []
        for file in files:
            cube.append(Channel(file))
        return cube

    def get_backgrounds(self,files):
        cube_backgrounds = []
        for file in files:
            cube_backgrounds.append(Backgrounds(file))
        return cube_backgrounds
