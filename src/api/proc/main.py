import sys
import psycopg2

from flask import Flask
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/best_players', methods=['GET'])
def get_best_players():
    return [{
        "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
        "name": "Ronaldo",
        "country": "Portugal",
        "position": "Striker",
        "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
        "number": 7
    }]


@app.route('/api/athleteByName', methods=['GET'])
def getAthleteByName(name, id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute("SELECT unnest(CAST(XPATH('/athletes/atlethe[@name=\""+name+"\"]/@name', xml)AS TEXT)::text[]) AS nome, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name +
                   "\"]/sex/text()', xml)AS TEXT)::text[]) AS sexo, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name+"\"]/age/text()', xml)AS TEXT)::text[]) AS idade FROM xmldata where id="+id)
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data


# Consulta que conta quantas medalhas existem de cada tipo
@app.route('/api/groupByMedals', methods=['GET'])
def getGroupByMedals(id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/medal/text()', xml)as TEXT)::text[]) as medalhas, count(*) as contagem FROM xmldata where id="+id+" group by medalhas")
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data

# Consulta que conta quantos tipos de desportos existem


@app.route('/api/groupBySport', methods=['GET'])
def getGroupBySport(id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto, count(*) as contagem FROM xmldata where id="+id+" group by desporto")
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data


# Consulta que conta quantos atletas existem com aquele tipo de sexo(NESTE CASO CONTA QUANTOS ATLETAS EXISTEM DO SEXO MASCULINO E FEMININO)
@app.route('/api/groupBySex', methods=['GET'])
def getGroupBySex(id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/sex/text()', xml)as TEXT)::text[]) as sex, count(*) as contagem FROM xmldata where id=" +
                   id+" group by sex order by contagem asc")
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data

# Consulta que apresenta o tipo de desporto praticado através do nome de um determinado atleta


@app.route('/api/sportByName', methods=['GET'])
def getSportByName(name, id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto FROM xmldata where id="+id)
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data

# Consulta que apresenta o tipo de evento desportivo praticado através do nome de um determinado atleta


@app.route('/api/eventByName', methods=['GET'])
def getEventByName(name, id):
    connection = psycopg2.connect(
        host='db-rel2', database='is', user='is', password='is')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/event/text()', xml)as TEXT)::text[]) as evento FROM xmldata where id="+id)
    connection.commit()
    data = cursor.fetchall()

    print(len(data))
    print(type(data))
    return data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
