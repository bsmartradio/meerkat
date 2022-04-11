from astropy.wcs import WCS

from common.channel import Channel
import common.data_helper as helper


class Image:
    channels = []
    vot_table = None
    folder_name = None
    vot_location = None
    positions = None

    def __init__(self, path):
        files = helper.find_files(path)

        self.channels= self.create_cube(files)
        self.folder_name = helper.get_name(path)
        self.vot_location = helper.get_vot_location(path)
        self.vot_table = helper.read_info(self.vot_location + self.folder_name +
                                          '_Mosaic_Mom0_comp.vot')
        w = WCS(self.channels[1].header, naxis=2)
        self.positions = helper.unify_coords(self.vot_table, w)

    @staticmethod
    def create_cube(files):
        cube = []
        for file in files:
            cube.append(Channel(file))
        return cube
