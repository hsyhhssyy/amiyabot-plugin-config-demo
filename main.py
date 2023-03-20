import os
import json
import re

from amiyabot import Message, Chain
from core.util import create_dir, read_yaml, run_in_thread_pool
from core import log
from core.amiyaBotPluginInstance import AmiyaBotPluginInstance

curr_dir = os.path.dirname(__file__)


class PluginConfigDemoPluginInstance(AmiyaBotPluginInstance):
    def install(self):
        # 如果您还想兼容旧的yaml配置或者您曾经使用的其他配置，您可以在这里读取
        config_file = 'resource/plugins/plugin_config_demo/old_config.yaml'
        if os.path.exists(config_file):
            yaml_config = read_yaml(config_file, _dict=True)
            for key in object.keys(yaml_config):
                self.set_config(None, key, yaml_config[key])

            os.remove(config_file)


bot = PluginConfigDemoPluginInstance(
    name='插件配置项Demo',
    version='1.1',
    plugin_id='amiyabot-plugin-config-demo',
    plugin_type='',
    description='帮助开发者了解如何与Console的配置页面对接',
    document=f'{curr_dir}/README.md',
    channel_config_default=f'{curr_dir}/channel_config_default.json',
    channel_config_schema=f'{curr_dir}/channel_config_schema.json',
    global_config_default=f'{curr_dir}/global_config_default.json',
    global_config_schema=f'{curr_dir}/global_config_schema.json',

)


@bot.on_message(keywords=['写入全局配置'], level=5)
async def save_global_config(data: Message):
    match = re.search(r"写入全局配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        bot.set_config(None, key, value)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')


@bot.on_message(keywords=['写入配置'], level=5)
async def save_channel_config(data: Message):
    match = re.search(r"写入配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        bot.set_config(data.channel_id, key, value)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')


@bot.on_message(keywords=['读取配置'], level=5)
async def check_config(data: Message):
    index = data.text.find('读取配置')
    if index != -1:
        result_str = data.text[index + len('读取配置'):]
        return Chain(data).text(f'{bot.get_config(data.channel_id, result_str)}')
    else:
        return Chain(data).text('未找到指定的字串')
