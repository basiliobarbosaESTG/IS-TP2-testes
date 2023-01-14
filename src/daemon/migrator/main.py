import sys
import time

import psycopg2
from psycopg2 import OperationalError
import requests

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
        host='db-xml2', database='is', user='is', password='is')
    db_dst = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(
                host='db-xml2', database='is', user='is', password='is')
            db_dst = psycopg2.connect(
                host='db-rel2', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        xml_cursor = db_org.cursor()
        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        resp = requests.get(
            url="http://api-entities2:8080/api/season", params={})
        # supostamente vai buscar os dados da tag season e o respetivo id
        seasons = {x.get("season")  # : x.get("id")
                   for x in resp.json()}
        query = """(with atlethes as (select unnest(xpath('//atlethe',xml)) as atlethes from imported_documents)
                            select DISTINCT(xpath('//atlethe/competition/season/text()',atlethes))[1]::text as Season
                            FROM atlethes
                            GROUP BY Season)"""
        xml_cursor.execute(query)

        print(seasons)
        for row in xml_cursor:
            # row[0].replace(" ", "")
            print(row[0])
            print(row[0].split())

            # mykeys = events.keys()
            # type(mykeys)
            # mylist = list(mykeys)
            # print(mylist)
            if row[0] not in seasons.keys():
                x = row[0]
                # print(x)
                print(x.split())
                resp = requests.post(
                    url="http://api-entities2:8080/api/seasons/create", json={"season": x})
                resp = requests.get(
                    url="http://api-entities2:8080/api/seasons", params={})
                seasons = {x.get("season")
                           for x in resp.json()}  # : x.get("id")

        # respRest = requests.get(
        #    url="http://api-entities2:8080/api/atlethes", params={})
        # atlethes = {x.get("id") for x in respRest.json()}
        # query2 = """ with atlethes as (select unnest(xpath('//atlethe/sex/..',xml)) as atlethes_with_sex from imported_documents)
        #                    select(xpath('//atlethe/@name',atlethes_with_sex))[1]::text as name,
                # (xpath('//atlethe/sex/text()',atlethes_with_sex))[1]::text as sex,
        #                    (xpath('//atlethe/age/text()',atlethes_with_sex))[1]::text as age,
        #                    (xpath('//atlethe/height/text()',atlethes_with_sex))[1]::text as height,
        #                    (xpath('//atlethe/weight/text()',atlethes_with_sex))[1]::text as weight,
        #                    (xpath('//atlethe/country/team/text()',atlethes_with_sex))[1]::text as team,
        #                    (xpath('//atlethe/country/noc/text()',atlethes_with_sex))[1]::text as noc,
         #                   (xpath('//atlethe/competition/games/text()',atlethes_with_sex))[1]::text as games,
          #                  (xpath('//atlethe/competition/year/text()',atlethes_with_sex))[1]::text as year,
           #                 (xpath('//atlethe/competition/season/text()',atlethes_with_sex))[1]::text as season,
            #                (xpath('//atlethe/competition/city/text()',atlethes_with_sex))[1]::text as city,
             #               (xpath('//atlethe/competition/coordenates/lat/text()',atlethes_with_sex))[1]::text as lat,
              #              (xpath('//atlethe/competition/coordenates/lon/text()',atlethes_with_sex))[1]::text as lon,
               #             (xpath('//atlethe/competition/statsBySport/sport/text()',atlethes_with_sex))[1]::text as sport,
                #            (xpath('//atlethe/competition/statsBySport/event/text()',atlethes_with_sex))[1]::text as event,
                #           (xpath('//atlethe/competition/statsBySport/medal/text()',atlethes_with_sex))[1]::text as medal
                #          FROM atlethes;"""
        # xml_cursor.execute(query2)
        # for row in xml_cursor:  # nome das colunas do xml
        #    if row[0] not in atlethes:
        #        x = row[0]
        #        data = {
        #            "name": row[0],
        #            "sex": row[1],
        #            "age": row[2],
        #            "height": row[3],
        #            "weight": row[4],
        #            "team": row[5],
        #            "noc": row[6],
        #            "games": row[7],
        #            "year": row[8],
         #           "season": row[9],
         #           "city": row[10],
            #        "lat": row[11],
           #         "lon": row[12],
          #          "sport": row[13],
         #           "event": events.get(row[14]),
         #           "medal": row[15]
         #       }
         #       url = "http://api-entities2:8080/api/atlethes/create"
         #       headers = {"Content-Type": "application/json"}
         #       response = requests.post(url, headers=headers, json=data)
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)

# TESTES

# d1[1, row[0]]
        # print(d1)

        # a_dict = {}
        # a_dict[row[0]] = 'example value'
        # print(a_dict)  # 👉️ {(7, 49): 'example value'}
        # print(a_dict[row[0]])

        # print("Index with a tuple")
        # d1[(1, "a")] = "tuple"
        # print("New dictionary contents")
        # print("Key", ' : ', "Value")
        # for x in d1.keys():
        #    print x, ' : ', d1[x]
        # ""  # Print blank line
        # print(row[0].get())


# TESTES 2
        # old_dict = ''
        # new_dict = {value: key for (
        #    key, value) in old_dict.split}  # .items()
        # print(new_dict)

# SOLUCAO EVENT TROCA PARA SEASON
# NAO CONSEGUIMOS CORRIGIR O ERRO DOS ESPAÇOS DAS KEYS
