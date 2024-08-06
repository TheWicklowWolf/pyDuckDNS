![Build Status](https://github.com/TheWicklowWolf/pyDuckDNS/actions/workflows/main.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/thewicklowwolf/pyduckdns.svg)

DuckDNS IP Updater.

## Run using docker-compose

```yaml
services:
  pyduckdns:
    image: thewicklowwolf/pyduckdns:latest
    container_name: pyduckdns
    environment:
      - domains=abc123,xyz789
      - duckdns_token=1234567890
      - refresh_interval=600
    volumes:
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
```

---


https://hub.docker.com/r/thewicklowwolf/pyduckdns

