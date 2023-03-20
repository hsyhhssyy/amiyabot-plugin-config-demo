# Core

class PluginInstance():
    def __init__(self,name:str,**kwargs):
        self.name = name

# AmiyaBot 目前没东西

class PluginTool():
    def __init__(self,config:str,**kwargs):
        self.config = config

# 插件里

class MyPlugin(PluginInstance,PluginTool):
    ...

bot = MyPlugin(
    name='1234',
    config='456' 
)