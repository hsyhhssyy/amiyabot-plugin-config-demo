# Core

class PluginInstance():
    def __init__(self,name:str):
        self.name = name

# AmiyaBot 

class AmiyaBotPluginInstance(PluginInstance):
    def __init__(self,name:str,config:str):
        self.name = name
        # 进行一定的处理
        self.real_config = config 

# 插件里

class MyPlugin(AmiyaBotPluginInstance):
    def install(self):
        pass

bot = MyPlugin(
    name='1234',
    config = '456'
)