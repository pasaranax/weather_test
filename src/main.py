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
        data = Data(res.json())
        status = int(data.data["cod"])
        message = data.data.get("name") or data.data.get("message") or "error"
        self.compose(message, result=data, status=status, send=True)
        es.index("log", {
            "date": datetime.now(),
            "query": city,
            "result": data.data
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
