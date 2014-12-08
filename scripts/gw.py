#!/usr/bin/env python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi, cgitb, os, json, shelve as sh, time
from listedDict import *
cgitb.enable()

def resetDb():
	allpatients={
	"3141":{"name":"Renner, Jeremy", "dob":"07-Jan-71", "room":"8S-853-A", "status":"ADM", "arrival":"1-Jan-14", "provider":"House MD, Gregory"},\
	"5926":{"name":"Blunt, Emily", "dob":"23-Feb-83", "room":"8S-852-D", "status":"ADM", "arrival":"1-Jan-14", "provider":"Forman, Eric"},\
	"5358":{"name":"Penn, Sean", "dob":"17-Aug-60","room":"8S-851-C", "status":"ADM", "arrival":"1-Jan-14", "provider":"Wilson, James"},\
	"9793":{"name":"Pegg, Simon", "dob":"14-Feb-70", "room":"8S-850-B", "status":"ADM", "arrival":"1-Jan-14", "provider":"Chase, Robert"},\
	"2384":{"name":"Neeson, Liam", "dob":"07-Jun-52", "room":"8S-849-A", "status":"ADM", "arrival":"1-Jan-14", "provider":"Cameron, Allison "}
	}
	patienHistory={
	
	}
	with sh.open('../shelveDB', writeback=True) as db:
		dbUpdate(db, allpatients ,'allpatients')

def retAllPatients():
	allpatients = listedDict()
	with sh.open('../shelveDB') as db:
		allpatients = json.dumps(db.get('allpatients'))
	return allpatients

def getFromPath(obj, itemPath):
	try:
		itemPath = itemPath.split('.') if isinstance(itemPath,str) else itemPath
		return reduce(dict.get, itemPath, obj)
	except TypeError:
		print('Warning: Invalid path')
		return None
	except:
		raise

def dbUpdate(db, obj,pathString):
	path = pathString.split('.') if not isinstance(pathString, list) else pathString
	ld = listedDict()
	ld.populateNestedDict(pathString, obj)
	db[path[0]]=ld[path[0]]

def dbDeleteItem(db,itemPath):
	path = itemPath.split('.') if not isinstance(itemPath, list) else itemPath
	try:
		if len(path)==1 and db.get(path[0]):
			del db[path[0]]
		else:
			dbDeleteItem(db[path.pop(0)], path)
	except KeyError:
		print('Invalid path provided to delete')
		return

def main():
	print("Content-Type: text/html;charset=utf-8\n")
	query = cgi.parse_qs(os.environ.get('QUERY_STRING'))
	if query!=None:
		if len(query)>0:
			for key, value in query.items():
				if key=='table' and value[0]=='allpatients':
					print(retAllPatients())

if __name__ == '__main__':
	main()
	'''
	resetDb()
	with sh.open('../shelveDB', writeback=True) as db:
		for item in db:
			print(db[item])
		time.sleep(3)
		dbDeleteItem(db, 'allpatients.9793')
		dbDeleteItem(db, 'allpatients.5926')
		for item in db:
			print(db[item])
	'''