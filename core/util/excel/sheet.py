class Sheet:
    def __init__(self, name, row, columns=[]):
        self.name = name
        self.row = row
        self.columns = columns
        self.rows = []
        self.data = []
