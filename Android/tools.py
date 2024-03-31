import sqlite3
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import requests, json
class DataTable(MDDataTable):
    def __init__(self,center_x,center_y,size,data):
        self.centerx = center_x
        self.centery = center_y
        self.size = size
        # self.column_data = column
        self.data = data

    def get_datatable(self):
        Table = MDDataTable()
        Table.pos_hint = {"center_x": self.centerx, "center_y": self.centery}
        Table.size_hint = self.size
        Table.column_data = [("Nom", dp(30)), ("Prix",dp(30))]
        Table.row_data = [("station 1", "toto"),("tata", "titi")]
        Table.pagination = False

        return Table

def get_gazole_price(ID):
    api = "https://api.prix-carburants.2aaz.fr/station/"
    array = []
    for id in ID:
        url = api+id[0]
        get_url = requests.get(url)
        data = json.loads(get_url.content)
        nom = data['name']
        prix = data['Fuels'][0]['Price']['value']
        row= (nom,prix)
        array.append(row)
    return array

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
            print(id)
            value = [str(id)]
            conn = sqlite3.connect('stations.db')
            c = conn.cursor()
            sql = ''' INSERT INTO stations(ID) VALUES (?)'''
            c.execute(sql, value)
            conn.commit()
            c.close()
        except Exception as e:
            print (e)