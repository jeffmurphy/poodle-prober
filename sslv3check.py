"""
setup:

apt-get install python3-pip
pip install IPy
python3 sslcheck.py 10.0.1.0/24

jcmurphy@buffalo.edu
"""
import socket, ssl, pprint, sys, IPy, getopt

def help(m=""):
	print("sslv3check.py [-p port,port,...] [-n <network/mask> OR -H hostname] [-t]")
	print("   -p port to connect to (default=443)")
	print("   -t check if SSLv3 is enabled and TLSv1 is not enabled")
	print("      otherwise just see if SSLv3 is enabled")
	print(m)
	sys.exit(2)

def print_results(host, port, sslv3, tlsv1):
	if tlsv1 is None:
		print("{0}:{1} SSLv3 {2}".format(str(host), port, sslv3))
		return

	if sslv3 == "enabled" and tlsv1 != "enabled":
		print("{0}:{1} SSLv3 enabled and TLSv1 not enabled".format(str(host), port))
	else:
		print("{0}:{1} SSLv3={2} TLSv1={3}".format(str(host), port, sslv3, tlsv1))

def main():
	port = "443"
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:n:H:t")
	except getopt.GetoptError:
		help()

	network = host = tlsv1 = None
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
		elif opt == '-H':
			host = arg
	
	if network == None and host == None:
		help("-n or -H required")

	if host is not None:
		for p in port.split(","):
			sslv3 = check_sslv3(host, p)
			if no_tlsv1 == True:
				tlsv1 = check_tls(host, p)
			print_results(host, p, sslv3, tlsv1)
		return


	ip = IPy.IP(network)

	for x in ip:
		if ip.prefixlen() != 32 and (ip.broadcast() == x or ip.net() == x):
			continue
		for p in port.split(","):
			sslv3 = check_sslv3(x, p)
			if no_tlsv1 == True:
				tlsv1 = check_tls(x, p)
			print_results(x, p, sslv3, tlsv1)


def check_tls(h, p):
	return check(h, p, ssl.PROTOCOL_TLSv1)

def check_sslv3(h, p):
	return check(h, p, ssl.PROTOCOL_SSLv3)

def check(h, p, ctx):
	context = ssl.SSLContext(ctx)
	context.verify_mode = ssl.CERT_NONE

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
