import sys
import psycopg2

from flask import Flask, request

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/markerAtlethe/', methods=['GET'])
def get_markers_atlethes():

    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    query = f"SELECT (SELECT jsonb_build_object('type', 'Feature','geometry', ST_AsGeoJSON(atlethe.geom)::jsonb,'properties', to_jsonb( t.* )  - 'geom') AS json FROM (VALUES (atlethe.id, atlethe.name, atlethe.city, 'POINT(1 1)'::geometry)) AS t(id, name, city, geom)) FROM atlethe;"

    cursor.execute(query)
    connection.commit()
    data = cursor.fetchall()

    connection.close()
    return data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
