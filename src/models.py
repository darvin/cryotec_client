# -*- coding: UTF-8 -*-


'''
@author: darvin
'''

from qtdjango.modelsmanager import ModelsManager

#ADDRESS = "http://94.244.162.162:8000"
ADDRESS = "http://172.16.170.1:8000"

API_PATH= "/api/"
models = ModelsManager(ADDRESS, API_PATH, "cryotec_server", \
                              ["machines","actions","actiontemplates","clients","checklists"],
                              ("Action", "PAction",))

#current_module =__import__(__name__)
#mm.do_models_magic_with_module(current_module)

if __name__ == '__main__':
#    print Machine.all()
#    m1 = Machine.new()
#    m1.save()
#    m2 = Machine.new()
#    m2.save()
#
#    from pprint import pprint
#    for m in Machine.all():
#        pprint (m.__dict__)
    pass
