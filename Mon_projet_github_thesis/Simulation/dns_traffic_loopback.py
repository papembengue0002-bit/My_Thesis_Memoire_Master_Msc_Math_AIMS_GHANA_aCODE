from scapy.all import IP, UDP, DNS, DNSQR, sr1
import time

print("Génération de requêtes DNS sur loopback ...")
for domain in ["google.com", "example.com", "github.com"]:
    pkt = IP(dst="127.0.0.1") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))
    sr1(pkt, timeout=1, verbose=0)
    time.sleep(0.3)
print("DNS loopback terminé")