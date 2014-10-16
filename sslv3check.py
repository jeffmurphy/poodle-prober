"""
setup:

apt-get install python3-pip
pip install IPy
python3 sslcheck.py 10.0.1.0/24

jcmurphy@buffalo.edu
"""
import socket, ssl, pprint, sys, IPy

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False
context.load_default_certs()

ip = IPy.IP(sys.argv[1])
for x in ip:
        if ip.broadcast() == x or ip.net() == x:
                continue
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                ssl_sock = context.wrap_socket(s, server_hostname=str(x), do_handshake_on_connect=True)
                ssl_sock.connect((str(x), 443))
                #pprint.pprint(ssl_sock.getpeercert())
                ssl_sock.close()
                print("{0} SSLv3 enabled".format(str(x)))
        except Exception as e:
                print("{0} {1}".format(str(x), e))
