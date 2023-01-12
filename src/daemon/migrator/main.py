import sys
import time

import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(
        host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(
        host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(
                host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(
                host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        resp = requests.get(
            url="http://api-entities:8080/api/provinces", params={})
        provinces = {x.get("province"): x.get("id") for x in resp.json()}
        query = """(with restaurants as (select unnest(xpath('//restaurant',xml)) as restaurants_in_city from imported_documents WHERE deleted='False')
                            select DISTINCT(xpath('//restaurant/location/province/text()',restaurants_in_city))[1]::text as Province
                            FROM restaurants
                            GROUP BY Province)"""
        xml_cursor.execute(query)
        for row in xml_cursor:
            if row[0] not in provinces.keys():
                x = row[0]
                resp = requests.post(
                    url="http://api-entities:8080/api/provinces/create", json={"province": x})
                resp = requests.get(
                    url="http://api-entities:8080/api/provinces", params={})
                provinces = {x.get("province"): x.get("id")
                             for x in resp.json()}

        respRest = requests.get(
            url="http://api-entities:8080/api/restaurants", params={})
        restaurants = {x.get("restid") for x in respRest.json()}
        query2 = """ with restaurants as (select unnest(xpath('//restaurant/name/..',xml)) as restaurants_with_name from imported_documents WHERE deleted='False')
                            select(xpath('//restaurant/@index',restaurants_with_name))[1]::text as restid,
							(xpath('//restaurant/name/text()',restaurants_with_name))[1]::text as name,
							(xpath('//address/text()',restaurants_with_name))[1]::text as address,
							(xpath('//city/text()',restaurants_with_name))[1]::text as city,
							(xpath('//country/text()',restaurants_with_name))[1]::text as country,
							(xpath('//postalCode/text()',restaurants_with_name))[1]::text as postalCode,
							(xpath('//province/text()',restaurants_with_name))[1]::text as province,
							(xpath('//latitude/text()',restaurants_with_name))[1]::text as latitude,
							(xpath('//longitude/text()',restaurants_with_name))[1]::text as longitude,
							(xpath('//websites/text()',restaurants_with_name))[1]::text as websites
                            FROM restaurants;"""
        xml_cursor.execute(query2)
        for row in xml_cursor:
            if row[0] not in restaurants:
                x = row[0]
                data = {
                    "restid": row[0],
                    "name": row[1],
                    "address": row[2],
                    "city": row[3],
                    "province": provinces.get(row[6]),
                    "latitude": row[7],
                    "longitude": row[8],
                    "websites": row[9],
                }
                url = "http://api-entities:8080/api/restaurants/create"
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, json=data)
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
