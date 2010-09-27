'''
    
    @author: darvin
'''
class Field(object):
    
    widget = None
    
    def __init__(self, *args, **kwargs):
        try:
            self.verbose_name = args[0]
        except IndexError:
            pass

    def load(self, data):
        return data
    
    def dump(self, data):
        return data
    
    def blank(self):
        return None
    
    def get_label(self):
        try:
            return self.verbose_name
        except AttributeError:
            return "verbose name not defined"


class IdField(Field):
    def load(self, data):
        return int(data)

class TextField(Field):
    pass

class CharField(Field):
    pass

class IntField(Field):
    def load(self, data):
        return int(data)
    
    def dump(self, data):
        return int(data)

class ForeignKey(Field):
    
    def load(self, data):
        return self.model.get(data["id"])
    
    def dump(self, data):
        return unicode(data)
    
    def __init__(self, *args, **kwargs):
        super(ForeignKey, self).__init__( *args, **kwargs)
        self.model = kwargs["model"]
        self.model.load()
        
        
#        self.model.__setattr__("foreing_key_model_"+kwargs["self"].__name__, kwargs["self"])






from connection import Connection
    

class Model(object):
    '''
    classdocs
    '''
    resource_name = "resource_name"
    loaded = False
    fields = {}

    objects = []

    @classmethod
    def load(cls):
        if not cls.loaded:
            cls.fields["id"] = IdField("Id")
            raw = Connection.get(cls.resource_name)
            cls.objects = [cls(**x) for x in raw]
            cls.loaded = True

    
    @classmethod
    def dump(cls):
        raise NonImplementedError
    
    @classmethod    
    def all(cls):
        return cls.filter()
    
    @classmethod    
    def new(cls, **kwargs):
        return cls(**kwargs)
    
    @classmethod
    def filter(cls, **kwargs):
        return [x for x in cls.objects if x.is_filtered(**kwargs)]
                                                        
    
    @classmethod
    def get(cls, id):
        res = cls.filter(id=id)
        if len(res)==1:
            return res[0]
            
#    def foreign_set(self, setname):
#        try:
#            fclass = "foreing_key_model_"+setname
#        except KeyError:
#            print setname
#            print globals()
#            pass 
#        return fclass.filter(\
#                    **{self.__class__.__name__.lower():self})
#    
    def __setattr__(self, name, value):
        try:
            if name in object.__getattribute__(self, "_data"):
                self._data[ name]= value
        except AttributeError:
            object.__setattr__(self, name, value)
    
    def __getattribute__(self, name):
        
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
#            if "_set" in name:
#                return self.foreign_set(name.replace("_set",""))
#            else:
            return self._data[name]
    
    def is_filtered(self, **kwargs):
        for field in kwargs:
            try:
                if self._data[field]!=kwargs[field]:
                    return False
            except KeyError:
                if "__" in field:
                    keymodel, keyfield = field.split("__")
                    if self._data[keymodel]._data[keyfield]!=kwargs[field]:
                        return False
                else:
                    print field
                    raise KeyError
        return True
    
    def __init__(self, **initdict):
        super(Model,self).__init__()
        self._data={}
        for field in self.fields:
            try:
                self._data[field]=self.fields[field].load(initdict[field])
            except KeyError:
                self._data[field]=self.fields[field].blank()
     
     
    def validate(self):
        pass
    
    def save(self):
        self.validate()
        
        dubl = self.get(self.id)
        
        if dubl is None:
            self.objects.append(self)
        self.undumped = True
    
    def __unicode__(self):
        return self._data
    
    
if __name__=="__main__":
    
    
    pass