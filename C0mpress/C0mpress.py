from HaffManCore import HuffmanTree
from DataExtract import DataExtractor
from FileStruct import C0mpressFile
from TableStruct import Table
from time import time
from hashlib import sha256
from binascii import unhexlify,hexlify,crc32
import rc4
import logging

class C0mpress(object):
    def __init__(self,filename=None,key=None):
        self._filename = filename
        self._error = 0
        self.size = 0
        self.pressedDataInList = None
        self.pressedDataInText = ""
        self.dataPressed = False
        self.targetFile = None
        self.key = key
        self._table_offset = 0x40
        self.keysPackInFile = ""
        self.valsPackInFile = []
        if None != self._filename:
            tmp = DataExtractor(filename)
            self._data = tmp.getData()
            tmp = HuffmanTree(tmp.weightDict)
            tmp.get_code()
            self.hftree = tmp.l
        else:
            self.hftree = {}
            self._error = 1
            self._data = None
    def PackWithPad(self):
        self.pressedDataInList += [0]*(8-self.size%8)
        tmpl = len(self.pressedDataInList)
        for i in range(int(tmpl / 8)):
            self.pressedDataInText += chr(int("".join([str(self.pressedDataInList[8*i+j]) for j in range(8)]),2))
        #self.pressedDataInText.join([chr(int("".join([str(self.pressedDataInList[8*i+j]) for j in range(8)]),2)) for i in range(int(tmpl/8))])
        #print(self.pressedDataInText)
        self.dataPressed = True
    def PackInFile(self):
        tmp = C0mpressFile(self.key)
        tmp._magic = b"C0sk"
        tmp._size = self.size
        tmp._isEnced = 1 if self.key!=b"" else 0
        tmp._time_stamp = int(time())
        tmp._sha256_check = unhexlify(sha256(self.pressedDataInText.encode()).hexdigest())
        if tmp._isEnced == 1:
            tmp._crc_check = crc32(self.pressedDataInText.encode("latin-1"))
            tmptext = rc4.rc4(self.pressedDataInText,self.key.decode("latin-1"))
            self.pressedDataInText = tmptext
        tmp._table_offset = 0x40 + len(self.pressedDataInText)
        table_tmp = Table(self.hftree)
        tmp._table_keys_size = table_tmp.table_size_1
        tmp._table_vals_size = table_tmp.table_size_2
        self.keysPackInFile = table_tmp.keys
        self.valsPackInFile = table_tmp.vals
        return tmp
    def packData(self):
        fdata = str(self.PackInFile()).encode("latin-1")
        fdata += self.pressedDataInText.encode("latin-1")
        fdata += self.keysPackInFile.encode("latin-1")
        tmpl = len(self.valsPackInFile)
        self.valsPackInFile += [0] * (8 - tmpl % 8)
        tmpl = len(self.valsPackInFile)
        ftmpdata = ""
        for i in range(int(tmpl/8)):
             ftmpdata += chr(int("".join([str(self.valsPackInFile[8*i+j]) for j in range(8)]),2))
        fdata += ftmpdata.encode("latin-1")
        return fdata
    def do(self):
        try:
            error = self._error
            data = self._data
            if error==0 and data!=None:
                zfilename = self._filename+".c0p"
                tmpf = open(zfilename,"wb")
                tmpd = []
                for i in data:
                   tmpd+=self.hftree[i]
                #tmpd = [self.hftree[i] for i in data]
                self.size = len(tmpd)
                self.pressedDataInList = tmpd
                self.PackWithPad()
                tmpf.write(self.packData())
                tmpf.close()
                self.targetFile = tmpf
                logging.info("pressed file %s generated"%self.targetFile.name)
                return
            else:
                logging.warning("EMPTY DATA")
                return
        except Exception:
            logging.error("bad use with %s"%(str(Exception)))
            exit()

'''
x = C0mpress("test","12345678")
#print(x.hftree)
x.do()
print(x.hftree)
print(x.pressedDataInList)
#print(x.pressedDataInText)
print(x.key)
print(hexlify(x.keysPackInFile.encode("latin-1")))
print(x.valsPackInFile)
'''
