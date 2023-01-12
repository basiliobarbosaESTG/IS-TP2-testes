from utils.athlete_events import athlete_events
import csv


class converterXML:
    def __init__(self, file1, file2):
        self.athlete_events_file = file1
        self.name_file = file2

    # Função que faz a conversão do ficheiro lendo e guardando os dados do CSV para um ficheiro XML
    def convert(self):
        try:
            def saveCSV(data):
                info = []
                for row in data:
                    info.append(row)
                return info
            # abertura em mode de leitura do ficheiro CSV
            with open(self.athlete_events_file, 'r', encoding="UTF8") as file:
                reader = csv.reader(file, delimiter=',')
                next(reader)
                athletes = saveCSV(reader)

            # Escrever ficheiro xml que fica gravado na pasta Output
            with open("Output\\"+self.name_file+".xml", "w", encoding="UTF8") as file:
                file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                file.write("\t<athletes>\n")
                for a in athletes:
                    athlete = athlete_events(a)
                    file.write(athlete.convert_toXML())
                file.write("\n\t</athletes>\n")

        except (Exception) as error:
            print("Erro: ", error)
