easy_install --upgrade qtdjango
easy_install --upgrade cryotec_server
python setup.py py2exe --includes sip,cryotec_server.machines.models,cryotec_server.actions.models,cryotec_server.actiontemplates.models,cryotec_server.clients.models,cryotec_server.checklists.models
