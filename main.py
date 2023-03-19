import os
import json
import re

from amiyabot import PluginInstance, Message, Chain
from core.util import create_dir, read_yaml, run_in_thread_pool
from core import log

curr_dir = os.path.dirname(__file__)

class PluginConfigDemoPluginInstance(PluginInstance):
    def install(self):
        # 第一步，插件加载时，读取默认的全局配置和默认的频道配置，以及两者的模板并写入插件对象
        self.default_global_config = '\n'.join(open(f'{curr_dir}/default_global_config.json', 'r', encoding='utf-8').readlines())
        self.global_config_template = '\n'.join(open(f'{curr_dir}/global_config_schema.json', 'r', encoding='utf-8').readlines())        
        # 如果您的插件不需要频道专属配置，则可以忽略
        self.default_channel_config = '\n'.join(open(f'{curr_dir}/default_channel_config.json', 'r', encoding='utf-8').readlines())
        self.channel_config_template = '\n'.join(open(f'{curr_dir}/channel_config_schema.json', 'r', encoding='utf-8').readlines())    


        # 判断amiyabot的版本是否支持set_global_config再进行后续操作
        if hasattr(bot, 'set_global_config'):            
            if hasattr(bot, 'get_global_config'):
                if bot.get_global_config() is None:
                    # 如果目前还没有GlobalConfig，则写入默认GlobalConfig，这里需要您开发者自己检测并写入
                    # 您可以通过这种方式，来判断这个bot以前是否安装过该插件
                    bot.set_global_config(self.default_global_config)
                    
            # 如果您还想兼容旧的yaml配置或者您曾经使用的其他配置，您可以在这里读取
            config_file = 'resource/plugins/plugin_config_demo/old_config.yaml'
            if os.path.exists(config_file):
                yamlConfig = read_yaml(config_file, _dict=True)
                bot.set_global_config(
                    json.dumps(
                    {
                        'api_key': yamlConfig.get('api_key', ''),
                        'stop_word': yamlConfig.get('stop_word', ''),
                        'proxy': yamlConfig.get('proxy', ''),
                        'predef_context': yamlConfig.get('predef_context', '')
                    })
                )

bot = PluginConfigDemoPluginInstance(
    name='插件配置项Demo',
    version='1.0',
    plugin_id='amiyabot-plugin-config-demo',
    plugin_type='',
    description='帮助开发者了解如何与Console的配置页面对接',
    document=f'{curr_dir}/README.md'
)

def get_config(channel_id, configName):
    if not hasattr(bot, 'get_global_config'):
        # 判断amiyabot的版本是否支持set_global_config
        # 如果是旧版，您可以在这里读取旧的配置文件
        config_file = 'resource/plugins/plugin_config_demo/config.yaml'
        if os.path.exists(config_file):
            yamlConfig = read_yaml(config_file, _dict=True)
            if configName in yamlConfig.keys():
                return yamlConfig[configName]
        return None
    
    # 这段代码展示了推荐的Config读取方式，也就是在全局和频道级别配置项都是Json的情况下，用相同名称的配置项来实现频道覆盖全局
    # 先查看频道专属配置中是否有此名称，再判断全局配置中是否有此名称，都没有最后返回None
    if channel_id and len(str(channel_id).strip()) > 0:
        conf = bot.get_channel_config(str(channel_id))
        jsonConfig = json.loads(conf)
        if configName in jsonConfig.keys():
            return jsonConfig[configName]
        
    conf = bot.get_global_config()
    jsonConfig = json.loads(conf)
    if configName in jsonConfig.keys():
        return jsonConfig[configName]
    
    return None

def set_config(channel_id, configName, value):
    # 检查 bot 对象是否支持设置配置
    if not hasattr(bot, 'set_global_config'):
        return None

    # 先获取已有的配置，然后将修改的值与其合并
    if channel_id and len(str(channel_id).strip()) > 0:
        conf = bot.get_channel_config(str(channel_id))
    else:
        conf = bot.get_global_config()

    jsonConfig = json.loads(conf)
    jsonConfig[configName] = value
    newConf = json.dumps(jsonConfig)

    # 如果 channel_id 为 None，则保存到全局配置
    if not channel_id:
        bot.set_global_config(newConf)
    else:
        bot.set_channel_config(str(channel_id), newConf)

    # 返回新的配置值
    return value

@bot.on_message(keywords=['写入全局配置'], level=5)
async def save_global_config(data: Message):
    match = re.search(r"写入全局配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        set_config(None,key,value)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')

@bot.on_message(keywords=['写入配置'], level=5)
async def save_channel_config(data: Message):
    match = re.search(r"写入配置(\w+)值(\w+)", data.text)
    if match:
        key = match.group(1)
        value = match.group(2)
        set_config(data.channel_id,key,value)
        return Chain(data).text('成功写入')
    else:
        return Chain(data).text('未找到指定的字串')

@bot.on_message(keywords=['读取配置'], level=5)
async def check_config(data: Message):
    index = data.text.find('读取配置')
    if index != -1:
        result_str = data.text[index + len('读取配置'):]
        return Chain(data).text(get_config(data.channel_id, result_str))
    else:
        return Chain(data).text('未找到指定的字串')