from typing import Union
from fastapi import FastAPI
import requests
import ipaddress

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Pong!"}


@app.get("/ip/{your_ip}")
def read_item(your_ip: str):
    try:
        ipaddress.IPv4Network(your_ip)
        requests.put(f"http://es01:9200/user_ip/_doc/{your_ip}?pipeline=geoip&pretty", json = {"ip": your_ip})
        r = requests.get(f"http://es01:9200/user_ip/_doc/{your_ip}?pretty")
        return r.json()['_source']

    except ValueError as e:
        return {
            "error": str(e)
        }
