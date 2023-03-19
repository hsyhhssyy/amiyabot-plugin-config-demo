> 帮助开发者了解如何与Console的配置页面对接

旧版AmiyaBot请不要安装这个插件。
该插件没有任何实际功能，仅供开发者体验和测试新版插件配置项功能，如何与AmiyaBotConsole进行对接。
您可以查看该插件的代码来了解如何开发此类功能。
该插件提供了一些通用的函数来读写新版AmiyaBot的四个新函数和四个新属性：
*注意：这四个函数和四个属性不是由Core提供的，如果你是编写Core程序，则这些内容不可用。*

### PluginInstance的四个新方法

| 方法名          | 参数                                     | 释义      | 异步  |
|--------------|----------------------------------------|---------|-----|
| get_channel_config         | channel_id                                  | 读取一个频道级别的配置  | 是   |
| set_channel_config         | channel_id,json       | 写入一个频道级别的配置  | 是   |
| get_global_config | 无 | 读取一个全局的配置 | 是   |
| set_global_config       |  json  | 写入一个全局的配置    | 是   |

### PluginInstance的四个新属性（需要由您根据需求创建，默认并不存在）

这四个属性仅供Console在向用户展示编辑功能时使用，如果你不提供这些内容，你仍然可以使用上面的四个方法来读取和写入配置项字符串，并把他们当成任意内容来解析。（也就是说你也可以在里面存储ini，yaml等格式的文件，只不过Console无法为你提供智能编辑功能）

| 属性           | 释义                        | 变动       |
|--------------|---------------------------|----------|
| default_global_config         | 在Console中点击全局配置的“重置为默认值”时会被填入的值 |  |
| global_config_template  | 全局配置的JsonSchema |  |
| default_channel_config  |  在Console中点击频道级别配置的“重置为默认值”时会被填入的值，以及创建新配置项时默认填入的值。  |       |
| channel_config_template | 频道级别配置的JsonSchema   |       |

想要在界面上展示“新增”按钮，则必须提供channel_config_template
想要在界面上展示“重置为默认值”按钮，则必须提供对应的template
没有提供Template的情况下，界面为纯文本编辑。

### 关于本插件

本插件提供了下面三个命令：`兔兔读取配置XXXXX`、`兔兔写入配置XXXXX值YYYYY`、`兔兔写入全局配置XXXXX值YYYYY`，可供您测试相关代码功能。

|  版本   | 变更  |
|  ----  | ----  |
| 1.0  | 最初的版本 |