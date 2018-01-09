#!/bin/sh

# wait for Redis and Mongo servers to start
sleep 10

# Comando para rodar o script.
su -m myuser -c "scrapy crawl articleg1"