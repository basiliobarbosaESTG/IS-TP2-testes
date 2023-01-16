import sys
import psycopg2

from flask import Flask, jsonify, request
from flask_cors import CORS
from entities.season import Season
from entities.atlethe import Atlethe
from entities import Team

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access


def connect_db_rel():
    db_access = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    return db_access.cursor()


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/season/', methods=['GET'])
def get_seasons():
    rel_cursor = connect_db_rel()
    rel_cursor.execute("SELECT id, season FROM season")
    return [Season(row[1]).to_json() for row in rel_cursor]


@app.route('/api/season/create', methods=['POST'])
def post_seasons():
    data = request.get_json()
    season = str(data.get('season'))
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO season (season) VALUES(%s)", (season,))
        connection.commit()
        return jsonify({'status': 'success', 'your_data': season}), 201
    except:
        pass


@app.route('/api/atlethe/', methods=['GET'])
def get_atlethes():
    rel_cursor = connect_db_rel()
    rel_cursor.execute(
        "SELECT name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom, id FROM atlethe")
    return [Atlethe(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]).to_json() for row in rel_cursor]


@app.route('/api/atlethe/create', methods=['POST'])
def post_atlethes():
    data = request.get_json()
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    query = f"INSERT INTO atlethe(name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom) VALUES ('{data['name']}', '{data['sex']}', '{data['age']}', '{data['height']}', '{data['weight']}', '{data['team']}', '{data['noc']}', '{data['games']}', '{data['year']}', '{data['season']}', '{data['city']}', '{data['lat']}', '{data['lon']}', '{data['sport']}', '{data['event']}', '{data['medal']}', ST_GeomFromText('POINT({data['lon']}  {data['lat']})', 4326))"
    cursor.execute(query)
    connection.commit()
    return data


# @app.route('/api/teams/', methods=['GET'])
# def get_teams():
#    return jsonify([team.__dict__ for team in teams])
# @app.route('/api/teams/', methods=['POST'])
# def create_team():
#    data = request.get_json()
#    team = Team(name=data['name'])
#    teams.append(team)
#    return jsonify(team.__dict__), 201
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
