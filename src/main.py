from datetime import datetime

import requests
from elasticsearch import Elasticsearch
from microservice import BasicHandler, Data, check
from microservice import Server

import cfg


class WeatherHandler(BasicHandler):
    cache_method = "all"
    cache_lifetime = 60

    @check(anonymous=True)
    async def get(self, me, city):
        res = requests.get(cfg.app.owm_url.format(city=city, api_key=cfg.app.owm_api_key), timeout=5)
        data = res.json()
        if data.get("main"):
            temperature = data["main"]["temp"] - 273.15  # to celsius
            self.compose(
                "Temperature",
                result=Data({
                    "temperature": temperature
                }),
                send=True
            )
        else:
            self.compose(error=data["message"], status=int(data["cod"]), send=True)
        es.index("log", {
            "date": datetime.now(),
            "query": city,
            "result": data
        })


routes = [
    (r"weather/([\w\s-]+)", {1: WeatherHandler})
]

es = Elasticsearch([cfg.app.elastic_host])
server = Server(routes)

if __name__ == '__main__':
    if not es.indices.exists(index="log"):
        es.indices.create("log")
    server.run()
