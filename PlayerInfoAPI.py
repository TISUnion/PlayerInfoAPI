# -*- coding: utf-8 -*-
import copy
import re
import ast
import json
import json.decoder
try:
	import Queue
except ImportError:
	import queue as Queue

work_queue = Queue.Queue()
query_count = 0


def convertMinecraftJson(text):
	text = re.sub(r'^.* has the following entity data: ', '', text)  # yeet prefix
	text = re.sub(r'(?<=\d)[a-zA-Z](?=\D)', '', text)  # remove letter after number
	text = re.sub(r'([a-zA-Z.]+)(?=:)', '"\g<1>"', text)  # add quotation marks to all
	list_a = re.split(r'""[a-zA-Z.]+":', text)  # split good texts
	list_b = re.findall(r'""[a-zA-Z.]+":', text)  # split bad texts
	result = list_a[0]
	for i in range(len(list_b)):
		result += list_b[i].replace('""', '"').replace('":', ':') + list_a[i + 1]
	x = [i for i in mcSingleQuotationJsonReader(result)]
	return json.loads("".join(x))


def mcSingleQuotationJsonReader(data):
	part = data
	count = 1
	while True:
		spliter = part.split(r"'{", maxsplit=1)  # Match first opening braces
		yield spliter[0]
		if len(spliter) == 1:
			return  # No more
		else:
			part_2 = spliter[1].split(r"}'")  # Match all closing braces
			index = 0
			res = jsonCheck("".join(part_2[:index + 1]))
			while not res:
				index += 1
				if index == len(part_2):
					raise RuntimeError("Out of index")  # Looks like illegal json string
				res = jsonCheck("".join(part_2[:index + 1]))
			j_dict = ""
			while res:
				# Is real need?
				j_dict = res
				index += 1
				if index == len(part_2):
					break  # Yep, is real
				res = jsonCheck("".join(part_2[:index + 1]))

			yield j_dict  # Match a json string

		# Restore split string
		part_2 = part_2[index:]
		part = part_2[0]
		if len(part_2) > 1:
			for i in part_2[1:]:
				part += "}'"
				part += i
		count += 1


def jsonCheck(j):
	checking = "".join(["{", j, "}"])
	try:
		# Plan A
		# checking = checking.replace("\"", "\\\"")
		# checking = checking.replace("\'","\\\'")
		# checking = checking.replace("\\n", "\\\\n")
		checking = checking.replace(r'\\', "\\")
		res = json.loads(checking)
	except json.decoder.JSONDecodeError:
		try:
			# Plan B
			res = ast.literal_eval(checking)
		except Exception:
			return False

	data = json.dumps({"data": json.dumps(res)})
	return data[9:-1]


def getPlayerInfo(server, name, path=''):
	if len(path) >= 1 and not path.startswith(' '):
		path = ' ' + path
	command = 'data get entity {}{}'.format(name, path)
	if hasattr(server, 'MCDR') and server.is_rcon_running():
		result = server.rcon_query(command)
	else:
		global query_count
		query_count += 1
		try:
			server.execute(command)
			global work_queue
			while work_queue.empty():
				pass
			result = work_queue.get()
		finally:
			query_count -= 1
	return convertMinecraftJson(result)


def cleanQueue():
	while not work_queue.empty():
		work_queue.get()


def onServerInfo(server, info):
	global work_queue
	if info.isPlayer == 0:
		if ' has the following entity data: ' in info.content:
			if query_count > 0:
				work_queue.put(info.content)
			else:
				cleanQueue()


def on_info(server, info):
	info2 = copy.deepcopy(info)
	info2.isPlayer = info2.is_player
	onServerInfo(server, info2)
