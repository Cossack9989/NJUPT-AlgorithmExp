import struct
import rc4

class D3c0mpress(object):
    def __init__(self,filename = None,key=None):
        self._filename = filename
        self._error = 0
        self.key = key
        self.size = 0
        self.RAW = None
        self.plainData = None
        self.hftree = {}
        self.plainDataEx = []
        self.decodeData = b""
        self.decodeFile = None
        if None != self._filename:
            self.parseC0p()
    def getContent(self):
        tmpf = open(self._filename,"rb")
        tmpfdata = tmpf.read()
        tmpf.close()
        return tmpfdata
    def getTblOffset(self):
        return struct.unpack("<I",self.RAW[0x34:0x38])[0]
    def getTblKeyLen(self):
        return struct.unpack("<I",self.RAW[0x38:0x3c])[0]
    def getTblValLen(self):
        return struct.unpack("<I",self.RAW[0x3c:0x40])[0]
    def getIntFromBytes(self,tmpbytes):
        return struct.unpack("<I",tmpbytes)[0]
    def getTblSize(self):
        tmpvallen = self.getTblValLen()
        tmpvallen = int(tmpvallen/8) if (tmpvallen%8==0) else (int(tmpvallen/8)+1)
        return self.getTblKeyLen()+tmpvallen
    def getDataLen(self):
        return self.getTblOffset()-0x40
    def getDataExLen(self):
        return struct.unpack("<I",self.RAW[0x4:0x8])[0]
    def parseTbl(self):
        tmpTbl = self.RAW[self.getTblOffset():self.getTblOffset()+self.getTblSize()]
        tmpKeys = tmpTbl[:self.getTblKeyLen()]
        tmpVals = tmpTbl[self.getTblKeyLen():]
        tmpValsInBits = []
        for i in tmpVals:
            tmpValsInBits += [int(j) for j in bin(i).replace('0b','').rjust(8,'0')]
        sum = 0
        for i in range(int(len(tmpKeys)/2)):
            tmpadd = tmpKeys[2*i+1]
            self.hftree[chr(tmpKeys[2*i])] = tmpValsInBits[sum:sum+tmpadd]
            sum += tmpadd
        return sum
    def parseData(self):
        for i in self.plainData:
            self.plainDataEx += [int(j) for j in bin(i).replace('0b','').rjust(8,'0')]
        self.plainDataEx = self.plainDataEx[:self.getDataExLen()]
    def parseC0p(self):
        self.RAW = self.getContent()
        originLen = self.getDataLen()
        self.parseTbl()
        if b"" != self.key:
            encedData = self.RAW[0x40:0x40+originLen]
            self.plainData = rc4.rc4(encedData.decode("latin-1"),self.key.decode("latin-1")).encode("latin-1")
        else:
            self.plainData = self.RAW[0x40:0x40+originLen]
        self.parseData()

    def undo(self):
        while(True):
            for key in self.hftree:
                if self.plainDataEx[:len(self.hftree[key])] == (self.hftree[key]):
                    self.plainDataEx = self.plainDataEx[len(self.hftree[key]):]
                    self.decodeData += key.encode("latin-1")
                    break
            if not self.plainDataEx:
                break
        tmpf = open(self._filename+".D3c","wb")
        tmpf.write(self.decodeData)
        self.decodeFile = tmpf.name
        tmpf.close()

'''
x = D3c0mpress("ztest.c0p","12345678")
x.undo()
'''
