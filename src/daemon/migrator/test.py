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
    cursor.execute("INSERT INTO season (season) VALUES(%s)", (season,))
    connection.commit()

except OperationalError as err:
    print_psycopg2_exception(err)
