import collections

class DataExtractor(object):
    def __init__(self,filename=None,isUsed = False):
        self._filename = filename
        self._isUsed = isUsed
        self.weightDict = []
    def getWeight(self,origin):
        statistic = collections.Counter(origin)
        collector = statistic.most_common()
        return collector
    def getData(self):
        try:
            f = open(self._filename,"rb")
            origin = f.read()
            f.close()
            tmp = self.getWeight(origin)
            for i in tmp:
                self.weightDict.append((chr(i[0]),i[1]))
            return origin.decode()
        except Exception:
            return None

'''
x = DataExtractor("test")
x.getData()
print(x.weightDict)
'''

