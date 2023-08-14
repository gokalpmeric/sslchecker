from flask import Flask, render_template, request
import ssl
import socket
import datetime
import threading
import schedule
import time
import certifi
import json
import os

app = Flask(__name__)

DATA_FILE = '/app/data/domains.json'

# Load domains from file if exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        domains = json.load(file)
else:
    domains = []

def get_certificate_expiration_date(hostname):
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                cert = sslsock.getpeercert()
                timestamp = cert['notAfter']
                expiration_date = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y %Z")
                return expiration_date
    except Exception as e:
        print(f"An error occurred while retrieving the certificate for {hostname}: {str(e)}")
        return None

def calculate_days_left(expiration_date):
    return (expiration_date - datetime.datetime.now()).days

def check_domain_expiry():
    global domains
    if domains:
        for domain in domains:
            expiration_date = get_certificate_expiration_date(domain['name'])
            if expiration_date:
                days_left = calculate_days_left(expiration_date)
                domain['expiration_date'] = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
                domain['days_left'] = days_left

        # Save updates to file
        with open(DATA_FILE, 'w') as file:
            json.dump(domains, file)

def schedule_check_domains():
    schedule.every(1).hour.do(check_domain_expiry)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    global domains
    if request.method == "POST":
        domain_name = request.form.get("domain")
        if domain_name:
            expiration_date = get_certificate_expiration_date(domain_name)
            if expiration_date:
                days_left = calculate_days_left(expiration_date)
                domain_info = {
                    "name": domain_name,
                    "expiration_date": expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "days_left": days_left,
                }

                existing_domain = next((d for d in domains if d['name'] == domain_name), None)
                if existing_domain:
                    existing_domain.update(domain_info)
                else:
                    domains.append(domain_info)

                # Save updates to file
                with open(DATA_FILE, 'w') as file:
                    json.dump(domains, file)

    return render_template("index.html", domains=domains)

if __name__ == "__main__":
    threading.Thread(target=schedule_check_domains, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
