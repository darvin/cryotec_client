# -*- coding: UTF-8 -*-


'''
@author: darvin
'''

from qtdjango.modelsmanager import ModelsManager
#ADDRESS = "http://94.244.162.162:8000"
#ADDRESS = "http://172.16.170.1:8000"

from settings import get_settings, error_settings
#try:
models = ModelsManager(get_settings("address"), \
                   get_settings("api_path"), \
                   get_settings("server_package"), \
                          ["machines","actions","actiontemplates","clients","checklists"],
                          ("Action", "PAction",))
#except ImportError:
#    error_settings("server_package")
#except:
#    error_settings("address")


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
