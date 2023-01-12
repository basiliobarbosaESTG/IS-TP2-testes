import csv


def converter(file_to_open, file_name):
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
        return """<restaurant index="%s">
           <name>%s</name>
           <location>
               <address>%s</address>
               <city>%s</city>
               <country>%s</country>
               <postalCode>%s</postalCode>
               <province>%s</province>
               <coordinates>
                   <latitude>%s</latitude>
                   <longitude>%s</longitude>
               </coordinates>
           </location>
           <websites>%s</websites>
       </restaurant>""" % (row[0], row[7].replace("&", "&amp;"), row[1].replace("&", "&amp;"), row[2], row[3], row[8], row[9], row[5], row[6], row[10].split(',', 1)[0].replace("&", "&amp;"))

    xmlData.write('\n'.join([convert_row(row) for row in data[1:]]))
    xmlData.write("\n" + '</csv_data>' + "\n")
    xmlData.close()
