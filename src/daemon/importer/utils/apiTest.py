import requests

class Coordenates:
        def getCoordenates(self, city):
                #pedido HTTPS - endpoit
                response = requests.get(f"https://nominatim.openstreetmap.org/search?city={city}&format=json") #ou /json  Lisbon

                #converte objetos python para strings JSON
                data = response.json()
                #print(type(data))

                print(f"A cidade e: {city}")
                lat = data[0]['lat']
                lon = data[0]['lon']
                #print(data[0]['lat'])
                #print(data[0]['lon'])
                return lat, lon