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

# Set debugging mode (0=No, 1=Yes)
_debug = '1'
#
# ------------------------------------------------------------------------------------------------------------------	

import requests
import sys
import re
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

# If there aren't enough arguments when the script is called, then display a message and exit.
if len(sys.argv) != 5:
 print (len(sys.argv))
 print ("Usage: python nsx-query-services.py username password nsx_manager_hostname port_number")
 sys.exit()

# Reads command line arguments and saves them to variables
_user = sys.argv[1]
_password = sys.argv[2]
_nsxmgr = sys.argv[3]
_port = sys.argv[4]

# Set the application content-type header value
myheaders = {'Content-Type': 'application/xml'}

# NSX API URL to get the Logical Switches of a particular transport zone
requests_url = 'https://%s/api/2.0/services/application/scope/%s' % (_nsxmgr, _scope)

# Submits the request to the NSX Manager
success = requests.get((requests_url), headers=myheaders, auth=(_user, _password), verify=False)

# DEBUGGING - Will parse xml response and write it to file configured in _responsefile variable
if _debug == '1':
	_responsexml = open('%s' % _responsefile, 'w+')
	_responsexml.write(success.text);
	_responsexml.close()

# Set output formatting
_outputHeaderRow = "{0:17} {1:30} {2:11} {3:16}"
_outputDataRow = "{0:17} {1:30.29} {2:11} {3:16}"

# Loads XML response into memory
doc = parseString(success.text)

# Sets up column headers 
print(_outputHeaderRow.format("ObjectID", "Name", "Protocol", "Port"))
print(_outputHeaderRow.format("-"*16, "-"*29, "-"*10, "-"*15))

def f_checkRange(y, _port):
	# Splits the variable into 2
	rangechecklist = y.split("-")
	# set the low integer port number
	l = int(rangechecklist[0])
	# set the high integer port number
	h = int(rangechecklist[1])
	# performs a check to see if the port exists between the low and high port numbers, and if it does
	# will print the data from the list
	if (l <= int(_port) and h >= int(_port)):
		print(_outputDataRow.format(data[0], data[1], data[2], data[3]))

def f_checkSingle(_int_port, _port):
	if _int_port == _port:	
		print(_outputDataRow.format(data[0], data[1], data[2], data[3]))

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
	
	# runs the regex against the port variable in the list
	m = _re_range.match(portcheck)
	
	# Checks to see if multiple ports and/or ranges are specified in the service (separated by comma)
	# If not, check to see if it contains just a range
	# lastly check the single port number
	if "," in portcheck:
		portchecklist = portcheck.split(",")
		for y in portchecklist:
			n = _re_range.match(y)
			if n:
				f_checkRange(y,_port)
			else:
				f_checkSingle(int(y), int(_port))
	elif m:
		f_checkRange(portcheck,_port)
	else:
		f_checkSingle(portcheck, _port)

exit()
