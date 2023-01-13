import uuid
from datetime import datetime


class Event:
    def __init__(self, name, sex, age, height, weight, team, noc, games, year, season, city, lat, lon, sport, event, medal, geom, id=None, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight
        self.team = team
        self.noc = noc
        self.games = games
        self.year = year
        self.season = season
        self.city = city
        self.lat = lat
        self.lon = lon
        self.sport = sport
        self.event = event
        self.medal = medal
        self.geom = geom
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "team": self.team,
            "noc": self.noc,
            "games": self.games,
            "year": self.year,
            "season": self.season,
            "city": self.city,
            "lan": self.lat,
            "lon": self.lon,
            "sport": self.sport,
            "event": self.event,
            "medal": self.medal,
            "geom": self.geom
        }
