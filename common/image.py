from common.channel import Channel
import common.data_helper as helper


class Image:
    all_cube_channels = []
    vot_table = None
    folder_name = None

    def __init__(self, path):
        files = helper.find_files(path)

        self.all_cube_channels= self.create_cube(files)
        self.folder_name = helper.get_name(path)
        upper_folder = path[0:-len(self.folder_name)-2].rfind("/")
        self.vot_table = helper.read_info(path[0:upper_folder] + '/Mom0_comp_catalogs/' + self.folder_name + '_Mosaic_Mom0_comp.vot')

    @staticmethod
    def create_cube(files):
        cube = []
        for file in files:
            cube.append(Channel(file))
        return cube
