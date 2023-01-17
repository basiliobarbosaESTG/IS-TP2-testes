import sys

from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


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


def getAthleteByName(name, id):  # recebe como parametros: o id e o nome
    try:
        cursor.execute("SELECT unnest(CAST(XPATH('/athletes/atlethe[@name=\""+name+"\"]/@name', xml)AS TEXT)::text[]) AS nome, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name +
                       "\"]/sex/text()', xml)AS TEXT)::text[]) AS sexo, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name+"\"]/age/text()', xml)AS TEXT)::text[]) AS idade FROM xmldata where id="+id)
        # cursor.execute("SELECT unnest(xpath('/athletes/atlethe[@name=\""+name+"\"]/sex/text()', xml)) AS sexo FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        # print(type(result[0]))
        print(type(result))
        # Type serve para ver o tipo de dado da variavel
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))

# Consulta que conta quantas medalhas existem de cada tipo


def getGroupByMedals(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/medal/text()', xml)as TEXT)::text[]) as medalhas, count(*) as contagem FROM xmldata where id="+id+" group by medalhas")
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))

# Consulta que conta quantos tipos de desportos existem


def getGroupBySport(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto, count(*) as contagem FROM xmldata where id="+id+" group by desporto")
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))

# Consulta que conta quantos atletas existem com aquele tipo de sexo(NESTE CASO CONTA QUANTOS ATLETAS EXISTEM DO SEXO MASCULINO E FEMININO)


def getGroupBySex(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/sex/text()', xml)as TEXT)::text[]) as sex, count(*) as contagem FROM xmldata where id=" +
                       id+" group by sex order by contagem asc")
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))

# Consulta que apresenta o tipo de desporto praticado através do nome de um determinado atleta


def getSportByName(name, id):
    try:
        cursor.execute(
            "SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))

# Consulta que apresenta o tipo de evento desportivo praticado através do nome de um determinado atleta


def getEventByName(name, id):
    try:
        cursor.execute(
            "SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/event/text()', xml)as TEXT)::text[]) as evento FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return (str(error))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
