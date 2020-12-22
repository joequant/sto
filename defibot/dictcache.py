import shelve
import os
import datetime

class DictCache:
    def __init__(self, name):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.s = shelve.open(os.path.join(script_dir, "asset",
                                          '{}.db'.format(name)),
                             writeback=True)
        self.expires = 3600
        self.s['_timestamp'] = {}
    def __getitem__(self, key):
        if self.expired(key):
            del(self.s[key])
            del(self.s['_timestamp'][key])
            throw(KeyError)
        else:
            return self.s[key]
    def __setitem__(self, key, value):
        self.s['_timestamp'][key] = self.utcnow()
        self.s[key] = value
    def __contains__(self, k):
        return False if k not in self.s else \
            not self.expired(k)
    def __del__(self):
        self.s.close()
    def utcnow(self):
        return datetime.datetime.utcnow().timestamp()
    def expired(self, k):
        return k in self.s['_timestamp'] and \
            self.utcnow() >= self.s['_timestamp'][k] + self.expires
