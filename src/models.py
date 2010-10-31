# -*- coding: UTF-8 -*-


'''
@author: darvin
'''

from qtdjango.modelsmanager import ModelsManager

from settings import get_settings
models = ModelsManager(get_settings("address"), \
                   get_settings("api_path"), \
                   get_settings("server_package"), \
                          ["machines","actions","actiontemplates","clients","checklists"],
                          ("Action", "PAction",),\
                login=get_settings("login"),\
                password=get_settings("password"),)

