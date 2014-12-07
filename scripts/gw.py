#!/usr/bin/env python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi, cgitb, os, json, shelve
cgitb.enable()

def retAllPatients():
	allpatients=[\
	{"name":"Renner, Jeremy", "dob":"07-Jan-71", "visit_id":"3141", "room":"8S-853-A", "status":"ADM", "arrival":"1-Jan-14", "provider":"House MD, Gregory"},\
	{"name":"Blunt, Emily", "dob":"23-Feb-83", "visit_id":"5926", "room":"8S-852-D", "status":"ADM", "arrival":"1-Jan-14", "provider":"Forman, Eric"},\
	{"name":"Penn, Sean", "dob":"17-Aug-60", "visit_id":"5358", "room":"8S-851-C", "status":"ADM", "arrival":"1-Jan-14", "provider":"Wilson, James"},\
	{"name":"Pegg, Simon", "dob":"14-Feb-70", "visit_id":"9793", "room":"8S-850-B", "status":"ADM", "arrival":"1-Jan-14", "provider":"Chase, Robert"},\
	{"name":"Neeson, Liam", "dob":"07-Jun-52", "visit_id":"2384", "room":"8S-849-A", "status":"ADM", "arrival":"1-Jan-14", "provider":"Cameron, Allison "}
	]
	return json.dumps(allpatients)

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
	#retAllPatients()