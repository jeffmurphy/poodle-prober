# POODLE Prober

Probe your poodle. Just to be safe.

Scan a netblock for SSLv3 enabled servers.

# Setup

```
# apt-get install python3-ipy
```

or, if that's not available

```
# apt-get install python3-pip
# pip3 install IPy
```

# Usage

```
sslv3check.py [-p port] -n <network/mask> [-t]
    -p port to connect to (default=443)
    -t check if SSLv3 is enabled and TLSv1 is not enabled
       otherwise just see if SSLv3 is enabled
```

Just look for anyone with SSLv3 turned on:

```
$ python3 sslv3check.py -n 10.0.1.0/24
10.0.1.1 SSLv3 [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:598)
10.0.1.2 SSLv3 timed out
10.0.1.3 SSLv3 timed out
10.0.1.4 SSLv3 enabled
10.0.1.5 SSLv3 enabled
```

Look for things with SSLv3 turned on and TLSv1 turned off:

```
$ python3 sslv3check.py -n 10.0.1.0/24 -t
10.0.1.1 SSLv3 [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:598) TLSv1 enabled
10.0.1.2 SSLv3 timed out TLSv1 timed out
10.0.1.3 SSLv3 timed out TLSv1 timed out
10.0.1.4 SSLv3 enabled TLSv1 not enabled
10.0.1.5 SSLv3 enabled TLSv1 enabled
```

Just check one host:

```
$ python3 sslv3check.py -n 10.0.1.1
10.0.1.1 SSLv3 [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:598)
```

# Props

To Kohster for the name and the "TLSv1 disabled" feature suggestion!
