#NSX-Query-Services-by-Port
A small python script to query NSX for vSphere to find and display all the services with a particular port configured.

The script will look for any service configured with the specified port, even if the port specified is part of a range of ports.

##Prerequisites
Requires the Requests libraby to be installed. Requests can be downloaded a from the following URL
http://docs.python-requests.org/en/latest/

You pass the following arguments to the script
* NSX Manager username
* NSX Manager password
* NSX Manager FQDN or IP address
* Port number you want to find
An example would be as follows
```
python nsx-query-services.py admin defaultpw nsxmgr-l-01a.corp.local 3389
```
You will also need to update the API URL with the DC managed object refence id. My one in my lab is "datacenter-2" so update it to suit your environment.

##Issues
* If the service has both a static port & a range defined it will not be handled correclty. If someone wants to fix this logic for me, please do so.
* Within the URL for the API call I have hard coded the vSphere data center managed object reference id. This needs to be pulled out into a variable, but not sure if it needs to be passed through as an argument or not.
