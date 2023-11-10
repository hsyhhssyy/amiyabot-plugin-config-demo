import asyncio
import json
import os
import re
import threading
import traceback

from amiyabot import Message, Chain, log
from amiyabot.network.httpServer import BaseModel

from core import bot as main_bot
from core import app,Requirement
from core.util import read_yaml
from core import AmiyaBotPluginInstance

curr_dir = os.path.dirname(__file__)

# 你可以考虑将路径加入allow_path来禁用对token的校验
app.set_allow_path(['/maa/token'])

@app.controller
class PluginConfigDemoServer:
    # 构造一个服务，用来提供网页，他的路径要写到插件的构造参数中。
    @app.route(method='get')
    async def page(self):
        return app.response()

class PluginConfigDemoPluginInstance(AmiyaBotPluginInstance):
    def install(self):
        # 下面这段代码，可以将低版本的配置文件拷贝到新版本配置系统中来，并删除旧配置文件。
        # 可以用于向下兼容
        config_file = 'resource/plugins/plugin_config_demo/old_config.yaml'
        if os.path.exists(config_file):
            yaml_config = read_yaml(config_file, _dict=True)
            for key in object.keys(yaml_config):
                self.set_config(key, yaml_config[key], None)

            os.remove(config_file)
        
        # 对于动态配置，建议不要在动态配置项执行时查询，除非你可以非常快速的查询出结果
        # 我们推荐你提前查询出结果，然后缓存起来，这样可以避免影响到Console的打开和其他插件的加载。

        # 如果你有一定程度的实时需求，你可以仿照下面这段代码，使用一个线程来定时查询
        def wrapper():

            loop = asyncio.new_event_loop()        
            asyncio.set_event_loop(loop)

            # 多层warper嵌套的目的是为了异步转同步。python的async，你懂的。
            async def async_wrapper():
                while True:
                    blm_lib = main_bot.plugins['amiyabot-blm-library']
                    
                    if blm_lib is not None:
                        model_list = await blm_lib.model_list()
                        model_name_list = [model['model_name'] for model in model_list]
                        self.model_name_list = model_name_list
                        
                    threading.Event().wait(600)  # 等待60秒

            loop.run_until_complete(async_wrapper())
            loop.close()

        threading.Thread(target=wrapper).start()
        

    def generate_schema(self):

        # 请记住一定要给一个完整的结构，你可以从文件中加载一个范本来方便自己构造这个结构。

        filepath = f'{curr_dir}/global_config_schema.json'

        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            log.info(f"Failed to load JSON from {filepath}.")
            return None
        
        # 从缓存中读取配置项而不是直接现场查询
        if hasattr(self, 'model_name_list') and self.model_name_list is not None:
            try:          
                log.info(f"Updating dynamic option: {self.model_name_list}")              
                data["properties"]["dynamic_option"]["enum"] = self.model_name_list
            except KeyError as e:
                stack_trace = traceback.format_exc()
                log.info(f"Expected keys not found in the JSON structure: {e}\n{stack_trace}")
        
        # 返回修改后的Schema

        return data

bot : PluginConfigDemoPluginInstance = None

def dynamic_get_global_config_schema_data():
    # 如果你需要调用一个bot的实例方法，这里要判断bot是否已经构造完毕。
    # 因为兔兔第一次尝试获取Schema时，正是在bot的构造函数中。
    # 此时bot还没有构造完毕，这时候调用bot的方法会出错。
    if bot:
        return bot.generate_schema()
    else:
        return f'{curr_dir}/global_config_default.json'

bot = PluginConfigDemoPluginInstance(
    name='插件配置项Demo',
    version='1.6',
    plugin_id='amiyabot-plugin-config-demo',
    plugin_type='',
    description='帮助开发者了解如何与Console的配置页面对接',
    document=f'{curr_dir}/README.md',
    requirements=[
        Requirement("amiyabot-blm-library")
    ],
    channel_config_default=f'{curr_dir}/channel_config_default.json',
    # 您可以选择不提供Schema, 系统会自动根据您给出的默认配置文件来猜测并提供一个编辑器
    channel_config_schema=f'{curr_dir}/channel_config_schema.json', 
    global_config_default=f'{curr_dir}/global_config_default.json',
    # 您可以选择不提供Schema, 系统会自动根据您给出的默认配置文件来猜测并提供一个编辑器
    # 或者您也可以提供一个function，让Console可以动态加载一个配置项的Schema
    global_config_schema=dynamic_get_global_config_schema_data, 

)

@bot.on_message(keywords=['写入全局配置'], level=5)
async def save_global_config(data: Message):
    match = re.search(r"写入全局配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        bot.set_config(key, value)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')


@bot.on_message(keywords=['写入配置'], level=5)
async def save_channel_config(data: Message):
    match = re.search(r"写入配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        bot.set_config(key, value, data.channel_id)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')


@bot.on_message(keywords=['读取配置'], level=5)
async def check_config(data: Message):
    index = data.text.find('读取配置')
    if index != -1:
        result_str = data.text[index + len('读取配置'):]
        return Chain(data).text(f'{bot.get_config(result_str, data.channel_id)}')
    else:
        return Chain(data).text('未找到指定的字串')