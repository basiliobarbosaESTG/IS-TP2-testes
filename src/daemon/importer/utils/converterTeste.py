import csv


def converterTeste(file_to_open, file_name):
    f = open(file_to_open)

    csv_f = csv.reader(f)

    data = []
    xmlFile = file_name
    xmlData = open(xmlFile, 'w')
    for row in csv_f:
        data.append(row)
    f.close()

    xmlData.write('<?xml version="1.0"?>' + "\n")
    xmlData.write('<csv_data>' + "\n")
    # print (data[1:])

    def convert_row(row):
        return """<atlethe name="%s">
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
                <statsBySport>
                    <sport>%s</sport>
                    <event>%s</event>
                    <medal>%s</medal>
                </statsBySport>
            </competition>
        </atlethe>""" % (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])

    xmlData.write('\n'.join([convert_row(row) for row in data[1:]]))
    xmlData.write("\n" + '</csv_data>' + "\n")
    xmlData.close()
