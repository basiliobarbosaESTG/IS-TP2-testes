from utils.apiTest import Coordenates


class athlete_events(object):
    # default constructor
    def __init__(self, line_csv):
        self.coordenates = Coordenates()
        self.name = line_csv[1]
        self.sex = line_csv[2]
        self.age = line_csv[3]
        self.height = line_csv[4]
        self.weight = line_csv[5]
        self.team = line_csv[6]
        self.noc = line_csv[7]
        self.games = line_csv[8]
        self.year = line_csv[9]
        self.season = line_csv[10]
        self.city = line_csv[11]
        self.sport = line_csv[12]
        self.event = line_csv[13]
        self.medal = line_csv[14]

# Escreve os dados de um atleta
    def convert_toXML(self):
        # variaveis onde guardamos as coordenadas da latitude e da longitude das cidades que se encontram no ficheiro XML
        lat, lon = self.coordenates.getCoordenates(self.city)
        print(lat)
        print(lon)
        return """
        <atlethe name="%s">
            <sex>%s</sex>
            <age>%s</age>
            <height>%s</height>
            <weight>%s</weight>
            <country>
                <team>%s</team>
                <noc>%s</noc>
            </country>
            <competition>
                <games>%s</games>
                <year>%s</year>
                <season>%s</season>
                <city>%s</city>
                <coordenates>
                    <lat>%s</lat>
                    <lon>%s</lon>
                </coordenates>
                <statsBySport>
                    <sport>%s</sport>
                    <event>%s</event>
                    <medal>%s</medal>
                </statsBySport>
            </competition>
        </atlethe>""" % (self.name, self.sex, self.age, self.height, self.weight, self.team, self.noc, self.games, self.year, self.season, self.city, lat, lon, self.sport, self.event, self.medal)
