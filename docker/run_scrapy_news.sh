#!/bin/sh

# wait for PSQL server to start
sleep 10

# Comando para rodar o script.
su -m myuser -c "scrapy crawl articleg1"