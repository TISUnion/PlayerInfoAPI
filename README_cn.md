# PlayerInfoAPI
-------------

**正在使用 MCDR 1.0+？去看看 [MinecraftDataAPI](https://github.com/MCDReforged/MinecraftDataAPI) 吧**

一个提供获取玩家信息的 MCDReforged 插件 API

现在支持 1.14.4 以上的新 JSON 字符串格式

(感谢 Pandaria 提供的有关正则表达式的支持)

## 使用方法

你必须先使用 imp.load_source()  来在你的插件中载入PlayerInfoAPI

```
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
```

如果使用 MCDReforged 必须使用 `server.get_plugin_instance()` 来获得 PlayerInfoAPI 插件实例

```
PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
```

### 方法：PlayerInfoAPI.convertMinecraftJson(text)

将麻将牌JSON转换成Python可读取的字典数据类型

麻将牌JSON的形式如下：

- `Steve has the following entity data: [-227.5d, 64.0d, 12.3E4d]`
- `[-227.5d, 64.0d, 231.5d]`
- `Alex has the following entity data: {HurtByTimestamp: 0, SleepTimer: 0s, ..., Inventory: [], foodTickTimer: 0}`

会自动检查消息是否包含 `<name> has the following entity data: `前缀，并且会在转换前自动去除

参数：
- text: 从`/data get entity`指令或者其他命令获得的麻将牌JSON数据

返回：
- json 解析后的结果。它可以是一个 `dict`, 一个 `list`, 一个 `int` 或者一个 `None`

示例：

- 输入： `Steve has the following entity data: [-227.5d, 64.0d, 231.5d]`, 输出： `[-227.5, 64.0, 123000.0]`

- 输入： `{HurtByTimestamp: 0, SleepTimer: 0s, Inventory: [], foodTickTimer: 0}`, 输出： `{'HurtByTimestamp': 0, 'SleepTimer': 0, 'Inventory': [], 'foodTickTimer': 0}`

### 方法：PlayerInfoAPI.getPlayerInfo(server, name, path='')

自动执行 `/data get entity <name> [<path>]` 并解析返回数据

如果在 MCDReforged 中使用并且开启了rcon，插件会自动从rcon执行获得结果

参数：
- server: Server对象
- name: 要获得TA数据的目标玩家
- path: 在`/data get entity` 指令中的可选参数`path`
- timeout: 当 rcon 关闭时等待结果的最长时间。如果超时了则返回 `None`


返回：
 - 解析后的结果

你可以在Minecraft Wiki参考关于Player.det的格式信息
[Player.dat格式](https://minecraft-zh.gamepedia.com/Player.dat%E6%A0%BC%E5%BC%8F)

## 示例

```
def onServerInfo(server, info):
  if info.content.startswith('!!test'):
    result = PlayerInfoAPI.getPlayerInfo(server,info.player)
    server.say("Dim:"+str(result["Dimension"])+"Pos:"+str(result["Pos"][0])+","+str(result["Pos"][1])+","+str(result["Pos"][2]))
```

你也可以参考使用了这个API的插件例子(位于newapi分支)

[Here(Demo)](https://github.com/TISUnion/Here/tree/newapi)