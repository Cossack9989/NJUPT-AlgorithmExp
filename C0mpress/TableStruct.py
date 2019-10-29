class Table(object):
    def __init__(self,idict):
        self.tree = idict
        self.keys = ""
        self.vals = []
        for key in idict:
            self.keys+=key
            self.keys+=chr(len(idict[key]))
            self.vals+=idict[key]
        self.table_size_1 = len(self.keys)
        self.table_size_2 = len(self.vals)