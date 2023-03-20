# Core

class PluginInstance():
    def __init__(self,name:str):
        self.name = name

class PluginTool():
    def __init__(self,config:str):
        self.config = config

# AmiyaBot 目前没东西


# 插件里

class MyPlugin(PluginInstance,PluginTool):
    ...

bot = MyPlugin(
    name='1234'
    #,config='456' 加这个会报错
)

bot.config='456'