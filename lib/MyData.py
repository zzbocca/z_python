from lib.MyDebug import Dprint as dprint
from lib import MyFile
from deepdiff import DeepDiff
from copy import deepcopy
import collections

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
    def __init__(self, filename = "", type = "", data = None):
        super(MyDict, self).__init__(filename, type)
        if data is not None:
            self.dic_data = deepcopy(data)
        else:
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

    def clear_data(self):
        self.dic_data.clear()

    def copy_data(self, data):
        self.dic_data = data
        return self.dic_data

    def get_data(self):
        return self.dic_data

    def get_data_len(self):
        return len(self.dic_data)

    def deep_update(self, overrides, source=None):
        """
        Update a nested dictionary or similar mapping.
        Modify ``source`` in place.
        """
        if source is None:
            source = self.dic_data
        for key, value in overrides.items():
            if isinstance(value, collections.Mapping) and value:
                returned = self.deep_update(value, source.get(key, {}))
                source[key] = returned
            else:
                if isinstance(value, list) and value:
                    source[key] = overrides[key].copy()
                else:
                    source[key] = overrides[key]
        return source

    def save_data(self, set_data=None, save=True):
        if set_data is not None:
            diff = DeepDiff(set_data, self.dic_data)
            if len(diff) == 0:
                return 0
            else:
                self.deep_update(set_data)
        dprint(self.dic_data, 4)
        if self.dfile is not None and save==True:
            self.dfile.write(self.dic_data)

        return 1

    def get_diff_data(self, set_data):
        if set_data is None:
            return None
        diff = DeepDiff(self.dic_data, set_data)
        return diff

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

        self.list_data.append(value)

    def del_data(self, value):
        if len(self.list_data) != 0:
            self.list_data.remove(value)

    def clear_data(self):
        self.list_data.clear()

    def del_data_index(self, index):
        if index < len(self.list_data):
            del self.list_data[index]

    def get_data(self):
        return self.list_data

    def get_data_len(self):
        return len(self.list_data)

    def save_data(self):
        super(MyList, self).save_data()

    def load_data(self):
        self.list_data = super(MyList, self).load_data()
