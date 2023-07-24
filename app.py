from flask import Flask, render_template, request
import ssl
import socket
import datetime
import threading
import schedule
import time
import certifi

app = Flask(__name__)

domains = []

def get_certificate_expiration_date(hostname):
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            cert = sslsock.getpeercert()
            timestamp = cert['notAfter']
            expiration_date = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y %Z")
            return expiration_date

def check_domain_expiry():
    global domains
    if domains:
        for domain in domains:
            expiration_date = get_certificate_expiration_date(domain['name'])
            domain['expiration_date'] = expiration_date

def schedule_check_domains():
    schedule.every(1).day.do(check_domain_expiry)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    global domains
    if request.method == "POST":
        domain_name = request.form.get("domain")
        if domain_name:
            domain_info = {
                "name": domain_name,
                "expiration_date": get_certificate_expiration_date(domain_name),
            }
            domains.append(domain_info)

    return render_template("index.html", domains=domains)

if __name__ == "__main__":
    threading.Thread(target=schedule_check_domains, daemon=True).start()
    app.run(debug=True)
