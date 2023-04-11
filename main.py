import os
import re

from amiyabot import Message, Chain
from core.util import read_yaml
from core.customPluginInstance import AmiyaBotPluginInstance

curr_dir = os.path.dirname(__file__)

class PluginConfigDemoPluginInstance(AmiyaBotPluginInstance):
    def install(self):
        # 下面这段代码，可以将低版本的配置文件拷贝到新版本配置系统中来，并删除旧配置文件。
        # 可以用于向下兼容
        config_file = 'resource/plugins/plugin_config_demo/old_config.yaml'
        if os.path.exists(config_file):
            yaml_config = read_yaml(config_file, _dict=True)
            for key in object.keys(yaml_config):
                self.set_config(None, key, yaml_config[key])

            os.remove(config_file)


bot = PluginConfigDemoPluginInstance(
    name='插件配置项Demo',
    version='1.2',
    plugin_id='amiyabot-plugin-config-demo',
    plugin_type='',
    description='帮助开发者了解如何与Console的配置页面对接',
    document=f'{curr_dir}/README.md',
    channel_config_default=f'{curr_dir}/channel_config_default.json',
    # 您可以选择不提供Schema, 系统会自动根据您给出的默认配置文件来猜测并提供一个编辑器
    channel_config_schema=f'{curr_dir}/channel_config_schema.json', 
    global_config_default=f'{curr_dir}/global_config_default.json',
    # 您可以选择不提供Schema, 系统会自动根据您给出的默认配置文件来猜测并提供一个编辑器
    global_config_schema=f'{curr_dir}/global_config_schema.json', 

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
