# 帮助开发者了解如何与Console的配置页面对接

*与该插件相关联的AmiyaBot版本还未正式发布，正式发布时会在频道公告*
旧版AmiyaBot请不要安装这个插件，旧版本下该插件无法启动。
该插件没有任何实际功能，仅供开发者体验和测试新版插件配置项功能，并了解如何与AmiyaBotConsole进行对接。
您可以查看该插件的代码来了解如何开发此类功能。
该插件提供了一些通用的函数来读写新版AmiyaBot的两个新函数和四个新构造参数：
*注意：这两个函数和四个新构造参数不是由Core提供的，如果你是编写Core程序，则这些内容不可用。*

### 新的基类AmiyaBotPluginInstance

从新版本开始，所有插件推荐继承自兔兔中的AmiyaBotPluginInstance类，而不是Core的PluginInstance
您可以在这里找到他：
`from core.customPluginInstance import AmiyaBotPluginInstance`

### AmiyaBotPluginInstance的新方法

| 方法名          | 参数                                     | 释义      | 异步  |
|--------------|----------------------------------------|---------|-----|
| get_config         | channel_id, config_name   | 读取一个指定名称的配置项，如果没有频道级别的配置则返回同名全局配置，如果也没有全局配置，返回None。传入`channel_id = None`可以直接读取全局配置。  | 否  |
| set_config   | channel_id, config_name, config_value       | 写入一个频道级别的配置，传入`channel_id = None`可以强制指定写入全局配置。 | 否   |

### PluginInstance的四个新新构造参数（可以不提供，成对出现）

这四个参数仅供Console在向用户展示编辑功能时使用，如果你不提供这些内容，你仍然可以使用上面的方法来读取和写入配置项字符串，只不过Console无法为你提供编辑功能。

> Schema指的是一个符合标准的JSONSchema，有关于JSONSchema，您可以在[这里](http://json-schema.org/ "这里")找到他们的官方文档。
当然，如果您不想去看复杂的文档，也可以参照本插件内给出的例子，或者干脆不提供Schema

这四个参数以下面的四个形式提供都是合法的：
1. 磁盘上JSON文件的路径字符串。
2. 磁盘上YAML文件的路径字符串。
3. 一个JSON字符串。
4. 一个YAML字符串。
5. 一个实现了__dict__的对象，比如Python中的dict。


| 属性           | 释义                        | 说明      |
|--------------|---------------------------|----------|
| channel_config_default  |  在Console中点击频道级别配置的`重置为默认值`时会被填入的值，以及创建新配置项时默认填入的值。  |       |
| channel_config_schema | 频道级别配置的JsonSchema   |   可选  |
| global_config_default         | 在Console中点击全局配置的`重置为默认值`时会被填入的值 |  |
| global_config_schema  | 全局配置的JsonSchema |  可选  |

插件加载时会进行下面的校验，校验不通过则会报错：
- 提供了schema则必须提供对应的default，反之则不必。
- 如果给出了schema，则会用schema对提供的default进行校验。
- 如果没有给出schema，则Console会使用提供的default的值来推测配置文件的结构。

此外，Console的界面还对配置文件有下列要求：
- 想要在界面上展示`新增`按钮，则必须提供`channel_config_default`。
- 想要在界面上展示`重置为默认值`按钮，则必须提供对应的schema。

### 如何在插件中使用

插件初次安装初次加载时，会将`global_config_default`作为默认全局配置写入数据库。该过程发生在构造函数，因此您如果需要对全局配置进行初始化操作，您需要在您的PluginInstance的构造函数，或者install函数中进行。

一般来说，建议将channel_config和global_config的default（和Schema）都设置成一样的，这样插件的用户可以针对每个channel都独立的配置插件。

你在get_config时读取的每个配置项，如果没有channel级别的config，就会返回global级别的值，这样，你就不需要去判断用户到底是否提供了channel级的配置。

举例来说，如果一个chatgpt插件设置了一些角色扮演的预制prompt，这些配置项就可以是channel级别的，全局中，这个配置项为空。
这样，只有在指定的频道里，插件才会执行角色扮演，或者在不同的频道里扮演不同的角色。

不过如果你非常确定某个配置项，永远不会有频道级别的配置，比如chatgpt插件里openai的api_key，你可以选择只在global的default（和Schema）里给出，这样channel级别的配置页面上就不会出现这个文本框。

### 关于本插件

本插件提供了下面三个命令：`兔兔读取配置XXXXX`、`兔兔写入配置XXXXX值YYYYY`、`兔兔写入全局配置XXXXX值YYYYY`，可供您测试相关代码功能。

例如您可以问`兔兔读取配置array_option`

|  版本   | 变更  |
|  ----  | ----  |
| 1.1  | 最初的版本 |
| 1.1  | 完善了部分文档 |