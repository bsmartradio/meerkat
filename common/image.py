from common.channel import Channel
import common.data_helper as helper

class Image:
    all_cube_channels = []
    vot_table = None

    def init_channel(self, path):
        files = helper.get_files(path)
        
        for file in files:
            self.all_cube_channels.append(self.create_channel(file))
        
        self.vot_table = helper.get_vot(name)

    @staticmethod
    def create_channel(file):
        return Channel(file, channel_number)
