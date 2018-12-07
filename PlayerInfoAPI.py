# -*- coding: utf-8 -*-

import re
import threading
import Queue
import json

workQueue = Queue.Queue(1)

def onServerInfo(server, info):
  global workQueue
  if (info.isPlayer == 0):
    if("following entity data" in info.content):
      process_str = re.sub('.*?has the following entity data: ','',info.content)  #remove title
      process_str = process_str.replace('minecraft:','')  #remove namespace
      process_str = re.sub(r"(?<=\d)[a-zA-Z]", '', process_str)  #remove letter after number
      process_str = re.sub(r"([a-zA-Z]*)(?=:)", '"\g<1>"', process_str)  #add quotation marks
      player_info = json.loads(process_str)
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
    
