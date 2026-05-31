from scapy.all import IP, ICMP, send
import time

target = "127.0.0.1"
print("Génération de trafic ICMP ...")
for _ in range(5):
    send(IP(dst=target)/ICMP(), verbose=0)
    time.sleep(0.5)
print("ICMP  est terminé")