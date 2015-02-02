#
# Script to get NSX services
 
import requests
import sys
import xml.etree.ElementTree as ET

#
# Module to help display XML correctly
from xml.dom.minidom import parse, parseString

#
# Sets a variable to save the HTTP/XML reponse so it can be parsed and displayed.
_responsefile = 'xml-services.xml'

#
# Set the datacenter managed object reference for your specific deployment
_dcmoref = 'datacenter-2'

#
# If there aren't enough arguments when the script is called, then display a message and exit.
if len(sys.argv) != 5:
 print (len(sys.argv))
 print ("Usage: python nsx-query-services.py username password nsx_manager_hostname port_number")
 sys.exit()

#
# Reads command line arguments and saves to an array
_user = sys.argv[1]
_password = sys.argv[2]
_nsxmgr = sys.argv[3]
x = sys.argv[4]

#
# Set the application content-type header value
myheaders = {'Content-Type': 'application/xml'}

#
# NSX API URL to get the Logical Switches of a particular transport zone
requests_url = 'https://%s/api/2.0/services/application/scope/%s' % (_nsxmgr, _dcmoref)

#
# Submits the request to the NSX Manager
success = requests.get((requests_url), headers=myheaders, auth=(_user, _password), verify=False)
_data=success.content

#
# Opens a file for writing and saves the XML response to the file to be parsed further down.
_responsexml = open('%s' % _responsefile, 'w+')
_responsexml.write(success.text);

#
# Parse the xml file from above
_responsexml = open('%s' % _responsefile, 'r+')
#dom4 = parse(_responsexml)

#
# Close the XML response file
_responsexml.close()

#
# (DEBUGGING) Print the output of the parse XML file in a pretty format.
#print (dom4.toprettyxml())


import re
import sys
from xml.dom import minidom
doc = minidom.parse(_responsefile)



# Sets up column headers 
print("{0:17} {1:30} {2:16} {3:16}".format("ObjectID", "Name", "Protocol", "Port"))
print("-"*80)

# Loads xml document into memory using the application element
nodes = doc.getElementsByTagName('application')

# Iterates through each application element
for node in nodes:
	# clears the list
	test = [];
	# Gets the a objectId of the application  
	appObjectId = node.getElementsByTagName("objectId")[0]
	# Get the name of the application
	name = node.getElementsByTagName("name")[0]
	# Sets the list to start with the objectID
	test = [(appObjectId.firstChild.data)]
	# Appends the application name to the list
	test.append(name.firstChild.data);

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
				test.append(protocol.firstChild.data);
				
			else:
				# So if there is no element called applicationProtocol, append the string to the list
				test.append("no protocol")

			# Load the element called value
			port = element.getElementsByTagName("value")[0]
			
			# Check to see if the element contains a child
			if port.firstChild:
			
				# If it contains the value element then append the data to the list
				test.append(port.firstChild.data);
				
			else:
			
				# So if there is no element called value, append the string to the list
				test.append("no port value")
	else:
		# Will drop through to here if there is no element called "element". Some built in services 
		# seem to be structured like this and essentially have not protocol or port defined in NSX.
		# NOTE: These also seem to be marked as read-only services
		test.append("no protocol");
		test.append("no port");
	
	# loads the data in the "value" element (port/ports) into a variable to we can check it
	portcheck = test[3]

	# ------------------------------------------------------------------------------------------------------------------	
	#
	# This section of code checks for a port number within a range
	
	# sets up regular expression to look for ranges within a variable
	_re_range = re.compile(".*\,*[0-9]+\-[0-9]+")
	
	# runs the regex against the port variable in the list
	m = _re_range.match(portcheck)
	
	# if it finds a match it will do the following
	if m:
		# Splits the variable into 2
		rangechecklist = portcheck.split("-")
		# set the low integer port number
		l = int(rangechecklist[0])
		# set the high integer port number
		h = int(rangechecklist[1])
		# performs a check to see if the port exists between the low and high port numbers, and if it does
		# will print the data from the list
		if (l <= int(x) and h >= int(x)):
			print("{0:17} {1:30} {2:16} {3:16}".format(test[0], test[1], test[2], test[3]))
	#
	# ------------------------------------------------------------------------------------------------------------------

	# Checks to see if multiple ports are specified in the service
	if "," in portcheck:
		# If there are multiple ports, split them into a list
		portchecklist = portcheck.split(",")
		# Iterate through the list
		for y in portchecklist:
			# save the port as an integer
			_int_port = int(y)
			# runs the regex against the port variable in the list
			z = _re_range.match(y)
			if z:
				# Splits the variable into 2
				rangechecklist = portcheck.split("-")
				# set the low integer port number
				l = int(rangechecklist[0])
				# set the high integer port number
				h = int(rangechecklist[1])
				# performs a check to see if the port exists between the low and high port numbers, and if it does
				# will print the data from the list
				if (l <= int(x) and h >= int(x)):
					print("{0:17} {1:30} {2:16} {3:16}".format(test[0], test[1], test[2], test[3]))
			else:
				# If the integer variable is the same as the port number passed through as an argument, then print the whole line
				if _int_port == int(x):
					print("{0:17} {1:30} {2:16} {3:16}".format(test[0], test[1], test[2], test[3]))

	# Checks to see if the port is an exact match for applications with only a single port defined
	if x == portcheck:
		print("{0:17} {1:30} {2:16} {3:16}".format(test[0], test[1], test[2], test[3]))
exit()
