import logging
import struct

C0mpressHeadStruct_size = {
	'normal':0x34,
	'security':0x34
}

C0mpressHeadStruct = {
    'normal': {
        0x0: '_magic',
        0x4: '_size',
        0x8: '_isEnced',
        0xc: '_time_stamp',
        0x10: '_sha256_check',
        0x30: '_reserved',
        0x34: '_table_offset',
        0x38: '_table_keys_size',
        0x3c: '_table_vals_size'
    },

    'security': {
        0x0: '_magic',
        0x4: '_size',
        0x8: '_isEnced',
        0xc: '_time_stamp',
        0x10: '_sha256_check',
        0x30: '_crc_check',
        0x34: '_table_offset',
        0x38: '_table_keys_size',
        0x3c: '_table_vals_size'
    }
}


class C0mpressFile(dict):
    mode = None
    size = 0
    FILE_struct = []

    def __init__(self,key=None):
        self.mode = "security" if None != key else "normal"
        self.FILE_struct = [C0mpressHeadStruct[self.mode][i] for i in sorted(C0mpressHeadStruct[self.mode].keys())]
        self.update({r: 0 for r in self.FILE_struct})
        self.size = C0mpressHeadStruct_size[self.mode]

    def __setitem__(self, item, value):
        if item not in self.FILE_struct:
            logging.error("Unknown item %r (not in %r)" % (item, self.FILE_struct))
        super(C0mpressFile, self).__setitem__(item, value)

    def __setattr__(self, attr, value):
        if attr in C0mpressFile.__dict__:
            super(C0mpressFile, self).__setattr__(attr, value)
        else:
            self[attr] = value

    def __getattr__(self, attr):
        return self[attr]

    def __str__(self):
        fake_file = b""
        for item_offset in sorted(self.item_offset):
            if len(fake_file) < item_offset:
                fake_file += "\x00" * (item_offset - len(fake_file))
            #fake_file += self.unhexlify_s(str(self[C0mpressHeadStruct[self.mode][item_offset]]))
            fake_file += self.pack(item_offset)
        fake_file += b"\x00" * (self.size - len(fake_file))
        return fake_file.decode("latin-1")

    @property
    def item_offset(self):
        return C0mpressHeadStruct[self.mode].keys()
    def pack(self,item_offset):
        if type(self[C0mpressHeadStruct[self.mode][item_offset]]) is int:
            return struct.pack("<I",self[C0mpressHeadStruct[self.mode][item_offset]])
        elif type(self[C0mpressHeadStruct[self.mode][item_offset]]) is bytes:
            return self[C0mpressHeadStruct[self.mode][item_offset]]
        else:
            return '\0'
