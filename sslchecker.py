import ssl
import socket
import datetime

def get_certificate_expiration_date(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            cert = sslsock.getpeercert()
            timestamp = cert['notAfter']
            expiration_date = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y %Z")
            return expiration_date

# Usage example
website = "gokalpmeric.com"
expiration_date = get_certificate_expiration_date(website)
print(f"The SSL certificate for {website} will expire on {expiration_date}")
