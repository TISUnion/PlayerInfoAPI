# PlayerInfoAPI
a MCDaemon plugin to provide API for getting player information

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

 ```
 {
   'Dim':'0',
   'Pos':('-50','64','300'),
   'Health':'15'
 }
 ```

| key | type | description | example value |
| ------ | ------ | ------ | ------ |
| Dim | string | dimension the player stay (by code) | '0' (means main world) |
| Pos | tuple of string | coordinate of the player (x,y,z) | ('-50','64','300') |
| Health | string | health value of the palyer (in string) | '15' |

## Example

```
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')

def onServerInfo(server, info):
  if info.content.startswith('!!test'):
    result = PlayerInfoAPI.getPlayerInfo(server,info.player)
    server.say("Dim:"+result["Dim"]+"Pos:"+result["Pos"][0]+","+result["Pos"][1]+","+result["Pos"][2])
```

you can also refer to the demo of Here plugin with this API(in newapi branch)

[Here(Demo)](https://github.com/TISUnion/Here/tree/newapi)
