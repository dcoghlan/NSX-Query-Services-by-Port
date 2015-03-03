#
# Script to search VMware NSX-v services by port number
# Written by Dale Coghlan
# Date: 03 Feb 2015
# https://github.com/dcoghlan/NSX-Query-Services-by-Port

# ------------------------------------------------------------------------------------------------------------------	
# Set some variables. No need to change anything else after this section

# Sets a variable to save the HTTP/XML reponse so it can be parsed and displayed.
_responsefile = 'debug-xml-services.xml'

# Set the managed object reference
_scope = 'globalroot-0'

# Uncomment the following line to hardcode the password. This will remove the password prompt.
#_password = 'VMware1!'
#
# ------------------------------------------------------------------------------------------------------------------	

import requests
import sys
import re
import argparse
import getpass
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse, parseString

try:
	# Only needed to disable anoying warnings self signed certificate warnings from NSX Manager.
	import urllib3
	requests.packages.urllib3.disable_warnings()
except ImportError:
	# If you don't have urllib3 we can just hide the warnings 
	logging.captureWarnings(True)

parser = argparse.ArgumentParser(description="Queries NSX Manager for a list of services configured with a specific port")
parser.add_argument("-u", help="OPTIONAL - NSX Manager username (default: %(default)s)", metavar="user", dest="_user", nargs="?", const='admin')
parser.set_defaults(_user="admin")
parser.add_argument("-n", help="NSX Manager hostname, FQDN or IP address", metavar="nsxmgr", dest="_nsxmgr", type=str, required=True)
parser.add_argument("-p", help="TCP/UDP port number", metavar="port", dest="_port", required=True)
parser.add_argument("-r", help="Include port ranges in the output", dest="_searchRanges", action="store_true")
parser.add_argument("-d", help="Enable script debugging", dest="_debug", action="store_true")
args = parser.parse_args()

# Check to see if the password has been hardcoded. If it hasn't prompt for the password
try: 
	_password
except NameError:
	_password = getpass.getpass(prompt="NSX Manager password:")

# Reads command line flags and saves them to variables
_user = args._user
_nsxmgr = args._nsxmgr
_port = args._port

# Set the application content-type header value
myheaders = {'Content-Type': 'application/xml'}

# NSX API URL to get all services configured in the specified scope
requests_url = 'https://%s/api/2.0/services/application/scope/%s' % (_nsxmgr, _scope)

# Submits the request to the NSX Manager
success = requests.get((requests_url), headers=myheaders, auth=(_user, _password), verify=False)

def f_debugMode():
	_responsexml = open('%s' % _responsefile, 'w+')
	_responsexml.write(success.text)
	_responsexml.close()
	print()
	print("Status Code = %s" % success.status_code)
	print("API response written to %s" % _responsefile)

def f_checkRange(y, _port):
	_exists = "n"
	if args._searchRanges:
		# Splits the variable into 2
		rangechecklist = y.split("-")
		# set the low integer port number
		l = int(rangechecklist[0])
		# set the high integer port number
		h = int(rangechecklist[1])
		# performs a check to see if the port exists between the low and high port numbers, and if it does
		# will print the data from the list
		if (l <= int(_port) and h >= int(_port)):
			_exists = "y"
	return _exists

def f_checkSingle(_int_port, _port):
	_exists = "n"
	if _int_port == _port:	
		_exists = "y"
	return _exists

def f_printDataRow():
	print(_outputDataRow.format(data[0], data[1], data[2], data[3]))
	
# If something goes wrong with the xml query, and we dont get a 200 status code returned,
# enabled debug mode and exit the script.
if int(success.status_code) != 200:
	f_debugMode()
	exit()

# Checks to see if debug mode is enabled
if args._debug:
	f_debugMode()
	
# Loads XML response into memory
doc = parseString(success.text)

# Set output formatting
_outputHeaderRow = "{0:17} {1:30} {2:11} {3:16}"
_outputDataRow = "{0:17} {1:30.29} {2:11} {3:16}"

# Sets up column headers
print() 
print(_outputHeaderRow.format("ObjectID", "Name", "Protocol", "Port"))
print(_outputHeaderRow.format("-"*16, "-"*29, "-"*10, "-"*15))
	
# Loads xml document into memory using the application element
nodes = doc.getElementsByTagName('application')

# Iterates through each application element
for node in nodes:
	# clears the list
	data = [];
	# Gets the objectId of the application  
	appObjectId = node.getElementsByTagName("objectId")[0]
	# Get the name of the application
	name = node.getElementsByTagName("name")[0]
	# Sets the list to start with the objectID
	data = [(appObjectId.firstChild.data)]
	# Appends the application name to the list
	data.append(name.firstChild.data);
	# Within the application node, loads the element called "element"
	elements = node.getElementsByTagName('element')
	# Checks to see if the element actually exists
	if elements:
		# If element does exist, iterate through it
		for element in elements:
			# Load the element called applicationProtocol
			protocol = element.getElementsByTagName("applicationProtocol")[0]
			# Check to see if the element contains a child
			if protocol.firstChild:
				# If it contains the applicatioProtocol element then append the data to the list
				data.append(protocol.firstChild.data);
			else:
				# So if there is no element called applicationProtocol, append the string to the list
				data.append("no protocol")
			# Load the element called value
			port = element.getElementsByTagName("value")[0]
			# Check to see if the element contains a child
			if port.firstChild:
				# If it contains the value element then append the data to the list
				data.append(port.firstChild.data);
			else:
				# So if there is no element called value, append the string to the list
				data.append("no port value")
	else:
		# Will drop through to here if there is no element called "element". Some built in services 
		# seem to be structured like this and essentially have no protocol or port defined in NSX.
		# NOTE: These also seem to be marked as read-only services
		data.append("no protocol");
		data.append("no port");
	
	# loads the data in the "value" element (port/ports) into a variable to we can check it
	portcheck = data[3]

	# sets up regular expression to look for ranges within a variable
	_re_range = re.compile(".*\,*[0-9]+\-[0-9]+")
	
	# runs the regex against the port variable in the list to see if a range exists? We will use this further down.
	m = _re_range.match(portcheck)
	
	# Checks to see if multiple ports and/or ranges are specified in the service (separated by comma)
	# If not, check to see if it contains just a range
	# lastly check the single port number
	if "," in portcheck:
		portchecklist = portcheck.split(",")
		_existenceCount = 0
		for z in portchecklist:
			n = _re_range.match(z)
			if n:
				_exists=(f_checkRange(z,_port))
				if _exists =="y":
					_existenceCount += 1
			else:
				_exists=(f_checkSingle(int(z), int(_port)))
				if _exists =="y":
					_existenceCount += 1
		if _existenceCount >= 1:
			f_printDataRow()
	elif m:
		_exists=(f_checkRange(portcheck,_port))
		if _exists == "y":
			f_printDataRow()
	else:
		_exists=(f_checkSingle(portcheck, _port))
		if _exists == "y":
			f_printDataRow()

exit()
