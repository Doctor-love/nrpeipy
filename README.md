nrpeipy
=======

A proof of concept script for use with SSH to execute commands the NRPEd way.

Usage
-----

```
$ ssh user@host users
USERS OK - 2 users currently logged in |users=2;5;8;0
$ echo $?
0
```

How it works
------------
When configured as a shell for a user, it loads files containing NRPE command configuration syntax (command[users]=/path/to/check_users --arg1 4.....) from a specified directory and makes them available for use.

Configuration
-------------

1. Create a dedicated user on your host
2. Add your monitoring system's public SSH key to the users authorized_keys file
3. Set the "configdir" variable in "nrpeipy.py" to your NRPE command configuration directory
4. Configure nrpeipy as a shell for the user (usermod -s /usr/bin/nrpeipy.py user)
5. Use a check plugin like "check_by_ssh" for the monitoring (check_by_ssh -H host -l user -i .ssh/id_rsa.pub -C users)
 
Recommendations
---------------
By default SSH allows a lot of things like port forwarding and similar - this can be disabled on a per key basis in the authorized_keys file:

```
no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAAB3Nza....... yoruser@monserver
```
