import json
import os

class JsonFile:
    def __init__(self, filename):
        # Asegurarse de que la carpeta jsonCrud existe
        self.folder = "jsonCrud"
        os.makedirs(self.folder, exist_ok=True)
        # Guardar el archivo en la carpeta jsonCrud
        self.filename = os.path.join(self.folder, filename)

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def read(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def find(self, atributo, buscado):
        try:
            with open(self.filename, 'r') as file:
                datas = json.load(file)
                data = [item for item in datas if item.get(atributo) == buscado]
        except FileNotFoundError:
            data = []
        return data
    
    def delete(self, atributo, valor):
        try:
            with open(self.filename, 'r') as file:
                datas = json.load(file)
            datas = [item for item in datas if item.get(atributo) != valor]
            self.save(datas)
        except FileNotFoundError:
            pass
