# PlayerInfoAPI
-------------

[中文](#https://github.com/TISUnion/PlayerInfoAPI/blob/master/README_cn.md)

a MCDaemon plugin to provide API for getting player information

Compatible with MCDaemon and MCDReforged

Now support 1.14+ new JSON string format

(Thank Pandaria for providing the regular expression)

## Usage

Use imp.load_source() to load PlayerInfoAPI in your plugin first

```
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
```

for MCDReforged use `server.get_plugin_instance()` to get PlayerInfoAPI instance

```
PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
```

### PlayerInfoAPI.convertMinecraftJson(text)

Convert Minecraft style json format into a dict

Minecraft style json format is something like these:

- `Steve has the following entity data: [-227.5d, 64.0d, 12.3E4d]`
- `[-227.5d, 64.0d, 231.5d]`
- `Alex has the following entity data: {HurtByTimestamp: 0, SleepTimer: 0s, ..., Inventory: [], foodTickTimer: 0}`

It will automatically detect if there is a `<name> has the following entity data: `. If there is, it will erase it before converting

Args:
- text: A data get entity or other command result that use Minecraft style json format

Return:
- a parsed json result

Samples:

- Input `Steve has the following entity data: [-227.5d, 64.0d, 231.5d]`, output `[-227.5, 64.0, 123000.0]`

- Input `{HurtByTimestamp: 0, SleepTimer: 0s, Inventory: [], foodTickTimer: 0}`, output `{'HurtByTimestamp': 0, 'SleepTimer': 0, 'Inventory': [], 'foodTickTimer': 0}`

### PlayerInfoAPI.getPlayerInfo(server, name, path='')

Call `data get entity <name> [<path>]` and parse the result

If it's in MCDReforged and rcon is enabled it will use rcon to query

Args:
- server: the Server Object
- name: name of the player who you want to get his/her info
- path: an optional `path` parameter in `data get entity` command

Return:
 - a parsed json result

Please refer to the Player.dat page on minecraft wiki
[Player.dat格式](https://minecraft-zh.gamepedia.com/Player.dat%E6%A0%BC%E5%BC%8F)

## Example

```
def onServerInfo(server, info):
  if info.content.startswith('!!test'):
    result = PlayerInfoAPI.getPlayerInfo(server,info.player)
    server.say("Dim:"+str(result["Dimension"])+"Pos:"+str(result["Pos"][0])+","+str(result["Pos"][1])+","+str(result["Pos"][2]))
```

you can also refer to the demo of Here plugin with this API(in newapi branch)

[Here(Demo)](https://github.com/TISUnion/Here/tree/newapi)
