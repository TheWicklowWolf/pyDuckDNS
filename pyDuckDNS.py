import os
import time
import logging
import ipaddress
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()

app_name_text = os.path.basename(__file__).replace(".py", "")
release_version = os.environ.get("RELEASE_VERSION", "unknown")
logger.info(f"{'*' * 50}\n")
logger.info(f"{app_name_text} Version: {release_version}\n")
logger.info(f"{'*' * 50}")

api_endpoints = ["https://api.ipify.org", "http://wtfismyip.com/text"]
domains = os.environ.get("domains", "domainB,domainA")
token = os.environ.get("duckdns_token", "123")
refresh_interval = float(os.environ.get("refresh_interval", 600))


def get_public_ip(api_endpoint):
    try:
        ip = requests.get(api_endpoint).text.replace("\n", "")
        ipaddress.ip_address(ip)
        logger.info(f"Found IP Address: {ip} from {api_endpoint}")
        return ip.strip()
    except Exception as e:
        logger.error(f"Error getting public IP from {api_endpoint}, Error: {e}")
        return None


def update_duckdns(ip):
    try:
        url = f"https://www.duckdns.org/update?domains={domains}&token={token}&{'&ip=' + ip if ip else ''}&verbose=true"
        req = requests.get(url)
        if req.status_code == 200 and "OK" in req.content.decode():
            response_state, response_ip_v4, response_ip_v6, response_text = req.content.decode().split("\n")
            logger.info(f"Response: {response_state} -> {response_text} -> Domains: {domains} -> IP address: {response_ip_v4}")

        else:
            logger.error(f"Failed to update {domains} with IP address: {ip}")
            logger.error(req.status_code)
            logger.error(req.content)
            logger.error(req.headers)

    except Exception as e:
        logger.error(f"Error updating DuckDNS: {e}")


while True:
    logger.info("Getting IP Address")
    ip = next((ip for api in api_endpoints if (ip := get_public_ip(api)) is not None), None)
    if not ip:
        logger.warning("No valid IP Address Found, letting DuckDNS obtain it automatically")

    update_duckdns(ip)
    logger.info(f"Sleeping for {refresh_interval} seconds")
    time.sleep(refresh_interval)
