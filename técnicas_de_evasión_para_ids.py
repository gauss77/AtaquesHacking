# -*- coding: utf-8 -*-
"""Técnicas de evasión para IDS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iZfrRedxWh5W18pRzIeQzhkoeRavOadC
"""

#3.1.1. Spoofing de Tráfico
from scapy.all import *

def spoof_traffic(target_ip, spoofed_ip):
    packet = IP(src=spoofed_ip, dst=target_ip) / ICMP()
    send(packet, verbose=0)

# Uso de la función
spoof_traffic("192.168.1.100", "10.0.0.2")

#Explicación:
"""Este script utiliza Scapy para construir un paquete ICMP con una dirección IP de origen falsificada y lo envía al destino.
La intención es eludir la detección de IDS al cambiar la dirección IP de origen."""

#3.2.1. Exploración de Puertos No Convencionales

import nmap

def scan_ports(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-p 12345,23456,34567')

    # Imprimir resultados
    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"Open ports: {nm[host]['tcp'].keys()}")

# Uso de la función
scan_ports("192.168.1.100")

#Explicación:
"""Este script utiliza la biblioteca nmap para realizar un escaneo de puertos específicos en el objetivo,
incluyendo puertos no convencionales. El objetivo es eludir la detección de firewall al no utilizar puertos comunes. """

#3.2.2. Uso de Túneles SSH o VPN

import paramiko

def establish_ssh_tunnel(target_ip, ssh_username, ssh_private_key):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conexión al servidor SSH para establecer un túnel
    client.connect(target_ip, username=ssh_username, key_filename=ssh_private_key, port=22, look_for_keys=False, allow_agent=False)

    # Lógica adicional para el tráfico a través del túnel SSH

    # Cierre de la conexión SSH
    client.close()

# Uso de la función
establish_ssh_tunnel("192.168.1.100", "user", "private_key.pem")

#Explicación:
""" Este script utiliza la biblioteca Paramiko para establecer una conexión SSH y crear un túnel a través del cual
se puede enviar tráfico malicioso al objetivo, eludiendo posibles restricciones del firewall. """

#3.3.1. Detección y Evitación de Honeypots (Python)
import scapy.all as scapy

def detect_honeypot(target_ip):
    # Implementar lógica para analizar patrones de tráfico y detectar honeypots
    # ...

# Uso de la función
detect_honeypot("192.168.1.100")

#Explicación:
"""Explicación:
Este ejemplo simplificado utiliza Scapy para analizar patrones de tráfico y detectar características
que podrían indicar la presencia de un honeypot. Basado en la detección, un atacante podría decidir
evitar la interacción con el honeypot. """

#3.3.2. Simulación de Comportamiento Legítimo (Python)

import time

def simulate_legitimate_behavior(target_ip):
    # Implementar lógica para simular el comportamiento de usuarios y sistemas legítimos
    # ...

# Uso de la función
simulate_legitimate_behavior("192.168.1.100")