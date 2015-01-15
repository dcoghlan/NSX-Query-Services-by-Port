# NSX-Query-Services-by-Port
A small script to query NSX for vSphere to find and display all the services with a particular port configured

You pass the following arguments to the script

      NSX Manager username
  
      NSX Manager password
  
      NSX Manager FQDN or IP address
  
      Port number you want to find
  

The script will look for any service configured with the specified port, even if the port specified is part of a range of ports.

Issues
  - If the service has both a static port & a range defined it will not be handled correclty. If someone wants to fix this logic for me, please do so.
