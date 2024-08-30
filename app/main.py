from fastapi import FastAPI, Request, Response, status
import geoip2.database
from geoip2.errors import AddressNotFoundError
import pathlib
import time

app = FastAPI()

BASEDIR = pathlib.Path(__file__).parent.resolve()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = str(process_time)
    return response


def read_ip(your_ip: str, reader: str):
    try:
        with geoip2.database.Reader(f"{BASEDIR}/data/{reader}/GeoLite2-{reader.title()}.mmdb") as r:
            if reader == 'city':
                response = r.city(your_ip)
            else:
                response = r.country(your_ip)
        return {
            "code": status.HTTP_200_OK,
            "data": response.raw
        }
    except ValueError as e:
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "ValueError": str(e)
        }
    except AddressNotFoundError as e:
        return {
            "code": status.HTTP_404_NOT_FOUND,
            "AddressNotFoundError": str(e)
        }


@app.get("/ip/{your_ip}")
async def read_item(your_ip: str, request: Request, response: Response):
    if your_ip == 'me':
        your_ip = request.client.host

    result = read_ip(your_ip, 'city')
    response.status_code = result['code']
    return result
