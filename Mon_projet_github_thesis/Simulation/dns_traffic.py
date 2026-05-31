import socket

domains = ["google.com", "example.com","kaggle.com", "github.com","wikipedia.com"]
print("Génération de trafic DNS ...")
for dom in domains:
    try:
        socket.getaddrinfo(dom, None)
        print(f"  Résolu : {dom}")
    except Exception as e:
        print(f"  Échec {dom} : {e}")
print("DNS is finish")