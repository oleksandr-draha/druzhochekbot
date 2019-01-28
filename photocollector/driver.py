class PhotoCollector(object):
    def __init__(self):
        self.start_offset = 0
        self.session = session()
        self.get_updates()