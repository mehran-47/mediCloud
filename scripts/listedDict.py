#!/usr/bin/env python3
from functools import reduce #functools.reduce(dict.get,['a','b','c'],dc)
import json, copy

def colorPrint(string, *stringAttrs, **allStringAttrs):
	colorMap = {\
		'PURPLE' : '\033[95m',\
		'CYAN' : '\033[96m',\
		'DARKCYAN' : '\033[36m',\
		'BLUE' : '\033[94m',\
		'GREEN' : '\033[92m',\
		'YELLOW' : '\033[93m',\
		'RED' : '\033[91m',\
		'BOLD' : '\033[1m',\
		'UNDERLINE' : '\033[4m',\
		'END' : '\033[0m'}
	if len(stringAttrs)>0:
		for attr in stringAttrs:
			string = colorMap.get(str(attr).upper()) + str(string) + colorMap['END']
		print(string)
	if len(allStringAttrs)>0:
		for stringAttrTuple in allStringAttrs.values():
			for attr in stringAttrTuple:
				string = colorMap.get(str(attr).upper()) + str(string) + colorMap['END']
			print(string)

class listedDict(dict):
	def __init__(self):
		pass

	def populateNestedDict(self, itemPath, item):
		itemPath = itemPath.split('.') if isinstance(itemPath,str) else itemPath
		if len(itemPath)==1:
			self[itemPath[0]] = item
		else:
			self[itemPath[0]] = listedDict() if not isinstance(self.get(itemPath[0]), dict) else self[itemPath[0]]
			listedDict.populateNestedDict(self[itemPath.pop(0)], itemPath, item)

	def keypaths(self):
		# http://stackoverflow.com/questions/18819154/python-finding-parent-keys-for-a-specific-value-in-a-nested-dictionary
		for key, value in self.items():
			if isinstance(value, dict):
				for subkey, subvalue in listedDict.keypaths(value):
					yield [key]+subkey, subvalue
			else:
				yield [key], value

	def reverse_dict(self):
		reverse_dict = listedDict()
		for keypath, value in self.keypaths():
		    reverse_dict[str(value)] = keypath
		return reverse_dict

	def getFromPath(self, itemPath):
		try:
			itemPath = itemPath.split('.') if isinstance(itemPath,str) else itemPath
			return reduce(dict.get, itemPath, self)
		except TypeError:
			print('Warning: Invalid path')
			return None
		except:
			raise

	def getFromPath_o(self, itemPath):
		itemPath = itemPath.split('.') if isinstance(itemPath,str) else itemPath
		if len(itemPath)==1:
			return self.get(itemPath[0])
		else:
			if isinstance(self.get(itemPath[0]), dict):
				print(itemPath)
				listedDict.getFromPath(self[itemPath.pop(0)], itemPath)
			else:
				print(itemPath)
				print(self.get(itemPath[0]))
				return None

	def lookupValuePath(self, key):
		return self.reverse_dict().get(str(key))

	def deleteItem(self, itemPath):
		try:
			itemPath = itemPath.split('.') if isinstance(itemPath,str) else itemPath
			if len(itemPath)==1 and self.get(itemPath[0]):
				del self[itemPath[0]]
			else:
				listedDict.deleteItem(self[itemPath.pop(0)], itemPath)
		except KeyError:
			print('Invalid path provided to delete')
			return

	def prettyPrint(self, indent, **kwargs):
		for key, value in sorted(self.items()):
			if isinstance(value, dict):
				if len(value)>0:
					if kwargs.get('keyColor')!=None:
						colorPrint(('  '*indent)+'"'+str(key)+'":', allStringAttrs=kwargs['keyColor'])
					else:
						print(('  '*indent)+'"'+str(key)+'":')
				listedDict.prettyPrint(value, indent+1, keyColor=kwargs.get('keyColor'), valColor=kwargs.get('valColor'))
			else:
				if kwargs.get('valColor')!=None:
						colorPrint('  '*(indent+1)+'"'+str(key)+'":"'+str(value)+'",', allStringAttrs=kwargs['valColor'])
				else:
					print('  '*(indent+1)+'"'+str(key)+'":"'+str(value)+'",')

	def dictPrint(self):
		print(json.dumps(self, sort_keys=True))

	def saveAt(self, filePath):
		with open(filePath, 'w') as fs:
			fs.write(json.dumps(self, sort_keys=True))

	def loadFrom(self, filePath):
		with open(filePath, 'r') as fs:
			self = json.loads(fs.read())
		return self

	def structureDiff(self, listedDict):
		vals_1 = [str(item) for item in self.reverse_dict().values()]
		vals_2 = [str(item) for item in listedDict.reverse_dict().values()]
		return list(set(vals_1)-set(vals_2))+list(set(vals_2)-set(vals_1))

	def updateUsage(self, usageDict):
		for key, value in self.items():
			if isinstance(value, dict):
				listedDict.updateUsage(value, usageDict)
			elif isinstance(value, float):
				if key in usageDict:
					usageDict[key]+=self[key]
				else:
					usageDict[key]=self[key]			


if __name__ == '__main__':
	#'''
	#Some tests of the API
	###
	X = listedDict()
	X.populateNestedDict('a.b1',{'ab_val':5.0, 'cd_val':4.4})
	X.populateNestedDict('a.b2',{'ab_val':7.0, 'de_val':1.1})
	X.populateNestedDict('a.b.c1','abc1_val')
	X.populateNestedDict('a.b.c2','abc2_val')
	print('printing X:\n')
	X.prettyPrint(0)
	print('printing usage:\n')
	#X.updateUsage({})
	tu = {}
	X.updateUsage(tu)
	print(tu)
	'''
	print(X.getFromPath(input('Provide path to get value: (e.g. a.b.c )\n> ')))
	Y = listedDict()
	Y = copy.deepcopy(X)
	print('printing Y:\n')
	Y.prettyPrint(0)
	pathtodel = str(input('select node to delete from Y for diff. Blank input will mean X=Y\n> '))
	if len(pathtodel)>0:
		Y.deleteItem(pathtodel)
	print('printing Y:\n')
	Y.prettyPrint(0)
	print('printing X:\n')
	X.prettyPrint(0)
	print('Difference between X and Y')
	print(X.structureDiff(Y))
	X.saveAt(input('Save at filepath:\n> '))
	Y = listedDict()
	print(Y.loadFrom(input('load from filepath:\n> ')))
	print(X.getFromPath(input('Provide path to get value: (e.g. a.b.c )\n> ')))
	print('keypaths:\n%s'%(str(X.keypaths())))
	print('reverse-dict:\n%s'%(X.reverse_dict()))
	print(X.lookupValuePath(input('\nlookup in nested dict with value\n> ')))
	X.deleteItem(input('type path to delete item/dict from main tree\n> '))
	print(X)
	'''