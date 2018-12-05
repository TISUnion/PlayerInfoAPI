# PlayerInfoAPI
a MCDaemon plugin to provide API for getting player information
## Usage
Put this plugin in "plugins" folder and use
``` import PlayerInfoAPI ```
in your plugin


### PlayerInfoAPI.getPlayerInfo(Server server,String name)

Args:
- Server server : the Server Object
- String name : name of the player who you want to get his/her info

Return:
 - a Dictionary Object of result 
 ```
 {
   'Dim':'0',
   'Pos':('-50','64','300')
 }
 ```
| key | type | description | example value |
| ------ | ------ | ------ | ------ |
| Dim | string | dimension the player stay (by code) | '0' (means main world) |
| Pos | tuple of string | coordinate of the player (x,y,z) | ('-50','64','300') |

## Example
```
import PlayerInfoAPI

def onServerInfo(server, info):
  if info.content.startswith('!!test'):
    result = PlayerInfoAPI.getPlayerInfo(server,info.player)
    server.say("Dim:"+result["Dim"]+"Pos:"+result["Pos"][0]+","+result["Pos"][1]+","+result["Pos"][2])
```