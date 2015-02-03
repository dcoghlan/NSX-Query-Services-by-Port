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

##Example
Run the following command to find all services configured with port 3389
```
python nsx-query-services.py admin defaultpw nsxmgr-l-01a.corp.local 3389
```
A sample output would be as follows
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
