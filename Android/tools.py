import sqlite3
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import requests, json

class StationInfo():
    def __init__(self, stations):
        self.data = stations
        self.api = "https://api.prix-carburants.2aaz.fr/station/"
    def get_gazole_price(self):
        try:
            array = []
            for id in self.data:
                url = self.api+id[0]
                get_url = requests.get(url,verify=False)
                data = json.loads(get_url.content)
                nom = data['name']
                prix = data['Fuels'][0]['Price']['value']
                row= (nom,prix)
                array.append(row)
            return array
        except Exception as e:
            print(e)
    def get_station_liste(self):
        try:
            array = []
            for id in self.data:
                url = self.api + id[0]
                get_url = requests.get(url, verify=False)
                data = json.loads(get_url.content)
                nom = data['name']
                numero = str(id[0])
                row= (nom,numero)
                array.append(row)
            return array
        except Exception as e:
            print(e)

class DatabaseHelper():
    def __init__(self):
        self.name = "Stations"

    def initiate_db(self):
        conn = sqlite3.connect('stations.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists stations(ID VARCHAR(160))""")
        conn.commit()
        conn.close()
    def select_stations(self):
        conn = sqlite3.connect('stations.db')
        data = []
        c = conn.cursor()
        c.execute("""SELECT * FROM stations """)
        rows = c.fetchall()
        for row in rows:
            data.append(row)
        c.close()
        return data

    def add_stations_id(self, id):
        try:
            value = [str(id)]
            conn = sqlite3.connect('stations.db')
            c = conn.cursor()
            sql = ''' INSERT INTO stations(ID) VALUES (?)'''
            c.execute(sql, value)
            conn.commit()
            c.close()
        except Exception as e:
            print (e)

    def delete_stations(self, id):
        try:
            conn = sqlite3.connect('stations.db')
            c = conn.cursor()
            for i in id:
                value = [str(i)]
                sql = ''' DELETE FROM stations WHERE ID=(?)'''
                c.execute(sql, value)
            conn.commit()
            c.close()
        except Exception as e:
            print(e)

