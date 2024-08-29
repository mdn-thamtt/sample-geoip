from fastapi import FastAPI
import geoip2.database
from geoip2.errors import AddressNotFoundError
import pathlib

app = FastAPI()


def read_ip(your_ip: str, reader: str):
    try:
        path = pathlib.Path(__file__).parent.resolve()
        with geoip2.database.Reader(f"{path}/data/{reader}/GeoLite2-{reader.title()}.mmdb") as r:
            if reader == 'city':
                response = r.city(your_ip)
            else:
                response = r.country(your_ip)
        return response.raw
    except ValueError as e:
        return {
            "error": str(e)
        }
    except AddressNotFoundError as e:
        return {
            "AddressNotFoundError": str(e)
        }


@app.get("/")
def index():
    return {"message": "Pong!"}


@app.get("/ip/{your_ip}")
def read_item(your_ip: str):
    reader = 'city'
    return read_ip(your_ip, reader)
