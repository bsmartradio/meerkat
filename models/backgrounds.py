import common.data_helper as helper


class Backgrounds:
    header = None
    data = None
    name = None

    def __init__(self, path):
        self.data, self.header = helper.get_image(path)
        self.name = path
