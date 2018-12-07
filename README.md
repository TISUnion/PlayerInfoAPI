# PlayerInfoAPI
a MCDaemon plugin to provide API for getting player information

(Thank Pandaria for providing the regular expression)

## Usage

Use imp.load_source() to load PlayerInfoAPI in your plugin first

```
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
```

### PlayerInfoAPI.getPlayerInfo(Server server,String name)

Args:
- Server server : the Server Object
- String name : name of the player who you want to get his/her info

Return:
 - a Dictionary Object of result 

please refer to the Player.dat page on minecraft wiki
[Player.dat格式](https://minecraft-zh.gamepedia.com/Player.dat%E6%A0%BC%E5%BC%8F)

## Example

```
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')

def onServerInfo(server, info):
  if info.content.startswith('!!test'):
    result = PlayerInfoAPI.getPlayerInfo(server,info.player)
    server.say("Dim:"+str(result["Dimension"])+"Pos:"+str(result["Pos"][0])+","+str(result["Pos"][1])+","+str(result["Pos"][2]))
```

you can also refer to the demo of Here plugin with this API(in newapi branch)

[Here(Demo)](https://github.com/TISUnion/Here/tree/newapi)
