import asyncio
import time
import uuid
import psycopg2

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.to_xml_converter import CSVtoXMLConverter
from utils.converter import converter


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        # !TODO: once the conversion is done, we should updated the converted_documents tables
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")
        try:
            print("Connecting to DB to read XML file.")
            connection = psycopg2.connect(
                host='db-xml', database='is', user='is', password='is')
            cursor = connection.cursor()
            print("Connection successful.\nAtempting insertion.")
            with open(xml_path, 'r', encoding="utf8") as file:
                xml_string = file.read()

            cursor.execute("INSERT INTO converted_documents(src,file_size,dst) VALUES(%s,%s,%s)",
                           (csv_path, os.path.getsize(xml_path), xml_path))
            connection.commit()
            print("Dados inseridos com sucesso!")
        except:
            print("Erro na conexão à BD.")

        # !TODO: we should store the XML document into the imported_documents table

    async def get_converted_files(self):
        # !TODO: you should retrieve from the database the files that were already converted before
        result = []
        try:
            print("Connecting to DB to convert CSV into XML.")
            connection = psycopg2.connect(
                host='db-xml', database='is', user='is', password='is')
            cursor = connection.cursor()
            cursor.execute(
                "SELECT src FROM converted_documents WHERE deleted = false")
            for row in cursor:
                result.append(row[0])
        except:
            return ("Falhou no get converted files")
        finally:
            return [result]

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
