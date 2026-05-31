from scapy.all import ARP, Ether, srp
import time

target = "127.0.0.1"
print("Génératio de trafic ARP .....")
for _ in range(5):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target)
    srp(pkt, timeout=1, verbose=0)
    time.sleep(0.5)
print("ARP est terminé")