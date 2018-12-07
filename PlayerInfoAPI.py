# -*- coding: utf-8 -*-

import re
import threading
import Queue

workQueue = Queue.Queue(1)

def onServerInfo(server, info):
  global workQueue
  if (info.isPlayer == 0):
    if("following entity data" in info.content):
      player_info = {}
      name = info.content.split(" ")[0]
      dimension = re.search("(?<=Dimension: )-?\d",info.content).group()
      position_str = re.search("(?<=Pos: )\[.*?\]",info.content).group()
      position = re.findall("\[(-?\d*).*?, (-?\d*).*?, (-?\d*).*?\]",position_str)[0]
      health = re.search("(?<=Health: )-?\d*",info.content).group()
      foodlv = re.search("(?<=foodLevel: )-?\d*",info.content).group()
      player_info["Pos"] = position
      player_info["Dim"] = dimension
      player_info["Health"] = health
      player_info["foodLevel"] = foodlv
      workQueue.put(player_info)

def process_data(q):
  while(q.empty()):
    pass
  return q.get()

def getPlayerInfo(server,name):
  global workQueue
  server.execute("data get entity "+name)
  thread = WorkingThread(1, name,server,workQueue)
  thread.start()
  result = thread.join()
  return result

class WorkingThread(threading.Thread):
  def __init__(self, threadID, name, server,q):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.server = server
    self._return = None
    self.q = q
  def run(self):
    self._return = process_data(self.q)
  def join(self):
    threading.Thread.join(self)
    return self._return
    
