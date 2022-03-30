from lib.MyDebug import Dprint as dprint
from lib import MyFile

class MyData:
    def __init__(self, filename = "", type = ""):
        self.filename = filename
        if len(filename) > 0:
            self.dfile = MyFile.MyFile(filename)
            if len(type) == 0:
                self.dfile.set_type("json")
            else:
                self.dfile.set_type(type)

    def __del__(self):
        pass

    def add_data(self, param, parm2=None):
        pass

    def del_data(self, param, parm2=None):
        pass

    def get_data_len(self):
        pass

    def save_data(self):
        if self.dfile is not None:
            self.dfile.write(self.ldata)

    def load_data(self):
        if self.dfile is not None:
            return self.dfile.read()


class MyDict(MyData):
    def __init__(self, filename = "", type = ""):
        super(MyDict, self).__init__(filename, type)
        self.dic_data = {}

    def __del__(self):
        super(MyDict, self).__del__()
        self.dic_data.clear()

    def add_data(self, key, value):
        if key is None or value is None:
            return
        self.dic_data[key] = value

    def del_data(self, key, value):
        if key is None:
            return
        if value is None:
            self.dic_data[key].clear()
        else:
            self.dic_data[key].remove(value)

    def copy_data(self, data):
        self.dic_data = data
        return self.dic_data

    def get_data(self):
        return self.dic_data

    def get_data_len(self):
        return len(self.dic_data)

    def save_data(self):
        if self.dfile is not None:
            self.dfile.write(self.dic_data)

    def load_data(self):
        if self.dfile is not None and self.dfile.exist():
            self.dic_data.clear()
            self.dic_data.update(self.dfile.read())
            return 1

        return 0


class MyList(MyData):
    def __init__(self, filename ="", type = ""):
        super(MyList, self).__init__(filename, type)
        self.list_data = []

    def __del__(self):
        super(MyList, self).__del__()
        self.list_data.clear()

    def add_data(self, value):
        if value is None:
            return

        self.ldata.append(value)

    def del_data(self, value):
        if len(self.ldata) != 0:
            self.ldata.remove(value)

    def del_data_index(self, index):
        if index < len(self.ldata):
            del self.ldata[index]

    def get_data(self):
        return self.ldata

    def get_data_len(self):
        return len(self.ldata)

    def save_data(self):
        super(MyList, self).save_data()

    def load_data(self):
        self.ldata = super(MyList, self).load_data()
