import common.data_helper as helper


class Rms:
    header = None
    data = None

    def __init__(self, path):
        self.data, self.header = helper.get_image(path)
