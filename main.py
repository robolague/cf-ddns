import requests
import json
import ipaddress
import os

baseid= os.environ['BASEID']
zone = os.environ['ZONE']
auth_email = os.environ['AUTH_EMAIL']
auth_key =  os.environ['AUTH_KEY']
bearer = os.environ['BEARER']


cloudflareurl = "https://api.cloudflare.com/client/v4/zones/" + zone + "/dns_records"
cfheaders = {
    'X-Auth-Email': auth_email,
    'X-Auth-Key': auth_key,
    'Authorization': bearer,
    'Content-Type': 'application/json'
}

def update_ddns(domain, id, ipaddr):
    payload = json.dumps({
        "type": "A",
        "name": domain,
        "content": ipaddr,
        "ttl": 1,
        "proxied": True
    })
    response = requests.request("PUT", cloudflareurl + "/" + id, headers=cfheaders, data=payload)
    print(response.text)

def new_ddns(domain, ipaddr):
    payload = json.dumps({
        "type": "A",
        "name": domain,
        "content": ipaddr,
        "ttl": 1,
        "proxied": True
    })
    response = requests.request("POST", cloudflareurl + "/", headers=cfheaders, data=payload)
    print(response.text)

def get_domain_id(domain):
    payload = {"match": "all","name": domain}
    response = requests.request("GET", cloudflareurl, headers=cfheaders, params=payload)
    data = json.loads(response.text)
    try:
        data_inner = data['result'][0]['id']
        return data_inner
    except IndexError:
        return None

def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        print("IP address {} is not valid".format(address))
        return False

def get_public_ip():
    ip = requests.request("GET","http://ipinfo.io/ip")
    if validate_ip_address(ip.text) == True:
        return ip.text
    else:
        raise Error("Not a valid IP")

if __name__ == "__main__":
    current_ip = get_public_ip()
    update_ddns("", baseid, current_ip)
    with open("/etc/ddupdate/dnslist") as file:
        lines = [line.rstrip() for line in file]
    for entry in lines:
        id = get_domain_id(entry)
        if id is not None:
            update_ddns(entry, id, current_ip)
        else:
            new_ddns(entry, current_ip)