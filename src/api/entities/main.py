import sys
import psycopg2

from flask import Flask, jsonify, request
from entities.event import Event
from entities.atlethe import Atlethe
from entities import Team

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
# events = [
# ]
events = [
    {
        "event": "basketball"
    }
]


def connect_db_rel():
    db_access = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    return db_access.cursor()


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/event/', methods=['GET'])
def get_events():
    # rel_cursor = connect_db_rel()
    # rel_cursor.execute("SELECT id, event FROM event")
    # return [Event(row[1]).to_json() for row in rel_cursor]
    return events


@app.route('/api/event/create', methods=['POST'])
def post_events():
    data = request.get_json()
    event_name = str(data.get('event'))
    rel_cursor = connect_db_rel()
    rel_cursor.cursor()
    try:
        rel_cursor.execute(
            "INSERT INTO event (event) VALUES(%s)", (event_name,))
        connect_db_rel().commit()
        return jsonify({'status': 'success', 'your_data': event_name}), 201
    except:
        pass


@app.route('/api/atlethe/', methods=['GET'])
def get_atlethes():
    rel_cursor = connect_db_rel()
    rel_cursor.execute(
        "SELECT name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom, id FROM event")
    return [Atlethe(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]).to_json() for row in rel_cursor]


@app.route('/api/atlethe/create', methods=['POST'])
def post_atlethes():
    atlethe = request.get_json()
    rel_cursor = connect_db_rel()
    rel_cursor.cursor()
    # meter point direito, tirar plicas
    lat = float(atlethe.get("lat", None).replace("'", ""))
    lon = float(atlethe.get("lon", None).replace("'", ""))
    try:
        rel_cursor.execute("""INSERT INTO atlethe(name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom,) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)',4326))""",
                           (atlethe.get("name"), atlethe.get("sex"), atlethe.get("age"), atlethe.get("height"), atlethe.get("weight"), atlethe.get("team"), atlethe.get("noc"), atlethe.get("games"), atlethe.get("year"), atlethe.get("season"), atlethe.get("city"), atlethe.get("lat"), atlethe.get("lon"), atlethe.get("sport"), atlethe.get("event"), atlethe.get("medal"), lat, lon))
        connect_db_rel().commit()
        return jsonify(message='Restaurant created successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400


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
