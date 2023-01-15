import sys
import time

import psycopg2
from psycopg2 import OperationalError
import requests

try:
    print("Connecting to DB to read and insert XML file.")
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()
    season = 'teste'
    # cursor.execute("INSERT INTO season (season) VALUES(%s)", (season,))
    # cursor.execute("""INSERT INTO atlethe(name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)',4326))""",
    #               (atlethe.get("name"), atlethe.get("sex"), atlethe.get("age"), atlethe.get("height"), atlethe.get("weight"), atlethe.get("team"), atlethe.get("noc"), atlethe.get("games"), atlethe.get("year"), atlethe.get("season"), atlethe.get("city"), atlethe.get("lat"), atlethe.get("lon"), atlethe.get("sport"), atlethe.get("event"), atlethe.get("medal"), longitude, latitude))
    cursor.execute("INSERT INTO atlethe(name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom) VALUES ('name', 'sex', 'age', 'height', 'weight', 'team', 'noc', 'games', 'year', 'season', 'city', 'lat', 'lon', 'sport', 'event', 'medal', null)")
    connection.commit()

except OperationalError as err:
    print_psycopg2_exception(err)
