> 帮助开发者了解如何与Console的配置页面对接

*与该插件相关联的AmiyaBot版本还未正式发布，正式发布时会在频道公告*
旧版AmiyaBot请不要安装这个插件。
该插件没有任何实际功能，仅供开发者体验和测试新版插件配置项功能，并了解如何与AmiyaBotConsole进行对接。
您可以查看该插件的代码来了解如何开发此类功能。
该插件提供了一些通用的函数来读写新版AmiyaBot的两个新函数和四个新构造参数：
*注意：这两个函数和四个新构造参数不是由Core提供的，如果你是编写Core程序，则这些内容不可用。*

### 新的基类AmiyaBotPluginInstance

从新版本开始，所有插件推荐继承自兔兔中的AmiyaBotPluginInstance类，而不是Core的PluginInstance

### AmiyaBotPluginInstance的新方法

| 方法名          | 参数                                     | 释义      | 异步  |
|--------------|----------------------------------------|---------|-----|
| get_config         | channel_id, config_name   | 读取一个指定名称的配置项，如果没有频道级别的配置则返回同名全局配置，如果也没有全局配置，返回None。传入`channel_id = None`可以直接读取全局配置。  | 否  |
| set_channel_config   | channel_id, config_name, config_value       | 写入一个频道级别的配置，传入`channel_id = None`可以写入全局配置。 | 否   |

### PluginInstance的四个新新构造参数（可以不提供，成对出现）

这四个参数仅供Console在向用户展示编辑功能时使用，如果你不提供这些内容，你仍然可以使用上面的方法来读取和写入配置项字符串，只不过Console无法为你提供编辑功能。

| 属性           | 释义                        | 变动       |
|--------------|---------------------------|----------|
| channel_config_default  |  在Console中点击频道级别配置的“重置为默认值”时会被填入的值，以及创建新配置项时默认填入的值。  |       |
| channel_config_schema | 频道级别配置的JsonSchema   |       |
| global_config_default         | 在Console中点击全局配置的“重置为默认值”时会被填入的值 |  |
| global_config_schema  | 全局配置的JsonSchema |  |

想要在界面上展示“新增”按钮，则必须提供channel_config_default
想要在界面上展示“重置为默认值”按钮，则必须提供对应的schema
提供了schema则必须提供对应的default，反之则不必。

### 关于本插件

本插件提供了下面三个命令：`兔兔读取配置XXXXX`、`兔兔写入配置XXXXX值YYYYY`、`兔兔写入全局配置XXXXX值YYYYY`，可供您测试相关代码功能。

|  版本   | 变更  |
|  ----  | ----  |
| 1.0  | 最初的版本 |