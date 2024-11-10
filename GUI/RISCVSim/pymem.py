from collections import OrderedDict

def PyMem_Iter(_mdata):
        _addr  = 0x00000000
        _max_addr = list(_mdata.keys())[-1]
        while True:
            if _addr > _max_addr:
                return
            else:
                v = _addr
                _addr += 1
                yield v

class PyMEM:
    FORMAT_VLOG_B8 = 1
    SIZE = 16384

    def __init__(self,file_or_fileobj,FORMAT=None):
        obj_close_flag = type(file_or_fileobj) == type("")
        if obj_close_flag:
            file_or_fileobj = open(file_or_fileobj,"r")
        self._mdata = OrderedDict()   
        if FORMAT is None:
            self.__read_vlog_b8(self._mdata, file_or_fileobj)
            self.__fill()
        if obj_close_flag:
            file_or_fileobj.close()
                
    def __read_vlog_b8(self,mdata,fileobj):
        addr = 0x00000000
        for line in fileobj:
            segs = line.strip().split(' ')
            for seg in segs:
                if seg == '':
                    continue
                if seg.startswith('@'):
                    addr = int(seg[2:],base=16)
                else:
                    data = int(seg,base=16)
                    mdata[addr] = data
                    addr += 1
    def __fill(self):
        current_size = len(self._mdata)
        if current_size < self.SIZE:
            for addr in range(current_size, self.SIZE):
                self._mdata[addr] = 0  # Fill missing addresses with 0
    def __getitem__(self,addr):
        return self._mdata[addr]
    def __setitem__(self,addr,data):
        self._mdata[addr] = data
    def keys(self):
        return PyMem_Iter(self._mdata)
                    
if __name__ == '__main__':
    import sys
    o = PyMEM("./test2.v")
    print(o._mdata)
    for a in o.keys():
        print(a,o[a])
