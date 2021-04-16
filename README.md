# ARP_Spoof
ARP spoofing is a type of attack in which a malicious actor sends falsified ARP (Address Resolution Protocol) messages over a local area network.
This results in the linking of an attacker's MAC address with the IP address of a legitimate computer or server on the network.

## Requirements:
You must enable packet forwarding using `root@kali:~$ echo 1 > /proc/sys/net/ipv4/ip_forwarding`

## Usage:
sudo python3 ARP_Spoof.py -t IP_OF_THE_VICTIM -g IP_OF_THE_GATEWAY

### Example:
sudo python3 ARP_Spoof.py -t 192.168.1.105 -g 192.168.1.1
