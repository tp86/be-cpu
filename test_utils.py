class Probe:
    def __init__(self):
        self.results = []
        self.error = None

    def on_next(self, elem):
        self.results.append(elem)

    def on_error(self, error):
        self.error = error

    def on_completed(self):
        pass
