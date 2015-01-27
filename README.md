#NSX-Query-Services-by-Port
A small python script to query VMware NSX-v to find and display all the services with a particular port configured.

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
You will also need to update the _dcmoref variable with the DC managed object refence id. My one in my lab is "datacenter-2" so update it to suit your environment.

##Issues
* If the service has both a static port & a range defined it will not be handled correclty. If someone wants to fix this logic for me, please do so.