"""
setup:

apt-get install python3-pip
pip install IPy
python3 sslcheck.py 10.0.1.0/24

jcmurphy@buffalo.edu
"""
import socket, ssl, pprint, sys, IPy, getopt
port = 443

def help(m=""):
	print("sslv3check.py [-p port,port,...] -n <network/mask> [-t]")
	print("   -p port to connect to (default=443)")
	print("   -t check if SSLv3 is enabled and TLSv1 is not enabled")
	print("      otherwise just see if SSLv3 is enabled")
	print(m)
	sys.exit(2)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:n:t")
	except getopt.GetoptError:
		help()

	network = None
	no_tlsv1 = False

	for opt, arg in opts:
		if opt == '-h':
			help()
		elif opt == '-n':
			network = arg
		elif opt == '-p':
			port = arg
		elif opt == '-t':
			no_tlsv1 = True
	
	if network == None:
		help("-n required")

	ip = IPy.IP(network)
	for x in ip:
		for p in port.split(","):
			if ip.prefixlen() != 32 and (ip.broadcast() == x or ip.net() == x):
				continue
			sslv3 = check_sslv3(x, p)
			if no_tlsv1 == True:
				tlsv1 = check_tls(x, p)
				if sslv3 == "enabled" and tlsv1 != "enabled":
					print("{0}:{1} SSLv3 enabled and TLSv1 not enabled".format(str(x), p))
				else:
					print("{0}:{1} SSLv3={2} TLSv1={3}".format(str(x), p, sslv3, tlsv1))
			else:
				print("{0}:{1} SSLv3 {2}".format(str(x), p, sslv3))


def check_tls(h, p):
	return check(h, p, ssl.PROTOCOL_TLSv1)

def check_sslv3(h, p):
	return check(h, p, ssl.PROTOCOL_SSLv3)

def check(h, p, ctx):
	context = ssl.SSLContext(ctx)
	context.verify_mode = ssl.CERT_NONE
	context.check_hostname = False
	context.load_default_certs()

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		ssl_sock = context.wrap_socket(s, server_hostname=str(h), do_handshake_on_connect=True)
		ssl_sock.connect((str(h), int(p)))
		ssl_sock.close()
		return "enabled"
	except Exception as e:
		return str(e)

if __name__ == "__main__":
	main()
