#NSX-Query-Services-by-Port
A small python script to query VMware NSX-v to find and display all the services with a particular port configured.

The script will look for any service configured with the specified port, even if the port specified is part of a range of ports.

If a status code other than 200 is returned, the script will log the XML response to a debug file and exit the script.

##Prerequisites
Requires the Requests libraby to be installed. Requests can be downloaded a from the following URL
http://docs.python-requests.org/en/latest/

##Usage
```
python nsx-query-services.py -h
```
Output:
```
usage: nsx-query-services.py [-h] [-u [user]] -n nsxmgr -p port [-r] [-d]

Queries NSX Manager for a list of services configured with a specific port

optional arguments:
  -h, --help  show this help message and exit
  -u [user]   OPTIONAL - NSX Manager username (default: admin)
  -n nsxmgr   NSX Manager hostname, FQDN or IP address
  -p port     TCP/UDP port number
  -r          Include port ranges in the output
  -d          Enable script debugging
```
##Examples
### Example 1
Run the following command to find all services configured with port 3389
```
python nsx-query-services.py -n nsxmgr-l-01a.corp.local -p 3389
```
Output:
```
ObjectID          Name                           Protocol    Port
----------------  -----------------------------  ----------  ---------------
application-163   Terminal Services (UDP)        UDP         3389
application-203   Terminal Services (TCP)        TCP         3389
application-157   RDP                            TCP         3389
```
###Example 2
Run the following command to find all services configured with port 3389, and any service with a port range which includes 3389
```
python nsx-query-services.py -n nsxmgr-l-01a.corp.local -p 3389 -r
```
Output:
```
ObjectID          Name                           Protocol    Port
----------------  -----------------------------  ----------  ---------------
application-32    Win - RPC, DCOM, EPM, DRSUAPI  UDP         1025-65535
application-36    Win 2003 - RPC, DCOM, EPM, DR  TCP         1025-5000
application-163   Terminal Services (UDP)        UDP         3389
application-147   Win - RPC, DCOM, EPM, DRSUAPI  TCP         1025-65535
application-203   Terminal Services (TCP)        TCP         3389
application-166   VMware-VDM2.x-Ephemeral        TCP         1024-65535
application-157   RDP                            TCP         3389
application-385   aac_6666                       TCP         1234,2345-3456,6666
```
